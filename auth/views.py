from main import app
from auth.auth import AuthDetails, Token, User
from auth.auth import get_password_hash, authenticate_user
from auth.auth import create_access_token, get_current_active_user
from auth.auth import users, fake_users_db
from datetime import timedelta
from fastapi import Depends, HTTPException, status

ACCESS_TOKEN_EXPIRE_MINUTES = 300


@app.post('/register', status_code=201)
def register(auth_details: AuthDetails):
    if any(user['username'] == auth_details.username for user in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_password = get_password_hash(auth_details.password)
    users.append({
        'username': auth_details.username,
        'hashed_password': hashed_password
    })

    fake_users_db[auth_details.username] = users[-1]
    return {"Info": "Successful registrations! Go to /token to get a token"}


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: AuthDetails):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
