# Spec — auth-jwt

## O que faz
Autentica usuários via JWT, gerando um token de acesso no login e validando-o nas rotas protegidas. Suporta refresh de token para renovar sessões sem novo login.

## Comportamento esperado
- Usuário envia credenciais (email/senha) e recebe um `access_token` e um `refresh_token`
- Rotas protegidas validam o `access_token` no header `Authorization: Bearer <token>`
- Quando o `access_token` expira, o usuário pode trocá-lo por um novo usando o `refresh_token`
- Logout invalida o `refresh_token`

## Casos de erro
- Token expirado → retorna `401 Unauthorized` com mensagem `"token_expired"`
- Token inválido/malformado → retorna `401 Unauthorized` com mensagem `"token_invalid"`
- Credenciais incorretas no login → retorna `401 Unauthorized` com mensagem `"invalid_credentials"`
- Refresh token inválido ou já usado → retorna `401 Unauthorized` com mensagem `"refresh_token_invalid"`
- Rota protegida sem token → retorna `401 Unauthorized` com mensagem `"token_missing"`

## Restrições
- Nenhuma restrição técnica definida
