import uvicorn
from fastapi import FastAPI

from auth_jwt import router

app = FastAPI(title="CDD Auth JWT")
app.include_router(router)


@app.get("/me")
def me_example():
    """Exemplo de uso — substitua pela sua rota protegida."""
    from fastapi import Depends
    from auth_jwt.dependencies import get_current_user
    from auth_jwt.models import User

    # ver auth_jwt/dependencies.py para usar get_current_user nas suas rotas


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
