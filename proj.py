from math import cos, pi 
import pyaudio, struct
import tkinter as Tk    
import time
import wave
import os
import numpy as np

# Open wave file 
input_wavefile = './podcast/Mono.wav'

wf          = wave.open(input_wavefile, 'rb')
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

def clip16( x ):    
    # Clipping for 16 bits
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    else:
        x = x        
    return (x)

def replay():
  global podcast_path
  t.set(0)
  wf.setpos(0)
  sv.set(0)
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

def fun_sf():
  global sf
  if sf:
    sf = False
    print("smart fasten is off")
    pass
  else :
    sf = True
    print("smart fasten is on")
  pass

# Define TK root
root = Tk.Tk()
root.geometry("500x310")
gain = Tk.IntVar()
gain.set(10)
# Define widgets
t = Tk.DoubleVar()
t.set(0)
sv = Tk.DoubleVar()
sv.set(0)

list_box = Tk.Listbox(root, bg = 'black', fg = 'green', width = 20)
slid = Tk.Scale(root,from_= 0.0, to = (NFRAME / RATE), orient = Tk.HORIZONTAL, variable = t )
B_pp = Tk.Button(root, text = 'play/pause', command = fun_pp)
B_rp = Tk.Button(root, text = 'replay', command = replay)
B_quit = Tk.Button(root, text = 'Quit', command = fun_quit)
B_fasten = Tk.Button(root, text = "smart fasten", command = fun_sf)
S_gain = Tk.Scale(root, label = 'volumn', variable = gain, from_ = 0, to = 100, orient = Tk. HORIZONTAL)
L_timesave = Tk.Label(root , textvariable =sv)
L_tsl = Tk.Label(root, text = "save time")



# Place widgets                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
list_box.pack(side = Tk.TOP)
L_tsl.pack(side= Tk.TOP)
L_timesave.pack(side = Tk.TOP)
slid.pack(side = Tk.TOP, fill =Tk.BOTH)
B_pp.pack(side = Tk.LEFT)
B_rp.pack(side = Tk.LEFT)
B_quit.pack(side = Tk.LEFT)
B_fasten.pack(side = Tk.LEFT)

S_gain.pack(side = Tk.TOP)
           

BLOCKLEN =int(RATE/10)
output_block = [0] * BLOCKLEN  # create 1D array  
CONTINUE = True
play = True
sf = False
pre = 0

os.chdir("./podcast")
podcasts = os.listdir()
for pd in podcasts:
  if pd != ".DS_Store":
    list_box.insert('end', pd)

list_box.selection_set(0)

prev_p = "Mono.wav"

while CONTINUE:
  root.update()
  root.title('podcast player')
  
  currentPodcast = list_box.get('active')
  podcast_path = os.getcwd() + "/" + currentPodcast
  # print(currentPodcast)
  if currentPodcast != prev_p:
    t.set(0)
    sv.set(0)
    wf          = wave.open(podcast_path, 'rb')
    RATE        = wf.getframerate()
    WIDTH       = wf.getsampwidth()
    LEN         = wf.getnframes() 
    CHANNELS    = wf.getnchannels() 
    NFRAME      = wf.getnframes()
    BLOCKLEN = int(RATE / 10)
    output_block = [0] * BLOCKLEN  # create 1D array  

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

  
  if play :
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
      if not sf :
        skip = False 
      else :
        for x in range(freqbeg, freqend):
          if int(abs(X[x])) > 10000 :
            skip = False
            break
          pass

      if(pre + 0.1 != t.get()):
        wf.setpos(int(t.get() * RATE))
      pre = t.get() 
      t.set(t.get() + 0.1)

      if pre >= (NFRAME / RATE):
        play = False

      for i in range(0, len(input_block)):
        output_block[i] =int(clip16(input_block[i] * (gain.get() /10)))
      binary_data = struct.pack('h' * BLOCKLEN, *output_block)   # 'h' for 16 bits
      if not skip:
        stream.write(binary_data)
      else:
        sv.set(sv.get() + 0.1)
    else:
      binary_data = wf.readframes(BLOCKLEN)
      if len(binary_data) != BLOCKLEN * 2 * CHANNELS:
        play = False
        print("pause")
        continue


      skip = True
      input_block = struct.unpack('hh' * BLOCKLEN, binary_data)
      X = np.fft.fft(input_block)
      freqbeg = int(300/RATE*BLOCKLEN*CHANNELS)
      freqend = int(1500/RATE*BLOCKLEN*CHANNELS)
      for x in range(freqbeg, freqend):
        if not sf:
          skip = False
        if int(abs(X[x])) > 40000:
          #print(abs(X[x]))
          skip = False
          break
        pass
      
      if(pre + 0.1 != t.get()):
        wf.setpos(int(t.get() * RATE))
      pre = t.get() 
      t.set(t.get() + 0.1)

      if pre >= (NFRAME / RATE):
        play = False
  
      output_block = [0] * BLOCKLEN*CHANNELS
      for i in range(0, len(input_block)):
        output_block[i] =int(clip16(input_block[i] * (gain.get() /10)))

      binary_data = struct.pack('hh' * BLOCKLEN, *output_block)
      if not skip :
        stream.write(binary_data)
      else:
        sv.set(sv.get() + 0.1)

  else:
    time.sleep(0.1)

print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()
