from gpiozero import Motor
import curses

lmotor = Motor(forward=16, backward=17)
rmotor = Motor(forward=18, backward=13)

def left():
#    print('Left ...')
    lmotor.backward()
    rmotor.forward()

def right():
#    print('Right ...')
    lmotor.forward()
    rmotor.backward()

def forward():
#    print('Forwarding ...')
    lmotor.forward()
    rmotor.forward()

def reverse():
#    print('Reversing ...')
    lmotor.backward()
    rmotor.backward()

def stop():
#    print('Stopping ...')
    lmotor.stop()
    rmotor.stop()

actions = {
    curses.KEY_UP:    forward,
    curses.KEY_DOWN:  reverse,
    curses.KEY_LEFT:  left,
    curses.KEY_RIGHT: right,
}

def main(window):
    next_key = None
    while True:
        curses.halfdelay(1)
        if next_key is None:
            key = window.getch()
        else:
            key = next_key
            next_key = None
        if key != -1:
            # KEY PRESSED
            curses.halfdelay(3)
            action = actions.get(key)
            if action is not None:
                action()
            next_key = key
            while next_key == key:
                next_key = window.getch()
            # KEY RELEASED
            stop()

curses.wrapper(main)