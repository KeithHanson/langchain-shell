from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Button, Footer, Header, Static, Label, Placeholder
from textual.screen import Screen
from textual.containers import Grid, Horizontal, Vertical, Container
from textual.reactive import reactive
from textual import log

class QuitScreen(Screen):
    """Screen with a dialog to quit."""
    BINDINGS = [("c", "request_cancel", "Cancel"), ("q", "request_exit", "Confirm")]

    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Are you sure you want to quit?", id="question"),
            Button("Quit", variant="error", id="quit"),
            Button("Cancel", variant="primary", id="cancel"),
            id="dialog",
        )
        yield Footer()

    def action_request_cancel(self):
        self.app.is_quitting = False
        self.app.pop_screen()

    def action_request_exit(self):
        self.app.exit()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit":
            self.app.exit()
        else:
            self.app.is_quitting = False
            self.app.pop_screen()

class LangChainShellApp(App[str]):
    CSS_PATH = "app.css"
    TITLE = "LangChain Shell by Keith Hanson"
    BINDINGS = [("escape", "request_pop", "Go Back"), ("q", "request_quit", "Quit"), ("t", "request_test_function", "Test")]
    SCREENS = {"quit": QuitScreen()}

    left_container_children = reactive([], layout=True, always_update=True, repaint=True)
    right_container_children = reactive([])
    right_top_children = reactive([])
    right_bottom_children = reactive([])

    is_quitting = reactive(False)

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        with Horizontal():
            with Container(id = "left"):
                for child in self.left_container_children:
                    yield child
            with Container(id = "content"):
                with Container(id = "right-top"):
                    for child in self.right_top_children:
                        yield child
                with Container(id = "right-bottom"):
                    for child in self.right_bottom_children:
                        yield child

        yield Footer()

    def watch_left_container_children(self, value):
        for child in self.children[0].children: 
            log("FOUND CHILD")
            log(child)
            child.refresh()

        log("Fired Watch!")

    def action_request_pop(self) -> None:
        if(self.is_quitting):
            self.is_quitting = False

        if(self.screen_stack.__len__() > 1):
            self.pop_screen()

    def action_request_quit(self) -> None:
        if(not self.is_quitting):
            self.is_quitting = True
            self.push_screen("quit")

    def on_mount(self) -> None:
        """Mount the app."""

    def action_request_test_function(self):
        # Use this function to test things with T
        log("TEST FUNCTION STARTING!")

        self.left_container_children = [Placeholder(id="LeftContainerPlaceholder"), Placeholder(id="LeftContainerPlaceholder2")]
        log(len(self.left_container_children))

        log("TEST FUNCTION COMPLETE!")
        return
