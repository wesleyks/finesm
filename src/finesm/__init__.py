import inspect
from collections.abc import Callable
from typing import TypeVar, overload


F = TypeVar("F", bound=Callable[..., object])


class State:
    EVENT_ENTER = "enter"
    EVENT_UPDATE = "update"
    EVENT_EXIT = "exit"

    def __init__(self, default: bool | None = None) -> None:
        self.default: bool = default if default is not None else False
        self.__event_handlers: dict[str, str] = {}
        self.__message_handlers: dict[str, str] = {}

    def _on_event(self, event: str) -> Callable[[F], F]:
        def decorator(function: F) -> F:
            self.__event_handlers[event] = function.__name__
            return function

        return decorator

    @overload
    def on_enter(self, function: F, /) -> F: ...

    @overload
    def on_enter(self) -> Callable[[F], F]: ...

    def on_enter(self, function: F | None = None) -> F | Callable[[F], F]:
        if function is not None:
            return self._on_event(self.EVENT_ENTER)(function)
        return self._on_event(self.EVENT_ENTER)

    @overload
    def on_update(self, function: F, /) -> F: ...

    @overload
    def on_update(self) -> Callable[[F], F]: ...

    def on_update(self, function: F | None = None) -> F | Callable[[F], F]:
        if function is not None:
            return self._on_event(self.EVENT_UPDATE)(function)
        return self._on_event(self.EVENT_UPDATE)

    @overload
    def on_exit(self, function: F, /) -> F: ...

    @overload
    def on_exit(self) -> Callable[[F], F]: ...

    def on_exit(self, function: F | None = None) -> F | Callable[[F], F]:
        if function is not None:
            return self._on_event(self.EVENT_EXIT)(function)
        return self._on_event(self.EVENT_EXIT)

    def on_message(self, message_name: str) -> Callable[[F], F]:
        def decorator(function: F) -> F:
            self.__message_handlers[message_name] = function.__name__
            return function

        return decorator

    def _handle_event(self, event: str, state_machine: "StateMachine") -> None:
        if event in self.__event_handlers:
            function_name = self.__event_handlers[event]
            getattr(state_machine, function_name)()

    def handle_enter(self, state_machine: "StateMachine") -> None:
        self._handle_event(self.EVENT_ENTER, state_machine)

    def handle_update(self, state_machine: "StateMachine") -> None:
        self._handle_event(self.EVENT_UPDATE, state_machine)

    def handle_exit(self, state_machine: "StateMachine") -> None:
        self._handle_event(self.EVENT_EXIT, state_machine)

    def handle_message(
        self,
        state_machine: "StateMachine",
        message_name: str,
        *args: object,
        **kwargs: object,
    ) -> None:
        if message_name in self.__message_handlers:
            function_name = self.__message_handlers[message_name]
            getattr(state_machine, function_name)(*args, **kwargs)


class StateMachine:
    def __init__(self) -> None:
        states = [
            (name, state)
            for name, state in inspect.getmembers(self)
            if isinstance(state, State)
        ]
        self.__states: dict[str, State] = dict(states)
        default_states = [state for _, state in states if state.default]
        if len(default_states) != 1:
            raise Exception("Must have exactly 1 default state.")
        self.state: State = default_states[0]

    def send_message(
        self, message_name: str, *args: object, **kwargs: object
    ) -> None:
        self.state.handle_message(self, message_name, *args, **kwargs)

    def update(self) -> None:
        self.state.handle_update(self)

    def set_state(self, state: State) -> None:
        changed = self.state != state
        if changed:
            self.state.handle_exit(self)
        self.state = state
        if changed:
            self.state.handle_enter(self)
