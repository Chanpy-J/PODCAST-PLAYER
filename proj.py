from math import cos, pi 
import pyaudio, struct
import tkinter as Tk    
import time
import wave
import os
import numpy as np

# Open wave file 
input_wavefile = './podcast/test2.wav'

wf          = wave.open( input_wavefile, 'rb')
RATE        = wf.getframerate()
WIDTH       = wf.getsampwidth()
LEN         = wf.getnframes() 
CHANNELS    = wf.getnchannels() 
NFRAME      = wf.getnframes()

# Create Pyaudio object
p = pyaudio.PyAudio()
stream = p.open(
    format = pyaudio.paInt16,  
    channels = CHANNELS, 
    rate = RATE,
    input = False, 
    output = True,
    frames_per_buffer = 128) 

def replay():
  global podcast_path
  t.set(0)
  wf          = wave.open(podcast_path, 'rb')
  RATE        = wf.getframerate()
  WIDTH       = wf.getsampwidth()
  LEN         = wf.getnframes() 
  CHANNELS    = wf.getnchannels() 
  NFRAME      = wf.getnframes()
  BLOCKLEN = int(RATE / 10)

  slid.configure(to = NFRAME / RATE)

  p = pyaudio.PyAudio()
  stream = p.open(
      format = pyaudio.paInt16,  
      channels = CHANNELS, 
      rate = RATE,
      input = False, 
      output = True,
      frames_per_buffer = 128)
  play = True


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

# Define widgets
t = Tk.DoubleVar()
t.set(0)
list_box = Tk.Listbox(root, bg = 'black', fg = 'green', width = 20)
slid = Tk.Scale(root,from_= 0.0, to = (NFRAME / RATE), orient = Tk.HORIZONTAL, variable = t )
B_pp = Tk.Button(root, text = 'play/pause', command = fun_pp)
B_rp = Tk.Button(root, text = 'replay', command = replay)
B_quit = Tk.Button(root, text = 'Quit', command = fun_quit)

# Place widgets                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
list_box.pack(side = Tk.TOP)
slid.pack(side = Tk.TOP, fill =Tk.BOTH)
B_pp.pack(side = Tk.LEFT)
B_rp.pack(side = Tk.LEFT)
B_quit.pack(side = Tk.LEFT)
           

BLOCKLEN =int(RATE/10)
output_block = [0] * BLOCKLEN  # create 1D array  
CONTINUE = True
play = True
pre = 0

os.chdir("./podcast")
podcasts = os.listdir()
for p in podcasts:
  if p != ".DS_Store":
    list_box.insert('end', p)

list_box.selection_set(0)

prev_p = "test2.wav"
#binary_data = wf.readframes(BLOCKLEN)



# while(1):
#   list_box.selection_clear(0, 'end')
#   currentPodcast = list_box.get('active')
while CONTINUE:
  root.update()
  root.title('podcast player')
  
  currentPodcast = list_box.get('active')
  podcast_path = os.getcwd() + "/" + currentPodcast
  print(currentPodcast)

  
  if play :
    if currentPodcast != prev_p:
      t.set(0)
      wf          = wave.open(podcast_path, 'rb')
      RATE        = wf.getframerate()
      WIDTH       = wf.getsampwidth()
      LEN         = wf.getnframes() 
      CHANNELS    = wf.getnchannels() 
      NFRAME      = wf.getnframes()
      BLOCKLEN = int(RATE / 10)

      slid.configure(to = NFRAME / RATE)

      p = pyaudio.PyAudio()
      stream = p.open(
          format = pyaudio.paInt16,  
          channels = CHANNELS, 
          rate = RATE,
          input = False, 
          output = True,
          frames_per_buffer = 128)
      prev_p = currentPodcast

    
    if CHANNELS == 1:
      binary_data = wf.readframes(BLOCKLEN)
      if len(binary_data) != BLOCKLEN * 2:
        play = False
        print("pause")
        continue

      
      skip = True
      input_block = struct.unpack('h' * BLOCKLEN, binary_data)
      X = np.fft.fft(input_block)
      freqbeg = int(300/RATE*BLOCKLEN)
      freqend = int(1500/RATE*BLOCKLEN)
      for x in range(freqbeg, freqend):
        if int(abs(X[x])) > 35000:
          print(X[x])
          skip = False
          break
        pass


      if(pre + 0.1 != t.get()):
        wf.setpos(int(t.get() * RATE))
      pre = t.get() 
      t.set(t.get() + 0.1)

      if pre >= (NFRAME / RATE):
        play = False
        CONTINUE = False


      output_block = input_block

      binary_data = struct.pack('h' * BLOCKLEN, *output_block)   # 'h' for 16 bits
      print(skip)
      if not skip :
        stream.write(binary_data)
    else:
      binary_data = wf.readframes(BLOCKLEN)
      if len(binary_data) != BLOCKLEN * 2 * CHANNELS:
        play = False
        print("pause")
        continue


      skip = False
      input_block = struct.unpack('hh' * BLOCKLEN, binary_data)
      X = np.fft.fft(input_block)
      #print(len(X))#8820



      if(pre + 0.1 != t.get()):
        wf.setpos(int(t.get() * RATE))
      pre = t.get() 
      t.set(t.get() + 0.1)

      if pre >= (NFRAME / RATE):
        play = False
        CONTINUE = False

      output_block = input_block

      binary_data = struct.pack('hh' * BLOCKLEN, *output_block)
      stream.write(binary_data)

print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()
