# Plan — auth-jwt

## Arquivos

| Arquivo | Ação | Motivo |
|---------|------|--------|
| `pyproject.toml` | modificar | adicionar dependências: fastapi, uvicorn, pyjwt, passlib, python-multipart |
| `auth_jwt/__init__.py` | criar | expõe o router do módulo |
| `auth_jwt/config.py` | criar | configurações JWT (secret, algoritmo, expiração) |
| `auth_jwt/models.py` | criar | modelos Pydantic: User, TokenPair, TokenData, LoginRequest |
| `auth_jwt/security.py` | criar | lógica de criação/validação de tokens e hash de senha |
| `auth_jwt/store.py` | criar | armazenamento in-memory de usuários e refresh tokens |
| `auth_jwt/router.py` | criar | endpoints: POST /login, POST /refresh, POST /logout |
| `auth_jwt/dependencies.py` | criar | dependência FastAPI `get_current_user` para rotas protegidas |
| `main.py` | modificar | montar o router e expor a app FastAPI |

## Funções / Classes

### `auth_jwt/config.py`
- `Settings` — dataclass com `SECRET_KEY`, `ALGORITHM = "HS256"`, `ACCESS_TOKEN_EXPIRE_MINUTES = 15`, `REFRESH_TOKEN_EXPIRE_DAYS = 7`

### `auth_jwt/models.py`
- `User` — `id: str`, `email: str`, `hashed_password: str`
- `LoginRequest` — `email: str`, `password: str`
- `TokenPair` — `access_token: str`, `refresh_token: str`, `token_type: str = "bearer"`
- `TokenData` — `sub: str`, `type: str` (access | refresh)

### `auth_jwt/security.py`
- `hash_password(plain: str) -> str` — retorna bcrypt hash
- `verify_password(plain: str, hashed: str) -> bool` — compara com bcrypt
- `create_token(data: dict, expires_delta: timedelta) -> str` — gera JWT com `exp`
- `decode_token(token: str) -> TokenData` — valida e decodifica; levanta `401` em caso de expirado ou inválido

### `auth_jwt/store.py`
- `users: dict[str, User]` — dicionário in-memory com um usuário seed
- `refresh_tokens: set[str]` — conjunto de refresh tokens ativos
- `get_user_by_email(email: str) -> User | None`
- `add_refresh_token(token: str) -> None`
- `revoke_refresh_token(token: str) -> None`
- `is_refresh_token_valid(token: str) -> bool`

### `auth_jwt/router.py`
- `POST /auth/login` — valida credenciais, retorna `TokenPair`
- `POST /auth/refresh` — recebe `refresh_token`, retorna novo `TokenPair`
- `POST /auth/logout` — revoga o `refresh_token`

### `auth_jwt/dependencies.py`
- `get_current_user(token: str = Depends(oauth2_scheme)) -> User` — decodifica o access token e retorna o usuário; usado como dependência em rotas protegidas

## Padrões seguidos
- Estrutura de módulo Python com `__init__.py` expondo apenas o necessário
- Dependências FastAPI via `Depends()` para injeção nas rotas
- Modelos Pydantic para validação de entrada/saída

## Ordem de implementação
1. Atualizar `pyproject.toml` com as dependências
2. Criar `auth_jwt/config.py`
3. Criar `auth_jwt/models.py`
4. Criar `auth_jwt/security.py`
5. Criar `auth_jwt/store.py`
6. Criar `auth_jwt/dependencies.py`
7. Criar `auth_jwt/router.py`
8. Criar `auth_jwt/__init__.py`
9. Atualizar `main.py` para montar o router e expor a app
