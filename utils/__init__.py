from typing import Dict, Any, List, Optional, Tuple, Union


def safe_convert(value: Any, to_type: Any = int, default=None) -> int:
    try:
        return to_type(value) if value else default  
    except (ValueError, TypeError):
        return default
