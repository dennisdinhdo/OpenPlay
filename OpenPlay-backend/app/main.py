from fastapi import FastAPI
from app.database import Base, engine
from app.routes import users, events, invites

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(events.router, prefix="/api/events", tags=["events"])
app.include_router(invites.router, prefix="/api/invites", tags=["invites"])