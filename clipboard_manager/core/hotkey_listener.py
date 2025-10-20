# core/hotkey_listener.py
import threading
from pynput import keyboard

class HotkeyListener(threading.Thread):
    def __init__(self, event_bus, hotkey="<ctrl>+v", check_interval=0.05):
        super().__init__(daemon=True)
        self.event_bus = event_bus
        self.hotkey = hotkey
        self.check_interval = check_interval
        self.listener = None

    def run(self):
        print(f"[{self.name}] is running HotkeyListener")
        
        def on_activate():
            self.event_bus.emit("HOTKEY_TRIGGER", None)

        with keyboard.GlobalHotKeys({
            self.hotkey: on_activate,
        }) as self.listener:
            self.listener.join()

    def stop(self):
        if self.listener:
            self.listener.stop()
