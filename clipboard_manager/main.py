import ctypes
import sys
import threading
from core.hotkey_listener import HotkeyListener
from core.event_bus import EventBus
from gui.app import ClipboardGUI

# This is a placeholder until you create your actual history manager
class PlaceholderHistoryManager:
    def get_history(self):
        return ["Clipboard Item 1", "Clipboard Item 2", "Another Item"]

def is_admin():
    """Check if the script is running with administrative privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def main():
    """Initializes and runs the application components."""
    print("Starting Clipboard Manager...")

    event_bus = EventBus()
    event_bus_thread = threading.Thread(target=event_bus.start, daemon=True)
    event_bus_thread.start()

    # The HotkeyListener runs in a background thread
    # CORRECTED: Pass only the event_bus to the constructor
    hotkey_listener = HotkeyListener(event_bus)
    hotkey_listener.start()

    # For now, we use a placeholder for the history manager
    history_manager = PlaceholderHistoryManager()

    # The Kivy app runs on the main thread and listens for events
    clipboard_gui = ClipboardGUI(event_bus=event_bus, history_manager=history_manager)
    clipboard_gui.run()  # This starts the Kivy application loop

    print("Clipboard Manager stopped.")


if __name__ == "__main__":
    if is_admin():
        main()
    else:
        print("Requesting administrator privileges...")
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
