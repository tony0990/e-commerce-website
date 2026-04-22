from datetime import datetime


def format_datetime(dt: datetime) -> str:
    """
    Convert datetime to readable string
    """
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def success_response(message: str, data=None):
    """
    Standard success response format
    """
    return {
        "status": "success",
        "message": message,
        "data": data
    }


def error_response(message: str):
    """
    Standard error response format
    """
    return {
        "status": "error",
        "message": message
    }