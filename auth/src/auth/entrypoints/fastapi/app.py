"""This module sets up the FasiAPI application that are common to
the various initiation channels. Initiation channels include the
main.py, create_db.py, alembic env.py, and pytest. Each of these
initiation channels can subsequently perform tasks specific to
their area."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.auth.entrypoints.fastapi import routes
from src.middlewares import mw_req_duration

app = FastAPI(title="FastAPI Microservices Demo - Auth service")
app.include_router(routes.signup.router)
app.include_router(routes.signin.router)
app.include_router(routes.refresh.router)
app.include_router(routes.user.router)


# Configure logging
# configure_logging()

# allow_origins = ["http://localhost:5173"]
allow_origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.add_exception_handler(
#     Exception,
#     mw_error_handler.handle_error,
# )

app.middleware("http")(mw_req_duration.request_duration)

# app.add_middleware(LoggingMiddleware)

# app.mount(
#     "/d_content",
#     StaticFiles(directory="src/d_content"),
#     name="d_content",
# )
