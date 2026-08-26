from fastapi import FastAPI

from app import config
from app.routes import (
    classify_router,
    emails_router,
    labels_router,
    oauth_router,
)

app = FastAPI()

app.include_router(oauth_router, prefix="/rest/oauth2-credential", tags=["oauth"])
app.include_router(emails_router, tags=["emails"])
app.include_router(classify_router, tags=["classify"])
app.include_router(labels_router, tags=["labels"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=config.PORT)
