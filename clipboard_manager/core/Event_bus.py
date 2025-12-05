
from queue import Queue

class EventBus:
    def __init__(self):
        self.queue = Queue()
        self.is_running = False
        self._subscribers = {}
        print("[DEBUG] EventBus initialized and ready to process events.")

    def subscribe(self, event_name, callback):
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        self._subscribers[event_name].append(callback)
        self.print_events()

    def emit(self, event_name, data=None):
        """Thread-safe emit: enqueue the event."""
        self.queue.put((event_name, data))

    def start(self):
        """Blocking event loop. Run this in a background thread."""
        self.is_running = True
        while self.is_running:
            event_name, data = self.queue.get()
            if event_name in self._subscribers:
                for callback in self._subscribers[event_name]:
                    try:
                        callback(data)
                    except Exception as e:
                        print(f"[ERROR] EventBus callback error for '{event_name}': {e}")
            self.queue.task_done()

    def stop(self):
        """Signal the loop to stop."""
        self.is_running = False
        # Wake up the loop
        self.queue.put((None, None))


    def print_events(self):
        if not self._subscribers:
            print("[DEBUG] No subscribers registered.")
            return

        for event, callbacks in self._subscribers.items():
            print(f"[DEBUG] Event: {event} -> {len(callbacks)} subscriber(s)")
            for cb in callbacks:
                name = getattr(cb, "__qualname__", getattr(cb, "__name__", repr(cb)))
                module = getattr(cb, "__module__", None)
                if module:
                    print(f"  - {module}.{name}")
                else:
                    print(f"  - {name}")

    def start_hotkey_listener(self, hotkey_listener):
        """Start the HotkeyListener thread."""
        print("[DEBUG] Starting HotkeyListener thread via EventBus...")
        hotkey_listener.start()
        print("[DEBUG] HotkeyListener thread started in event bus. ")