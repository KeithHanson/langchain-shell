from textual.widgets import Button, Footer, Header, Static, Label
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Static

class Home(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Hello, world!")
        yield Footer()

