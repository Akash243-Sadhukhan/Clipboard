from queue import Queue
# import threading


class EventBus:
    def __init__(self):
        self.Queue = Queue()
        self.is_running = False
        self._subscribers = {}

    def subscribe(self, event_name, callback):

        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        self._subscribers[event_name].append(callback)

    def emit(self,event_name,data=None):
        self.Queue.put((event_name,data))

    def start(self):
        while True:
            event_name,data = self.Queue.get()
            if event_name in self._subscribers:
                for callback in self._subscribers[event_name]:
                    callback(data)
            self.Queue.task_done()

    
