from fastapi.responses import Response, JSONResponse
from typing import Any
import orjson

class CustomORJSONResponse(Response):
    media_type = "application/json"
    def __init__(self, content = None, status_code = 200, headers = None, media_type = None, background = None):
        super().__init__(content, status_code, headers, media_type, background)

        # To make sure this is checked as soon as the server starts and not after the request is made
        assert orjson is not None, "orjson must be installed"

    def render(self, content: Any) -> bytes:
        response_content = {
            "status": "success" if self.status_code < 400 else "error",
            "data": content.get("data"),
            "message": content.get("message", "Success")
        }
        
        if metadata:= content.get("metadata", {}):
            response_content.update(metadata)

        return orjson.dumps(response_content, option=orjson.OPT_INDENT_2)




def json_error_response(status_code: int, detail: str):
    return JSONResponse(
        status_code=status_code,
        content={"detail": detail}
    )