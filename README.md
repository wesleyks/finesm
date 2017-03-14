# fine_sm [![Build Status](https://travis-ci.org/wesleyks/fine_sm.svg?branch=master)](https://travis-ci.org/wesleyks/fine_sm) [![Coverage Status](https://coveralls.io/repos/github/wesleyks/fine_sm/badge.svg?branch=master)](https://coveralls.io/github/wesleyks/fine_sm?branch=master)

## Installation

`pip install fine_sm`

## Usage

```python
from fine_sm import Stat, StateMachine

class MyStateMachine(StateMachine):
    stop = State(default=True)
    go = State()

    @stop.on_message('switch')
    def stop_switch(self):
        self.set_state(go)

    @stop.on_exit
    def stop_exit(self):
        print('exiting stop state')

    @go.on_enter
    def go_enter(self):
        print('entering go state')

    @go.on_update
    def go_update(self):
        print('tick')


sm = MyStateMachine()
sm.state  # stop
sm.update()  #
sm.send_message('switch')  # exiting stop state
                           # entering go state
sm.update()  # tick

```
