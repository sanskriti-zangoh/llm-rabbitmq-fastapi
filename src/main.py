from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers.llm import router as llm_router

app = FastAPI()


origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to LLM Chat Backend"}


app.include_router(llm_router)