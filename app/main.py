from starlette.middleware.cors import CORSMiddleware

from fastapi import FastAPI
from apis import user, oauth, spot, ai_course, card


app = FastAPI()
app.include_router(user.router)
app.include_router(oauth.router)
app.include_router(spot.router)
app.include_router(ai_course.router)
app.include_router(card.router)


app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)


@app.get("/")
def health_check_handler():
    return {"ping": "pong"}
