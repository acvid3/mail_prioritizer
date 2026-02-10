import os
from fastapi import FastAPI
from dotenv import load_dotenv

from src.routes import oauth_router, emails_router, classify_router

load_dotenv()

app = FastAPI()

# Include routers
app.include_router(oauth_router, prefix="/rest/oauth2-credential", tags=["oauth"])
app.include_router(emails_router, tags=["emails"])
app.include_router(classify_router, tags=["classify"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8082)
