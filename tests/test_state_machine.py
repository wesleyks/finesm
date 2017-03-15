from finesm import StateMachine, State


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

    @running.on_enter
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
