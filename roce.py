import webbrowser
from pynput import keyboard

# The legendary URL
RICKROLL_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

def on_press(key):
    try:
        # Check if the alphanumeric key 'o' or 'O' is pressed
        if key.char == 'o' or key.char == 'O':
            webbrowser.open(RICKROLL_URL)
    except AttributeError:
        # This handles special keys (like Ctrl, Alt, etc.) so the script doesn't crash
        pass

def on_release(key):
    # Optional: Stop the script if you press the Escape key
    if key == keyboard.Key.esc:
        print("Prank mode deactivated.")
        return False

print("Listening for the letter 'O'... (Press ESC to stop)")

# Start the listener
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()