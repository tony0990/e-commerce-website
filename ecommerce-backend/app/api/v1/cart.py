
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.cart import Cart, CartItem
from app.schemas.cart import CartOut, CartItemCreate, CartItemUpdate
from app.api.deps import get_db


# tb3 el security el func de---------------------------------------------------------
def get_current_user():
    return 1

router = APIRouter()

# 1. (POST)---------------------------------------------------------------------------
@router.post("/items", status_code=status.HTTP_201_CREATED)
def add_to_cart(
        item_in: CartItemCreate,
        db: Session = Depends(get_db),
        current_user_id: int = Depends(get_current_user)
):
    cart = db.query(Cart).filter(Cart.user_id == current_user_id).first()

    if not cart:
        cart = Cart(user_id=current_user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    existing_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == item_in.product_id
    ).first()

    if existing_item:
        existing_item.quantity += item_in.quantity
    else:
        new_item = CartItem(
            cart_id=cart.id,
            product_id=item_in.product_id,
            quantity=item_in.quantity
        )
        db.add(new_item)

    db.commit()
    return {"message": "The Product Was Added Successfully In Cart"}

# 2. (GET)---------------------------------------------------------------------------------
@router.get("/", response_model=CartOut)
def view_cart(
        db: Session = Depends(get_db),
        current_user_id: int = Depends(get_current_user)
):
    cart = db.query(Cart).filter(Cart.user_id == current_user_id).first()

    if not cart:
        return {"id": 0, "user_id": current_user_id, "items": []}
    return cart

# 3. (PUT)---------------------------------------------------------------------------------------
@router.put("/items/{item_id}")
def update_cart_item(
        item_id: int,
        item_in: CartItemUpdate,
        db: Session = Depends(get_db),
        current_user_id: int = Depends(get_current_user)
):
    cart = db.query(Cart).filter(Cart.user_id == current_user_id).first()
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Your Cart Doesn`t Exist")
    item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.cart_id == cart.id
    ).first()

    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This Item Doesn`t Exist In Your Cart")

    item.quantity = item_in.quantity
    db.commit()
    db.refresh(item)

    return {"message": "Quantity Updated Successfully", "item": item}

# 4. (DELETE)----------------------------------------------------------------------------------------------------
@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_cart(
        item_id: int,
        db: Session = Depends(get_db),
        current_user_id: int = Depends(get_current_user)
):
    cart = db.query(Cart).filter(Cart.user_id == current_user_id).first()
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Your Cart Doesn`t Exist ")
    item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.cart_id == cart.id
    ).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This Item Doesn`t Exist In Your Cart")

    db.delete(item)
    db.commit()

    return None

# 5. (DELETE)--------------------------------------------------------------------------------------------
@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def clear_cart(
        db: Session = Depends(get_db),
        current_user_id: int = Depends(get_current_user)
):
    cart = db.query(Cart).filter(Cart.user_id == current_user_id).first()

    if cart:
        db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
        db.commit()

    return None