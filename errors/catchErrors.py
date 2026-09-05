#That's the generic function for all internal server errors on controllers
from fastapi.responses import JSONResponse

from main import app
@app.exception_handler(Exception)
async def global_handler(s, err):
    s.rollback()
    return JSONResponse(
        status_code=500,
        content="Something went wrong"
    )
