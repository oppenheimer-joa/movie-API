import uvicorn
from fastapi import FastAPI
from routers.test import router as test
from routers.load_router import router as load_router
from routers.check_router import router as check_router
from routers.blob_router import router as blob_router

def create_app():
    app = FastAPI()
    app.include_router(test)
    app.include_router(load_router)
    app.include_router(check_router)
    app.include_router(blob_router)
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=2233)