import os
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.uix.floatlayout import FloatLayout # Import FloatLayout

# Construct an absolute path to the font file
font_path = os.path.join(os.path.dirname(__file__), 'DejaVuSansMono.ttf')
LabelBase.register(name='DejaVuSansMono', fn_regular=font_path)

class ClipboardGUI(App):
    def __init__(self, event_bus, history_manager, **kwargs):
        super().__init__(**kwargs)
        self.event_bus = event_bus
        self.history_manager = history_manager
        self.popup = None
        self.is_started = False  # Flag to check if the app is ready
        print("[DEBUG] GUI Initialized. Subscribing to 'hotkey_triggered' event.")
        self.event_bus.subscribe("hotkey_triggered", self.show_popup)

    def build(self):
        # Return a FloatLayout as the root widget to satisfy Kivy's requirement
        # This layout will be invisible until a popup is opened.
        return FloatLayout()

    def on_start(self):
        """This is a Kivy method that is called once the app is running."""
        print("[DEBUG] Kivy app has started. Ready for events.")
        self.is_started = True

    def show_popup(self, data):
        # Only show the popup if the app has fully started
        if not self.is_started:
            print("[DEBUG] Event received before app started. Ignoring.")
            return

        print(f"[DEBUG] 'hotkey_triggered' event received with data: {data}")
        # Use Clock to schedule the popup on the main Kivy thread
        Clock.schedule_once(lambda dt: self._show_popup_internal())

    def _show_popup_internal(self):
        print("[DEBUG] Showing popup.")
        # If a popup is already open, dismiss it before creating a new one
        if self.popup and self.popup.parent:
            self.popup.dismiss()

        items = "\n".join(self.history_manager.get_history() or ["(empty)"])
        self.popup = Popup(
            title="Clipboard History",
            content=Label(text=items, font_name="DejaVuSansMono"),
            size_hint=(0.4, 0.4)
        )
        self.popup.open()
