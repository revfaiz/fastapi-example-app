from fastapi import FastAPI
from router import router as process_router
# import uvicorn

# Create FastAPI app
app = FastAPI()

# Include routes from router.py
app.include_router(process_router)

@app.get("/")
def welcome():
    return {"message": "Welcome to the FastAPI backend!"}
# Run app if this file is executed directly
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
