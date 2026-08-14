import pytest

from finesm import State, StateMachine


class SimpleStateMachine(StateMachine):
    waiting = State(default=True)
    running = State()

    def __init__(self):
        super(SimpleStateMachine, self).__init__()
        self.foo = False
        self.bar = False
        self.updoot = 0

    @waiting.on_message('start')
    def waiting_start(self):
        self.set_state(self.running)

    @waiting.on_exit
    def waiting_exit(self):
        self.foo = True

    @running.on_enter()
    def running_enter(self):
        self.bar = True

    @running.on_update
    def runnin_update(self):
        self.updoot += 1


def test_state_machine():
    state_machine = SimpleStateMachine()

    assert state_machine.state == SimpleStateMachine.waiting
    assert state_machine.foo is False
    assert state_machine.bar is False

    state_machine.update()

    assert state_machine.updoot == 0

    state_machine.send_message('start')

    assert state_machine.foo is True
    assert state_machine.bar is True
    assert state_machine.state == SimpleStateMachine.running

    state_machine.update()
    state_machine.update()

    assert state_machine.updoot == 2


class NoDefaultStateMachine(StateMachine):
    waiting = State()


class MultipleDefaultStatesStateMachine(StateMachine):
    waiting = State(default=True)
    running = State(default=True)


@pytest.mark.parametrize(
    "state_machine_type",
    [NoDefaultStateMachine, MultipleDefaultStatesStateMachine],
)
def test_state_machine_requires_exactly_one_default_state(state_machine_type):
    with pytest.raises(Exception, match="Must have exactly 1 default state."):
        state_machine_type()


class SelfTransitionStateMachine(StateMachine):
    waiting = State(default=True)

    def __init__(self):
        super(SelfTransitionStateMachine, self).__init__()
        self.events = []

    @waiting.on_enter
    def waiting_enter(self):
        self.events.append("enter")

    @waiting.on_exit
    def waiting_exit(self):
        self.events.append("exit")


def test_self_transition_is_a_no_op():
    state_machine = SelfTransitionStateMachine()

    state_machine.set_state(state_machine.state)

    assert state_machine.state == SelfTransitionStateMachine.waiting
    assert state_machine.events == []


class MessageStateMachine(StateMachine):
    waiting = State(default=True)

    def __init__(self):
        super(MessageStateMachine, self).__init__()
        self.received = None

    @waiting.on_message("record")
    def waiting_record(self, *args, **kwargs):
        self.received = args, kwargs


def test_unknown_message_is_ignored():
    state_machine = MessageStateMachine()

    result = state_machine.send_message("unknown")

    assert result is None
    assert state_machine.state == MessageStateMachine.waiting
    assert state_machine.received is None


def test_message_handler_receives_arguments():
    state_machine = MessageStateMachine()

    state_machine.send_message("record", 1, "two", enabled=True)

    assert state_machine.received == ((1, "two"), {"enabled": True})
