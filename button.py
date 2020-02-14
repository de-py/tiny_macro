from pynput import keyboard
from datetime import datetime
import pyaudio
import wave
import _thread

def audio():
    CHUNK = 1

    wf = wave.open('shortest.wav', 'rb')

    # instantiate PyAudio (1)
    p = pyaudio.PyAudio()

    # open stream (2)
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # read data
    data = wf.readframes(CHUNK)

    # play stream (3)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)

    # stop stream (4)
    stream.stop_stream()
    stream.close()

    # close PyAudio (5)
    p.terminate()
    

# The key combination to check
COMBINATION_dt = {keyboard.KeyCode.from_char('d'), keyboard.KeyCode.from_char('t')}
COMBINATION_esc = {keyboard.Key.esc, keyboard.Key.backspace}
k = keyboard.Controller()

# The currently active modifiers
current = set()

current2 = set()
def on_press(key):
    if key in COMBINATION_dt:
        current.add(key)
        if all(k in current for k in COMBINATION_dt):
            _thread.start_new_thread( audio, () )
            k.press(keyboard.Key.backspace)
            k.press(keyboard.Key.backspace)
            now = datetime.now()
            first = (now.strftime("%Y-%m-%d %H"))
            second = (now.strftime("%M"))
            k.type(first)
            with k.pressed(keyboard.Key.shift):
                k.press(';')
                k.release(';')
            k.type(second)
            k.press(keyboard.Key.tab)
        
    # current.clear()

    if key in COMBINATION_esc:
        current2.add(key)
        if all(k in current2 for k in COMBINATION_esc):
            listener.stop()
    
    # current2.clear()
    # if key == keyboard.Key.esc:
        
    #     listener.stop()


def on_release(key):
    try:
        current.clear()
        current2.clear()
    except KeyError:
        pass


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

