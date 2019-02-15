import threading

# These are variables shared between the thread

condition = threading.Condition()

BOARD_STATE = [ 1, 2, 3]
DONE = True
