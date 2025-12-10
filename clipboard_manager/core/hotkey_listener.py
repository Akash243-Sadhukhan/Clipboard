import threading
from pynput import keyboard

class HotkeyListener(threading.Thread):
    def __init__(self, event_bus, name="HotkeyListener"):
        super().__init__(daemon=True)
        self.event_bus = event_bus
        self.current_keys = set()
        self.listener = None

    def run(self):
        print("[DEBUG] HotkeyListener thread started.")
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        self.listener.start()
        self.listener.join()
        print("[DEBUG] HotkeyListener thread stopped.")

    # ── Key normalization ──────────────────────────────────
    def _normalize_key(self, key):
        """Return a simple string name for a key (e.g., 'ctrl', 'shift', 'v')."""
        # Modifier keys
        if key in (keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
            return "ctrl"
        if key in (keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r):
            return "shift"
        if key in (keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r):
            return "alt"

        # Simple character keys
        if hasattr(key, "char") and key.char is not None:
            c = key.char
            # Handle control codes (\x01 - \x1a) -> (a - z)
            if len(c) == 1 and 1 <= ord(c) <= 26:
                return chr(ord(c) + 96)
            return c.lower()

        # Fallback for other special keys
        if isinstance(key, keyboard.Key):
            # Clean up 'Key.enter' -> 'enter'
            return str(key).replace('Key.', '')
        
        # Last resort: use the key code if available
        if hasattr(key, 'vk') and key.vk is not None:
            # Simple number/letter mapping could go here if needed
            pass

        return str(key)

    def on_press(self, key):
        name = self._normalize_key(key)
        if name:
            self.current_keys.add(name)
            print(f"[DEBUG] Keys pressed: {self.current_keys}")
            self.check_key()

    def on_release(self, key):
        name = self._normalize_key(key)
        if name and name in self.current_keys:
            try:
                self.current_keys.remove(name)
            except KeyError:
                print(f"[DEBUG] Key {name} was not in current_keys set.")

    def check_key(self):
        copy_hotkey = {"ctrl", "c"}          # Ctrl+c
        paste_hotkey = {"ctrl", "v"}          # Ctrl+v
        stop_hotkey  = {"ctrl", "shift", "c"} # Ctrl+Shift+C

        if stop_hotkey.issubset(self.current_keys):
            print("[DEBUG] Ctrl+Shift+C detected! Stopping listener.")
            self.stop()
            self.current_keys.clear()

        elif paste_hotkey.issubset(self.current_keys):
            print("[DEBUG] Ctrl+V detected! Emitting event.")
            self.event_bus.emit("hotkey_triggered", {"hotkey": "ctrl+v"})
            self.current_keys.clear()

        elif copy_hotkey.issubset(self.current_keys):
            print("[DEBUG] Ctrl+C detected! Emitting event.")
            self.event_bus.emit("hotkey_triggered", {"hotkey": "ctrl+c"})
            self.current_keys.clear()  # avoid multiple triggers if held
    
    def stop(self):
        if self.listener:
            self.listener.stop()
            print("[DEBUG] HotkeyListener stopped.")