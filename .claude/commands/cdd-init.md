---
description: Mapeia o codebase atual e salva o contexto para uso do /cdd
---

# CDD Init — Mapeamento do Codebase

Você vai fazer uma leitura profunda e completa do projeto atual e salvar o resultado em `.cdd/context.md`. Este arquivo será lido por todo `/cdd` e `/cdd fix` antes de qualquer ação.

## O que ler

Leia tudo que for relevante para entender o projeto completamente:

1. Estrutura completa de pastas e arquivos
2. Arquivos de configuração: `package.json`, `pyproject.toml`, `requirements.txt`, `go.mod`, `Cargo.toml`, `pom.xml`, `build.gradle` — o que existir
3. `README.md` e qualquer outra documentação na raiz
4. Arquivos de ambiente: `.env.example`, `docker-compose.yml`, `Dockerfile`
5. Arquivo de entrada principal: `main.py`, `index.ts`, `app.py`, `server.ts`, `main.go`, etc
6. Pelo menos 3 módulos/features já implementados — leia completo cada um
7. Arquivos de configuração de lint, testes, CI se existirem
8. Se houver `.cdd/` com features anteriores, leia todos os `plan.md` e `spec.md`

## O que extrair

Durante a leitura, mapeie:

- **Stack**: linguagem, framework, runtime, versões
- **Arquitetura**: como o projeto está organizado (camadas, módulos, monorepo, etc)
- **Padrões de nomenclatura**: arquivos, funções, classes, variáveis
- **Estrutura de pastas**: onde ficam controllers, services, models, testes, etc
- **Convenções de código**: como imports são feitos, como erros são tratados, estilo geral
- **Dependências principais**: libs mais usadas e pra que servem
- **Padrão de módulo**: como uma feature típica é estruturada (quais arquivos, em que ordem)
- **Como rodar**: comandos de dev, test, build
- **Integrações**: banco de dados, cache, storage, APIs externas

## Formato do `.cdd/context.md`

Salve em `.cdd/context.md`:

```markdown
# CDD Context — <nome do projeto>

> Gerado em: <data>

## Stack
- Linguagem: <ex: TypeScript 5.x>
- Framework: <ex: NestJS 11>
- Runtime: <ex: Node.js 20>
- Banco: <ex: PostgreSQL + Drizzle ORM>
- Cache: <ex: Redis>
- Storage: <ex: MinIO>

## Arquitetura
<descrição em 3-5 frases de como o projeto está organizado>

## Estrutura de pastas
```
<árvore simplificada das pastas principais>
```

## Padrão de módulo
<como uma feature típica é estruturada — quais arquivos, em que ordem, exemplo real>

## Convenções
- Nomenclatura: <ex: camelCase para funções, PascalCase para classes>
- Imports: <ex: sempre absolutos a partir de src/>
- Erros: <ex: lançar HttpException com código e mensagem padronizada>
- Testes: <ex: arquivos .spec.ts ao lado do arquivo testado>

## Dependências principais
- `<lib>` — <pra que serve>
- `<lib>` — <pra que serve>

## Como rodar
- Dev: `<comando>`
- Testes: `<comando>`
- Build: `<comando>`

## Módulos existentes
- `<módulo>` em `<caminho>` — <o que faz>
- `<módulo>` em `<caminho>` — <o que faz>

## Observações
<qualquer padrão não óbvio, decisão técnica importante, ou restrição que afeta o desenvolvimento>
```

## Após salvar

Exiba:

```
✓ CDD Init completo

Contexto salvo em .cdd/context.md

  Stack:       <stack detectada>
  Arquitetura: <resumo em 1 linha>
  Módulos mapeados: <quantidade>

Agora você pode usar /cdd <feature> com contexto completo do projeto.
```

## Atualização

Se `.cdd/context.md` já existir, pergunte ao usuário:
- "Contexto existente encontrado. Atualizar completamente ou só adicionar o que mudou?"
- Se atualizar: refaça a leitura completa
- Se adicionar: leia apenas o que mudou desde a última geração e faça merge
