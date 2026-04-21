"""
Application Constants (Tony)
==============================
Centralized constants used across the application.
Includes role definitions, status enums, and configuration constants.
"""

from enum import Enum


class UserRole(str, Enum):
    """User role enumeration for role-based access control."""
    ADMIN = "admin"
    USER = "user"


class OrderStatus(str, Enum):
    """Order status enumeration."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class PaymentStatus(str, Enum):
    """Payment status enumeration."""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


# --- Pagination Defaults ---
DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# --- Password Validation ---
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 128

# --- Product ---
MAX_PRODUCT_NAME_LENGTH = 255
MAX_PRODUCT_DESCRIPTION_LENGTH = 5000
MAX_CATEGORY_NAME_LENGTH = 100

# --- API Versioning ---
API_V1_PREFIX = "/api/v1"

# --- Error Messages ---
class ErrorMessages:
    """Centralized error messages."""
    INVALID_CREDENTIALS = "Invalid email or password"
    USER_NOT_FOUND = "User not found"
    USER_ALREADY_EXISTS = "A user with this email already exists"
    USER_INACTIVE = "User account is inactive"
    TOKEN_EXPIRED = "Token has expired"
    TOKEN_INVALID = "Invalid or expired token"
    FORBIDDEN = "You don't have permission to perform this action"
    NOT_FOUND = "Resource not found"
    PRODUCT_NOT_FOUND = "Product not found"
    CATEGORY_NOT_FOUND = "Category not found"
    ORDER_NOT_FOUND = "Order not found"
    CART_EMPTY = "Cart is empty"
    INSUFFICIENT_STOCK = "Insufficient stock available"
    INVALID_QUANTITY = "Quantity must be at least 1"


class SuccessMessages:
    """Centralized success messages."""
    USER_CREATED = "User registered successfully"
    USER_UPDATED = "User profile updated successfully"
    USER_DELETED = "User deleted successfully"
    LOGIN_SUCCESS = "Login successful"
    LOGOUT_SUCCESS = "Logged out successfully"
    PASSWORD_CHANGED = "Password changed successfully"
    PRODUCT_CREATED = "Product created successfully"
    PRODUCT_UPDATED = "Product updated successfully"
    PRODUCT_DELETED = "Product deleted successfully"
    ORDER_CREATED = "Order placed successfully"
    ORDER_CANCELLED = "Order cancelled successfully"
    CART_UPDATED = "Cart updated successfully"
    CART_CLEARED = "Cart cleared successfully"
