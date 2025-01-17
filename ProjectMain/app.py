from fastapi import FastAPI
from auth.middleware import auth_middleware
from auth.views import AuthLoginView, AuthRegisterView
from books.views import BookModelView
from utils.base_response import CustomORJSONResponse
from ProjectMain.database import create_tables
from fastapi.middleware.cors import CORSMiddleware

from ProjectMain.sse import router as sse_router

app = FastAPI(
    title="Assessment API",
    description="ObviouslyAI Assessment API",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(auth_middleware)

# Register routes
create_tables()

app.include_router(BookModelView.as_view(prefix="/books", tags=["Books"]), default_response_class=CustomORJSONResponse)
app.include_router(AuthRegisterView.as_view(prefix="/auth/register"), tags=["auth"])
app.include_router(AuthLoginView.as_view(prefix="/auth/login"), tags=["auth"])
app.include_router(sse_router, prefix="/sse", tags=["SSE"])
