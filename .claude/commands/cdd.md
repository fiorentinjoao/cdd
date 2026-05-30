---
description: Compression Driven Development — spec → plan → build → understanding visual
---

# CDD — Compression Driven Development

Você é o orquestrador do fluxo CDD. Seu objetivo é guiar o usuário por 4 etapas em sequência, com aprovação entre cada uma, e ao final gerar um `understanding.json` que pode ser visualizado na TUI interativa.

## Argumento

`$ARGUMENTS` pode ter dois formatos:
- `<feature>` — fluxo completo (spec → plan → build → compress)
- `fix <feature>` — alteração pequena (build → compress apenas)

Se não fornecido, pergunte.

---

## Modo fix

Se `$ARGUMENTS` começar com `fix`:

1. Extraia o nome da feature (ex: `fix auth-jwt` → feature = `auth-jwt`)
2. Verifique se `.cdd/<feature>/understanding.json` existe — se não existir, avise e encerre
3. Leia o `understanding.json` e o `plan.md` existentes para ter contexto do que já foi feito
4. Pergunte: **"O que você quer alterar?"**
5. Aplique a alteração diretamente no código sem passar por Spec ou Plan
6. Atualize o `understanding.json` refletindo o que mudou — não reescreva tudo, só ajuste os nós afetados
7. Exiba:

```
✓ Fix aplicado — <feature>

O que mudou:
  <descrição curta da alteração>

understanding.json atualizado. Para visualizar:
  cdd <feature>
```

---

## Estrutura de arquivos

Todas as saídas ficam em `.cdd/<feature-name>/`:
```
.cdd/<feature-name>/
  spec.md           ← o que será construído
  plan.md           ← como será construído
  understanding.json ← árvore de entendimento gerada após o build
```

---

## Fluxo

### Etapa 0 — Contexto do projeto

**Antes de qualquer pergunta ao usuário**, carregue o contexto:

1. Verifique se `.cdd/context.md` existe
   - **Se existir**: leia-o integralmente — esse é o contexto do projeto, não precisa varrer o codebase de novo
   - **Se não existir**: avise o usuário `"Contexto não encontrado. Rode /cdd-init primeiro para mapear o projeto."` e encerre

**O `context.md` é suficiente — não leia o codebase novamente.** Todo o mapeamento já foi feito pelo `/cdd-init`. Use o `context.md` como única fonte de contexto do projeto.

Se precisar de detalhe de um arquivo específico durante o Plan ou Build, leia apenas aquele arquivo pontualmente. Não faça leitura ampla do projeto.

Após carregar o contexto, mostre um resumo do que entendeu:

```
Contexto do projeto mapeado:

  Stack:       <linguagem + framework>
  Arquitetura: <como o projeto está organizado>
  Padrões:     <convenções observadas>
  Dependências principais: <libs mais importantes>
  Referência:  <módulo existente que será base para o build>

Qual feature vamos construir?
```

2. Receba o nome da feature do usuário (ou de `$ARGUMENTS` se fornecido)
3. Crie o diretório `.cdd/<feature>/`
4. Informe:

```
CDD iniciado — <feature>

Etapas:
  [1] Spec      — o que vamos construir
  [2] Plan      — como vamos construir
  [3] Build     — geração do código
  [4] Compress  — árvore de entendimento

Começando pela Spec...
```

---

### Etapa 1 — Spec (`spec.md`)

Com o contexto do codebase já em mãos, pergunte ao usuário apenas o que não dá pra inferir:
- O que essa feature deve fazer?
- Quais são os casos de erro/edge cases?
- Há alguma restrição técnica? (só pergunte se não foi possível inferir da stack)

Com as respostas, gere `.cdd/<feature>/spec.md` no formato:

```markdown
# Spec — <feature>

## O que faz
<descrição em 2-3 frases>

## Comportamento esperado
- <comportamento 1>
- <comportamento 2>

## Casos de erro
- <erro 1> → <como tratar>

## Restrições
- <restrição técnica se houver>
```

