from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Button, Footer, Header, Static, Label
from textual.screen import Screen
from textual.containers import Grid

from ui.screens.home import Home

class QuitScreen(Screen):
    """Screen with a dialog to quit."""
    BINDINGS = [("c", "pop_screen", "Cancel"), ("q", "request_exit", "Confirm")]

    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Are you sure you want to quit?", id="question"),
            Button("Quit", variant="error", id="quit"),
            Button("Cancel", variant="primary", id="cancel"),
            id="dialog",
        )
        yield Footer()

    def action_request_exit(self):
        self.app.exit()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit":
            self.app.exit()
        else:
            self.app.pop_screen()

class LangChainShellApp(App[str]):
    CSS_PATH = "app.css"
    TITLE = "LangChain Shell by Keith Hanson"
    BINDINGS = [("escape", "request_pop", "Go Back"), ("q", "request_quit", "Quit")]
    SCREENS = {"quit": QuitScreen()}

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()

    def action_request_pop(self) -> None:
        if(self.screen_stack.__len__() > 1):
            self.pop_screen()

    def action_request_quit(self) -> None:
        self.push_screen("quit")
