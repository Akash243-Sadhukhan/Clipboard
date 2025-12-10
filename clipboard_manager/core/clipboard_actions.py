# core/clipboard_actions.py
import platform
import time
from pynput.keyboard import Key, Controller
import pyperclip

kb = Controller()
def trigger_copy():
    """Simulate Cmd+C (macOS) or Ctrl+C (others)."""
    system = platform.system()
    if system == "Darwin":
        with kb.pressed(Key.cmd):
            kb.press('c')
            kb.release('c')
    else:
        with kb.pressed(Key.ctrl):
            kb.press('c')
            kb.release('c')
    time.sleep(0.1)  # give OS time to update clipboard

def get_clipboard_text():
    try:
        text = pyperclip.paste()
        return text.strip() if text else ""
    except Exception as e:
        print("[Clipboard] Read error:", e)
        return ""
