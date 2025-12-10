import threading

class HistoryManager:
    def __init__(self, event_bus, max_history=50):
        # super().__init__(daemon=True)
        self.event_bus = event_bus
        self.max_history = max_history
        self.history = []

        self.event_bus.subscribe("NEW_CLIPBOARD_DATA", self.add_to_history)

    def add_to_history(self, data):
        if data not in self.history:
            self.history.insert(0, data)
            if len(self.history) > self.max_history:
                self.history.pop()

    def get_history(self):
        return self.history.copy()