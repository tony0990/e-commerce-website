"""
Order Service
=============
Business logic for orders:
- Place order
- Calculate total amount
- Validate stock
- Deduct inventory
- Track orders
- Update order status
- Prevent invalid status transitions
"""

from typing import List
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.core.constants import OrderStatus, PaymentStatus, ErrorMessages
from app.models.order import Order
from app.models.order_item import OrderItem
from app.repositories.order_repository import OrderRepository
from app.repositories.order_item_repository import OrderItemRepository
from app.schemas.order import PlaceOrderRequest
from app.services.inventory_service import InventoryService
from app.utils.exceptions import BadRequestException, NotFoundException


VALID_ORDER_TRANSITIONS = {
    OrderStatus.PENDING: {
        OrderStatus.CONFIRMED,
        OrderStatus.CANCELLED,
    },
    OrderStatus.CONFIRMED: {
        OrderStatus.PROCESSING,
        OrderStatus.CANCELLED,
    },
    OrderStatus.PROCESSING: {
        OrderStatus.SHIPPED,
        OrderStatus.CANCELLED,
    },
    OrderStatus.SHIPPED: {
        OrderStatus.DELIVERED,
    },
    OrderStatus.DELIVERED: {
        OrderStatus.REFUNDED,
    },
    OrderStatus.CANCELLED: set(),
    OrderStatus.REFUNDED: set(),
}


class OrderService:
    """
    Service layer for order workflows.
    Contains the real rules of the order system.
    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.order_repo = OrderRepository(db)
        self.order_item_repo = OrderItemRepository(db)
        self.inventory_service = InventoryService(db)

    async def place_order(
        self,
        user_id: int,
        data: PlaceOrderRequest,
    ) -> Order:
        """
        Create a new order for a user.

        Steps:
        1. Validate products.
        2. Validate stock.
        3. Calculate total amount.
        4. Create order.
        5. Create order items.
        6. Deduct stock.
        7. Return full order.
        """

        total_amount = 0.0
        order_items: List[OrderItem] = []
        product_map = {}
        seen_products = set()
        product_names = []

        for item in data.items:
            if item.product_id in seen_products:
                raise BadRequestException(
                    f"Duplicate product in order: product_id={item.product_id}"
                )

            seen_products.add(item.product_id)

            product = await self.inventory_service.get_product_by_id(
                item.product_id
            )

            await self.inventory_service.validate_stock(
                product=product,
                quantity=item.quantity,
            )

            line_total = product.price * item.quantity
            total_amount += line_total

            product_map[item.product_id] = product
            product_names.append(f"{product.name} (x{item.quantity}, ${product.price})")

            order_items.append(
                OrderItem(
                    product_id=product.id,
                    quantity=item.quantity,
                    unit_price=product.price,
                    total_price=line_total,
                )
            )

        order = Order(
            user_id=user_id,
            total_amount=total_amount,
            shipping_cost=0.0,
            tax_amount=0.0,
            status=OrderStatus.PENDING,
            payment_status=PaymentStatus.PENDING,
            payment_method=data.payment_method,
            shipping_address=data.shipping_address,
            shipping_city=data.shipping_city,
            shipping_state=data.shipping_state,
            shipping_zip=data.shipping_zip,
            shipping_country=data.shipping_country,
            tracking_number=self._generate_tracking_number(),
            notes=data.notes,
        )

        order = await self.order_repo.create(order)

        for order_item in order_items:
            order_item.order_id = order.id

        await self.order_item_repo.create_many(order_items)

        for item in data.items:
            product = product_map[item.product_id]
            await self.inventory_service.deduct_stock(
                product=product,
                quantity=item.quantity,
            )

        await self.db.flush()

        created_order = await self.order_repo.get_by_id(order.id)

        if not created_order:
            raise NotFoundException(ErrorMessages.ORDER_NOT_FOUND)

        # Log order placement with full details
        logger.info(
            f"[ORDER] Order placed: order_id={order.id}, "
            f"user_id={user_id}, "
            f"total=${total_amount:.2f}, "
            f"payment={data.payment_method}, "
            f"city={data.shipping_city}, country={data.shipping_country}, "
            f"products=[{', '.join(product_names)}], "
            f"tracking={order.tracking_number}"
        )

        return created_order

    async def get_my_orders(self, user_id: int) -> List[Order]:
        """
        Get all orders that belong to the current user.
        """

        return await self.order_repo.get_orders_by_user(user_id)

    async def get_order_for_user(
        self,
        order_id: int,
        user_id: int,
    ) -> Order:
        """
        Get one order for a specific user.
        Prevents users from seeing other users' orders.
        """

        order = await self.order_repo.get_user_order(
            order_id=order_id,
            user_id=user_id,
        )

        if not order:
            raise NotFoundException(ErrorMessages.ORDER_NOT_FOUND)

        return order

    async def get_order_for_admin(
        self,
        order_id: int,
    ) -> Order:
        """
        Get any order by ID.
        Admin-only usage.
        """

        order = await self.order_repo.get_by_id(order_id)

        if not order:
            raise NotFoundException(ErrorMessages.ORDER_NOT_FOUND)

        return order

    async def get_all_orders(self) -> List[Order]:
        """
        Get all orders in the system.
        Admin-only usage.
        """

        return await self.order_repo.get_all()

    async def update_order_status(
        self,
        order_id: int,
        new_status: OrderStatus,
    ) -> Order:
        """
        Update order status after validating transition rules.
        """

        order = await self.order_repo.get_by_id(order_id)

        if not order:
            raise NotFoundException(ErrorMessages.ORDER_NOT_FOUND)

        old_status = order.status

        self._validate_status_transition(
            current_status=order.status,
            new_status=new_status,
        )

        updated_order = await self.order_repo.update_status(
            order=order,
            new_status=new_status,
        )

        # Log status change
        logger.info(
            f"[ORDER] Status changed: order_id={order_id}, "
            f"user_id={order.user_id}, "
            f"from={old_status.value}, to={new_status.value}"
        )

        return updated_order

    async def track_order(
        self,
        order_id: int,
        user_id: int,
    ) -> Order:
        """
        Track one order for the current user.
        """

        order = await self.order_repo.get_user_order(
            order_id=order_id,
            user_id=user_id,
        )

        if not order:
            raise NotFoundException(ErrorMessages.ORDER_NOT_FOUND)

        return order

    def _validate_status_transition(
        self,
        current_status: OrderStatus,
        new_status: OrderStatus,
    ) -> None:
        """
        Prevent invalid order status transitions.

        Example:
        pending -> confirmed is allowed.
        delivered -> pending is not allowed.
        """

        if current_status == new_status:
            raise BadRequestException(
                f"Order is already in '{new_status.value}' status"
            )

        allowed_next_statuses = VALID_ORDER_TRANSITIONS.get(
            current_status,
            set(),
        )

        if new_status not in allowed_next_statuses:
            raise BadRequestException(
                f"Invalid order transition from "
                f"'{current_status.value}' to '{new_status.value}'"
            )

    def _generate_tracking_number(self) -> str:
        """
        Generate a simple unique tracking number.
        """

        return f"TRK-{uuid4().hex[:10].upper()}"