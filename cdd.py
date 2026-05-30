#!/usr/bin/env python3
"""CDD — Compression Driven Development TUI"""

from textual.app import App, ComposeResult
from textual.widgets import Tree, Header, Footer, Static, RichLog
from textual.widgets.tree import TreeNode
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from rich.text import Text
from rich.syntax import Syntax
import json
import sys
from pathlib import Path

STATUS = {
    "unread": "[dim]·[/dim]",
    "reading": "[yellow]?[/yellow]",
    "done": "[green]✓[/green]",
}

EXAMPLE_DATA = {
    "title": "Auth com JWT",
    "nodes": [
        {
            "id": "1",
            "label": "O que faz",
            "level": 1,
            "content": "Implementa autenticação completa com JWT — login, refresh token e proteção de rotas via guard.",
            "status": "unread",
            "children": [
                {
                    "id": "2",
                    "label": "Módulos envolvidos",
                    "level": 2,
                    "content": "• auth.module.ts  — registra o módulo e suas dependências\n• auth.service.ts — lógica de login e refresh\n• auth.guard.ts   — protege rotas validando o JWT em cada request",
                    "status": "unread",
                    "children": [
                        {
                            "id": "3",
                            "label": "auth.service.ts",
                            "level": 3,
                            "content": "• login()        — valida credenciais, gera access + refresh token\n• refresh()      — valida refresh token, emite novo access token\n• validateUser() — chamado pelo guard em cada request autenticado",
                            "status": "unread",
                            "children": [
                                {
                                    "id": "4",
                                    "label": "login() — detalhe",
                                    "level": 4,
                                    "content": "Recebe email e senha.\nBusca o usuário via UserRepository.findByEmail().\nCompara a senha com bcrypt.compare().\nSe válido, assina um JWT com payload { sub: userId, email } e TTL de 15min.\nRetorna { accessToken, refreshToken }.",
                                    "status": "unread",
                                    "children": [],
                                }
                            ],
                        }
                    ],
                }
            ],
        }
    ],
}


class CDDApp(App):
    CSS = """
    Screen {
        layout: vertical;
    }
    #bar {
        height: 1;
        background: $primary;
        color: $text;
        padding: 0 2;
    }
    #main {
        layout: horizontal;
        height: 1fr;
    }
    #tree-panel {
        width: 36;
        border-right: solid $primary-darken-2;
        padding: 1 1;
    }
    #content-panel {
        padding: 1 2;
        height: 1fr;
        overflow-y: auto;
        overflow-x: hidden;
        width: 1fr;
    }
    """

    BINDINGS = [
        Binding("u", "mark_done", "✓ Entendido"),
        Binding("r", "mark_unread", "· Não lido"),
        Binding("q", "quit", "Sair"),
    ]

    def __init__(self, data: dict):
        super().__init__()
        self.data = data
        self._selected_node = None

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        yield Static(f" CDD  —  {self.data['title']}", id="bar")
        with Horizontal(id="main"):
            with Vertical(id="tree-panel"):
                yield Tree("Estrutura", id="tree")
            yield RichLog(id="content-panel", wrap=True, highlight=False, markup=True)
        yield Footer()

    def on_mount(self) -> None:
        tree = self.query_one(Tree)
        tree.root.expand()
        for node_data in self.data["nodes"]:
            self._add_node(tree.root, node_data)
        log = self.query_one("#content-panel", RichLog)
        log.write("[dim]← selecione um item na árvore[/dim]")

    def _add_node(self, parent: TreeNode, node_data: dict) -> None:
        status = STATUS[node_data.get("status", "unread")]
        indent = "  " * (node_data["level"] - 1)
        label = f"{indent}[{node_data['level']}] {node_data['label']}  {status}"
        node = parent.add(label, data=node_data)
        for child in node_data.get("children", []):
            self._add_node(node, child)
        if node_data.get("children"):
            node.collapse()

    def _refresh_label(self, node: TreeNode, node_data: dict) -> None:
        status = STATUS[node_data.get("status", "unread")]
        indent = "  " * (node_data["level"] - 1)
        label = f"{indent}[{node_data['level']}] {node_data['label']}  {status}"
        node.set_label(label)

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        if not event.node.data:
            return
        node_data = event.node.data
        self._selected_node = event.node

        if node_data.get("status") == "unread":
            node_data["status"] = "reading"
            self._refresh_label(event.node, node_data)

        level = node_data["level"]
        label = node_data["label"]
        content_text = node_data["content"]
        children = node_data.get("children", [])
        children_hint = ""
        if children:
            names = "  ,  ".join(f"[{c['level']}] {c['label']}" for c in children)
            children_hint = f"\n\n[dim]── filhos: {names}[/dim]"

        log = self.query_one("#content-panel", RichLog)
        log.clear()
        log.write(f"[bold cyan][{level}] {label}[/bold cyan]")
        log.write("─" * 40)
        log.write("")
        for line in content_text.splitlines():
            log.write(line)
        if children_hint:
            log.write("")
            log.write(children_hint.strip())

        code = node_data.get("code")
        if code:
            log.write("")
            log.write("[dim]── código ──────────────────────────────────────────[/dim]")
            log.write("")
            log.write(
                Syntax(
                    code,
                    "python",
                    theme="dracula",
                    word_wrap=True,
                    background_color="default",
                )
            )

        log.write("")
        log.write("[dim]  u  marcar como entendido    r  desmarcar[/dim]")

    def action_mark_done(self) -> None:
        if self._selected_node and self._selected_node.data:
            self._selected_node.data["status"] = "done"
            self._refresh_label(self._selected_node, self._selected_node.data)

    def action_mark_unread(self) -> None:
        if self._selected_node and self._selected_node.data:
            self._selected_node.data["status"] = "unread"
            self._refresh_label(self._selected_node, self._selected_node.data)


def main():
    data = EXAMPLE_DATA
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
        if path.exists():
            data = json.loads(path.read_text())
        else:
            print(f"Arquivo não encontrado: {path}")
            sys.exit(1)
    CDDApp(data).run()


if __name__ == "__main__":
    main()
