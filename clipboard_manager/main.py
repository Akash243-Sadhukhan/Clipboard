
import threading
import subprocess
from core.hotkey_listener import  HotkeyListener
from core.event_bus import EventBus
from gui.app import SpotlightSearch



def main():
    _event_bus = EventBus()
    _hotkey_listener = HotkeyListener(_event_bus, hotkey="<ctrl>+v")

    def on_hotkey_trigger(_):
        try:
            subprocess.run(["open", "-a", "Spotlight"], check=True)
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Error launching Spotlight: {e}")

    _event_bus.subscribe("HOTKEY_TRIGGER", on_hotkey_trigger)
    event_bus_thread = threading.Thread(target=_event_bus.start)
    event_bus_thread.daemon = True
    event_bus_thread.start()
    _hotkey_listener.start()

    gui =SpotlightSearch()


    try:
        _hotkey_listener.join()
        gui.run()
    except KeyboardInterrupt:
        print("Stopping...")
        _hotkey_listener.stop()



if __name__ == "__main__":
    main()