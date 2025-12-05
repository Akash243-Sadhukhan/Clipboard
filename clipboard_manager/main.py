import ctypes
import platform
import sys
import threading
import traceback
import time

from core.Event_bus import EventBus
from core.hotkey_listener import HotkeyListener
from gui.app import ClipboardGUI

# Temporary until you plug in the real one
class PlaceholderHistoryManager:
    def get_history(self):
        return ["Clipboard Item 1", "Clipboard Item 2", "Another Item"]

def is_admin():
    """Check if the script is running with administrative privileges (Windows only)."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False




# --- The Monitor Function ---
def log_thread_stacks():
    while True:
        with open("thread_dump.log", "w") as f:  # "w" overwrites file every time (clean view)
            f.write(f"=== THREAD SNAPSHOT AT {time.strftime('%H:%M:%S')} ===\n")

            # Get all running threads
            for thread_id, frame in sys._current_frames().items():
                # Find the thread name if possible
                t_name = next((t.name for t in threading.enumerate() if t.ident == thread_id), "Unknown")

                f.write(f"\n--- Thread: {t_name} (ID: {thread_id}) ---\n")
                # Format the stack trace
                stack = traceback.format_stack(frame)
                f.write("".join(stack))

        time.sleep(2)  # Update every 2 seconds



def main():
    print("Starting Clipboard Manager...")

    # 1. Core objects
    event_bus = EventBus()
    history_manager = PlaceholderHistoryManager()  # replace later with real HistoryManager

    # 2. Start EventBus processing in a background thread
    event_bus_thread = threading.Thread(target=event_bus.start, name="event_bus",daemon=True)
    event_bus_thread.start()

    # --- Start the Monitor in Background ---
    monitor_thread = threading.Thread(target=log_thread_stacks,name="monitor_thread", daemon=True)
    monitor_thread.start()

    # --- YOUR MAIN PROGRAM SIMULATION ---

    # 3. Create and start HotkeyListener
    hotkey_listener = HotkeyListener(event_bus=event_bus)
    event_bus.start_hotkey_listener(hotkey_listener)

    # 4. Create GUI (Kivy app)
    clipboard_gui = ClipboardGUI(event_bus=event_bus, history_manager=history_manager)

    # 5. Subscribe GUI to hotkey event BEFORE running the app
    # HotkeyListener emits: event_bus.emit("hotkey_triggered", {"hotkey": "ctrl+v"})
    # So the GUI should expose a method like: on_hotkey_trigger(self, data)
    # event_bus.subscribe("hotkey_triggered", clipboard_gui.show_popup)
    # 6. Run the Kivy application (blocks main thread)
    clipboard_gui.run()


    # Optional: if you ever implement clean shutdown:
    # event_bus.stop()
    # hotkey_listener.stop()

    print("Clipboard Manager stopped.")


if __name__ == "__main__":
    system = platform.system()
    if system == "Darwin":
        print("Running on macOS. Please ensure the application has accessibility permissions.")
        main()
    elif system == "Windows":
        if is_admin():
            print("Running with administrative privileges on Windows.")
            main()
        else:
            print("This application may require administrative privileges to listen for global hotkeys.")
            print("Please restart the application as an administrator if hotkeys do not work.")
            sys.exit(1)
    else:
        # Linux / others
        main()
