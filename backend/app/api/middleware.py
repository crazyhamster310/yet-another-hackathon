import time

from fastapi import Request

from app.core.logging import logger


async def log_requests_middleware(request: Request, call_next):
    start_time = time.time()

    caller = "Anonymous"

    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        caller = auth_header.split(" ")[1]
    elif "token" in request.query_params:
        caller = request.query_params.get("token")

    path = request.url.path
    method = request.method

    logger.info(f"AUDIT [START] | Caller: {caller} | Action: {method} {path}")

    try:
        response = await call_next(request)

        process_time = (time.time() - start_time) * 1000

        logger.info(
            f"AUDIT [END] | Caller: {caller} | Action: {method} {path} | "
            f"Status: {response.status_code} | Time: {process_time:.2f}ms"
        )
        return response

    except Exception as e:
        logger.error(
            f"AUDIT [ERROR] | Caller: {caller} | Action: {method} {path} | Error: {str(e)}"
        )
        raise
