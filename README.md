# CDD — Compression Driven Development

> Write code. Keep the reasoning.

CDD is a 4-stage development workflow powered by Claude that automatically generates a navigable knowledge tree alongside every feature you build.

## The problem

You finish a feature. The reasoning behind every decision lives in a chat that's gone, or in your head. Three months later — you remember nothing.

## The solution

CDD compresses the *why* behind your code into a hierarchical `understanding.json` file, navigable via an interactive TUI.

```
project/
├── .cdd/
│   ├── context.md              ← project context (generated once by /cdd-init)
│   └── <feature-name>/
│       ├── spec.md             ← what the feature does
│       ├── plan.md             ← how to build it
│       └── understanding.json  ← navigable knowledge tree
```

## The 4 stages

| # | Stage | Output |
|---|-------|--------|
| 1 | **Spec** | What the feature does — no code yet |
| 2 | **Plan** | Files, functions, technical decisions |
| 3 | **Build** | Actual implementation |
| 4 | **Compress** | Knowledge tree, navigable in the TUI |

## Claude Code skills

Add the skills from `.claude/commands/` to your project and use:

| Command | Description |
|---------|-------------|
| `/cdd-init` | Map the codebase once, save context to `.cdd/context.md` |
| `/cdd <feature>` | Run the full spec → plan → build → compress flow |
| `/cdd fix <feature>` | Quick modification to an existing feature |
| `/cdd-view <feature>` | Open the TUI to navigate `understanding.json` |

## TUI — Interactive viewer

```bash
# Install dependencies
uv sync

# Navigate a feature
uv run cdd.py <feature-name>
```

**Controls:** `↑↓` navigate · `Enter` expand/collapse · `u` mark understood · `r` unmark · `q` quit

## Example

The `auth-jwt` feature is included as a complete example — JWT authentication with access + refresh tokens, built with CDD from scratch.

## Requirements

- Python 3.12+
- [uv](https://github.com/astral-sh/uv)
- [Claude Code](https://claude.ai/code)

## Install

```bash
git clone https://github.com/fiorentinjoao/cdd
cd cdd
uv sync

# Copy skills to your project
cp .claude/commands/cdd*.md /path/to/your/project/.claude/commands/
```
