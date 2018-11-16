import inspect


class State(object):
    EVENT_ENTER = 'enter'
    EVENT_UPDATE = 'update'
    EVENT_EXIT = 'exit'

    def __init__(self, default=None):
        self.default = default if default is not None else False
        self.__event_handlers = {}
        self.__message_handlers = {}

    def _on_event(self, event):
        def decorator(f):
            self.__event_handlers[event] = f.__name__
            return f
        return decorator

    def on_enter(self, *args):
        if len(args) == 1 and callable(args[0]):
            return self._on_event(self.EVENT_ENTER)(args[0])
        else:
            return self._on_event(self.EVENT_ENTER)

    def on_update(self, *args):
        if len(args) == 1 and callable(args[0]):
            return self._on_event(self.EVENT_UPDATE)(args[0])
        else:
            return self._on_event(self.EVENT_UPDATE)

    def on_exit(self, *args):
        if len(args) == 1 and callable(args[0]):
            return self._on_event(self.EVENT_EXIT)(args[0])
        else:
            return self._on_event(self.EVENT_EXIT)

    def on_message(self, message_name):
        def decorator(f):
            self.__message_handlers[message_name] = f.__name__
            return f
        return decorator

    def _handle_event(self, event, state_machine):
        if event in self.__event_handlers:
            function_name = self.__event_handlers[event]
            getattr(state_machine, function_name)()

    def handle_enter(self, state_machine):
        self._handle_event(self.EVENT_ENTER, state_machine)

    def handle_update(self, state_machine):
        self._handle_event(self.EVENT_UPDATE, state_machine)

    def handle_exit(self, state_machine):
        self._handle_event(self.EVENT_EXIT, state_machine)

    def handle_message(self, state_machine, message_name, *args, **kwargs):
        if message_name in self.__message_handlers:
            function_name = self.__message_handlers[message_name]
            getattr(state_machine, function_name)(*args, **kwargs)


class StateMachine(object):
    def __init__(self):
        states = inspect.getmembers(self, lambda m: isinstance(m, State))
        self.__states = dict(states)
        default_states = list(filter(lambda s: s[1].default, states))
        if len(default_states) != 1:
            raise Exception('Must have exactly 1 default state.')
        self.state = default_states[0][1]

    def send_message(self, message_name, *args, **kwargs):
        self.state.handle_message(self, message_name, *args, **kwargs)

    def update(self):
        self.state.handle_update(self)

    def set_state(self, state):
        changed = self.state != state
        if changed:
            self.state.handle_exit(self)
        self.state = state
        if changed:
            self.state.handle_enter(self)
