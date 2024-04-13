from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from embeddings.api.files import files_router
from embeddings.api.openai import openai_router


def configure_cors(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app = FastAPI(
    debug=True,
    title='embeddings',
)

configure_cors(app)


@app.get("/", include_in_schema=False)
async def redirect_from_root() -> RedirectResponse:
    return RedirectResponse(url='/docs')


app.include_router(openai_router, prefix="/api/v1")
app.include_router(files_router, prefix="/api/v1")