import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return user


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    pass


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
