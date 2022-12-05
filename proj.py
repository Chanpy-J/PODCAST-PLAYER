# Tk_demo_02_buttons.py
# TKinter demo
# Play a sinusoid using Pyaudio. Use buttons to adjust the frequency.

from math import cos, pi 
import pyaudio, struct
import tkinter as Tk   	
import time
import wave

# Open wave file (mono)
input_wavefile = 'test.wav'
# input_wavefile = 'sin01_mono.wav'
# input_wavefile = 'sin01_stereo.wav'

wf          = wave.open( input_wavefile, 'rb')
RATE        = wf.getframerate()
WIDTH       = wf.getsampwidth()
LEN         = wf.getnframes() 
CHANNELS    = wf.getnchannels() 
NFRAME      = wf.getnframes()

def fun_pp():
  global play
  if(play):
    play = False
    print('pause')
  else:
    play = True
    print('Play')


def fun_quit():
  global CONTINUE
  print('Good bye')
  CONTINUE = False

# Define TK root
root = Tk.Tk()
root.geometry("300x250")
#content = Tk.Frame(root)
#frame = Tk.Frame(content, borderwidth=5, relief="ridge", width=200, height=100)
# Define widgets
t = Tk.DoubleVar()
t.set(0)
list_box = Tk.Listbox(root, bg = 'black', fg = 'green', width = 20)
slid = Tk.Scale(root,from_= 0, to = (NFRAME/RATE), orient = Tk.HORIZONTAL, variable = t )
B_pp = Tk.Button(root, text = 'play/pause', command = fun_pp)
B_quit = Tk.Button(root, text = 'Quit', command = fun_quit)

# Place widgets                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
list_box.pack(side = Tk.TOP)
slid.pack(side = Tk.TOP, fill =Tk.BOTH)
B_pp.pack(side = Tk.LEFT)
B_quit.pack(side = Tk.LEFT)

# Create Pyaudio object
p = pyaudio.PyAudio()
stream = p.open(
    format = pyaudio.paInt16,  
    channels = CHANNELS, 
    rate = RATE,
    input = False, 
    output = True,
    frames_per_buffer = 128)            
    # specify low frames_per_buffer to reduce latency

BLOCKLEN =int(RATE/10)
output_block = [0] * BLOCKLEN  # create 1D array  
CONTINUE = True
play = True
pre = 0

while CONTINUE:
  root.update()
  root.title('podcast player')
  if play:
    binary_data = wf.readframes(BLOCKLEN)
    input_block = struct.unpack('h' * BLOCKLEN, binary_data)
    if(pre+0.1 != t.get()):
      wf.setpos(int(t.get()*RATE))
    pre = t.get() 
    t.set(t.get() + 0.1)



    output_block = input_block



    binary_data = struct.pack('h' * BLOCKLEN, *output_block)

    binary_data = struct.pack('h' * BLOCKLEN, *output_block)   # 'h' for 16 bits
    stream.write(binary_data)

print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()
