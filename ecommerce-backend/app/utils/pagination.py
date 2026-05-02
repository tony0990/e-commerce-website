from typing import Tuple, List, Any, Dict
from sqlalchemy.orm import Query, Session

def get_pagination_params(page: int = 1, size: int = 10) -> Tuple[int, int]:
    """Calculate offset and limit with sane defaults."""
    page = max(1, page)
    size = max(1, min(size, 100))  # max 100 items per page
    offset = (page - 1) * size
    return offset, size

def paginate(
    query: Query, 
    page: int = 1, 
    size: int = 10, 
    db: Session = None
) -> Dict[str, Any]:
    """Return paginated results + metadata."""
    offset, limit = get_pagination_params(page, size)
    
    total = query.count()
    items = query.offset(offset).limit(limit).all()
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "size": limit,
        "pages": (total + limit - 1) // limit if limit > 0 else 0,
    }