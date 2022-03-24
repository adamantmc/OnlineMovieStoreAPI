from fastapi import FastAPI
from auth.views import router as auth_router
from movie_store.views import router as store_router


app = FastAPI()
app.include_router(auth_router)
app.include_router(store_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