Mostre o conteúdo gerado e pergunte: **"Spec ok? Posso avançar para o Plan?"**

Aguarde confirmação antes de continuar.

---

### Etapa 2 — Plan (`plan.md`)

Use o contexto já coletado na Etapa 0. Se precisar de mais detalhe sobre algum arquivo específico, leia-o agora. Não pergunte ao usuário o que o codebase já responde.

Gere `.cdd/<feature>/plan.md` no formato:

```markdown
# Plan — <feature>

## Arquivos

| Arquivo | Ação | Motivo |
|---------|------|--------|
| `path/to/file.ts` | criar | <motivo> |
| `path/to/other.ts` | modificar | <motivo> |

## Funções / Classes

### `NomeDoServico`
- `metodo(param: Tipo): RetornoTipo` — <o que faz>
- `outroMetodo(param: Tipo): RetornoTipo` — <o que faz>

## Padrões seguidos
- Segue o padrão de `<módulo existente>` em `<caminho>`

## Ordem de implementação
1. <primeiro passo>
2. <segundo passo>
3. <terceiro passo>
```

Mostre o plan e pergunte: **"Plan ok? Posso iniciar o Build?"**

Aguarde confirmação antes de continuar.

---

### Etapa 3 — Build

Execute a implementação seguindo o `plan.md` exatamente:
- Crie/modifique cada arquivo listado
- Siga os padrões identificados
- Não adicione nada além do que está no plan

Ao terminar, informe os arquivos criados/modificados.

Pergunte: **"Build concluído. Posso gerar o Compress (understanding.json)?"**

Aguarde confirmação antes de continuar.

---

### Etapa 4 — Compress (`understanding.json`)

Analise todo o código gerado no Build e produza `.cdd/<feature>/understanding.json` com exatamente esta estrutura:

```json
{
  "title": "<nome legível da feature>",
  "nodes": [
    {
      "id": "1",
      "label": "O que faz",
      "level": 1,
      "content": "<descrição geral em 1-2 frases do que a feature faz>",
      "status": "unread",
      "children": [
        {
          "id": "2",
          "label": "<nome do módulo/grupo principal>",
          "level": 2,
          "content": "<lista dos arquivos envolvidos e o papel de cada um>",
          "status": "unread",
          "children": [
            {
              "id": "3",
              "label": "<nome do arquivo mais importante>",
              "level": 3,
              "content": "<lista das funções/métodos e o que cada um faz>",
              "code": "<trecho de código relevante — opcional>",
              "status": "unread",
              "children": [
                {
                  "id": "4",
                  "label": "<nome da função mais complexa> — detalhe",
                  "level": 4,
                  "content": "<passo a passo do que a função faz, linha por linha se necessário>",
                  "code": "<corpo completo da função>",
                  "status": "unread",
                  "children": []
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

**Regras para gerar o JSON:**
- Nível 1: sempre "O que faz" — visão geral da feature inteira
- Nível 2: agrupamento por módulo ou responsabilidade
- Nível 3: arquivo específico — lista suas funções/exports
- Nível 4: detalhe de uma função — passo a passo do que acontece internamente
- Pode haver múltiplos nós em qualquer nível (use ids "2a", "2b" etc se necessário)
- `content` nunca pode ser vazio — sempre explique algo útil
- `code` é opcional — inclua apenas quando o trecho de código ajuda a entender. Nível 3 e 4 são os mais indicados
- Escreva em português

---

### Etapa final — Instruções para visualizar

Após salvar o `understanding.json`, exiba:

```
✓ CDD completo — <feature>

Arquivos gerados:
  .cdd/<feature>/spec.md
  .cdd/<feature>/plan.md
  .cdd/<feature>/understanding.json

Para visualizar na TUI:

  cd ~/cdd && uv run python cdd.py $(pwd)/../<projeto>/.cdd/<feature>/understanding.json

Navegue com ↑↓, Enter para expandir, u para marcar entendido.
```
