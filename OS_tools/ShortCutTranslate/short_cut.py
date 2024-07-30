import keyboard

def on_triggered():
    print("快捷键被触发")

keyboard.add_hotkey('ctrl+shift+a', on_triggered)

keyboard.wait('esc') 