# gamepad
A python abstraction for gamepads

## Usage
```python3
from gamepad import gamepad as gp

def a_button_pressed(val):
    # Buttons return 1 when pressed (and held) and a 0 when released
    if val == 1:
        print("A button pressed!")

c = gp.get_LogitechR710()

c.add_callback('A', a_button_pressed)

c.start()
```
