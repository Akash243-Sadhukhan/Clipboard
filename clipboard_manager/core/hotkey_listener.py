import threading
from pynput import keyboard

class HotkeyListener(threading.Thread):
    def __init__(self, event_bus):
        super().__init__(daemon=True)
        self.event_bus = event_bus
        self.current_keys = set()
        self.listener = None

    def run(self):
        print("[DEBUG] HotkeyListener thread started.")
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()
        self.listener.join()
        print("[DEBUG] HotkeyListener thread stopped.")

    def on_press(self, key):
        if isinstance(key, keyboard.Key):
            self.current_keys.add(key)
        elif hasattr(key, 'char'):
            self.current_keys.add(key.char)
        print(f"[DEBUG] Keys pressed: {self.current_keys}")
        self.check_key()

    def on_release(self, key):
        # Use a try-except block to avoid crashing if the key is not in the set
        try:
            if key in self.current_keys:
                self.current_keys.remove(key)
            elif hasattr(key, 'char') and key.char in self.current_keys:
                self.current_keys.remove(key.char)
        except KeyError:
            pass # Key was already removed

    def check_key(self):
        show_hotkey = frozenset([keyboard.Key.ctrl, 'v'])
        stop_hotkey = frozenset([keyboard.Key.ctrl, 'c'])

        if show_hotkey.issubset(self.current_keys):
            print("[DEBUG] Ctrl+V detected! Emitting event.")
            self.event_bus.emit("hotkey_triggered", {"hotkey": "ctrl+v"})
            self.current_keys.clear()
        
        elif stop_hotkey.issubset(self.current_keys):
            print("[DEBUG] Ctrl+C detected! Stopping listener.")
            self.stop()

    def stop(self):
        if self.listener:
            self.listener.stop()
