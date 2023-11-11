class Keyboard_observable:
    def __init__(self):
        self._observers = []

    def subscribe(self, observer):
        self._observers.append(observer)

    def notify_observers(self, key, mouse_position):
        for observer in self._observers:
            observer.key_event(key, mouse_position)

    def unsubscribe(self, observer):
        self._observers.remove(observer)
