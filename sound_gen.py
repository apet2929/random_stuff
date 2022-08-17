import math        #import needed modules
import pyaudio     #sudo apt-get install python-pyaudio
from enum import Enum
import os

class Note(Enum):
    A_0 = 27.5
    A_SHARP_0 = 29.1352
    B_0 = 30.8677
    C_1 = 32.7032
    C_SHARP_1 = 34.6478
    G_3 = 195.998
    F_3 = 174.614
    D_4 = 293.665
    C_4 = 261.626
    C_6 = 1046.5
    C_8 = 4186.01

def sin_wave(frequency: Note, time):
    # a = (time * frequency.value) / BITRATE
    # b = math.pi * 4
    # c = math.sin(a * b)
    # notes.append(int(c*127)+128)
    # !y=Asin(2πfx+θ)
    a = 127
    y = int(a * math.sin(2 * math.pi * frequency.value * time))
    y = y * -1
    y += 128
    notes.append(y)
    # notes.append(
    #     int(
    #         (math.sin(
    #             4 * math.pi*
    #             time / (BITRATE/frequency.value)
    #             )
    #         *127))
    #     +128
    #     )

def sign(num):
    if num > 0: return 1
    elif num < 0: return -1
    return 0

def square_wave(frequency: Note, time):
    notes.append(sign((math.sin(4 * math.pi * time / (BITRATE/frequency.value))) * 127) + 128)

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

PyAudio = pyaudio.PyAudio     #initialize pyaudio

#See https://en.wikipedia.org/wiki/Bit_rate#Audio
BITRATE = 12800    #number of frames per second/frameset.      

FREQUENCY = 261.63     #Hz, waves per second, 261.63=C4-note.
LENGTH = 1     #seconds to play sound

if FREQUENCY > BITRATE:
    BITRATE = FREQUENCY+100

NUMBEROFFRAMES = int(BITRATE * LENGTH)
RESTFRAMES = NUMBEROFFRAMES % BITRATE
WAVEDATA = ''    
WAVE_INTS = []
notes = []

#generating wawes
for x in range(NUMBEROFFRAMES):
    # note1 = play_note(Note.C_8.value, x)
    # note2 = play_note(Note.C_SHARP_4.value, x)
    
    # square_wave(Note.C_8.value, x)
    sin_wave(Note.C_4, x)
    # sin_wave(Note.C_SHARP_4, x)
    # square_wave(Note.C_SHARP_4.value, x)
    # sin_wave(Note.D_4.value, x)

for note in notes:
    WAVEDATA += chr(note)
    WAVE_INTS.append(note)
    # f_note = int(f_note/len(notes))
    # # print(note1) 
    # WAVEDATA = WAVEDATA + chr(f_note)

for x in range(RESTFRAMES): 
    WAVEDATA = WAVEDATA+chr(128)

p = PyAudio()
stream = p.open(format = p.get_format_from_width(1), 
                channels = 1, 
                rate = BITRATE, 
                output = True)
# print("")
# print(WAVEDATA)
# print("")

nums_str = ""
f = open(find("file.txt", "assets"), "w")
for num in WAVE_INTS:
    nums_str += str(num) + " "
f.write(nums_str)
f.close()

stream.write(WAVEDATA)
stream.stop_stream()
stream.close()
p.terminate()
