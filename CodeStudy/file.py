import pyautogui as pag

print(__file__)
try:
    old_pos = pag.position()
    while True:
        new_pos = pag.position()
        if new_pos != old_pos:
            print(new_pos)
            old_pos = new_pos
except KeyboardInterrupt:
    print("exit")
