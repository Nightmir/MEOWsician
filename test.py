import pyaudio
import wave
import numpy as np
from pygame import *

class Note(object):
    def __init__(self,note,length):
        self.note=note
        self.length=type

        self.px=0
        self.py=0
        self.active=False

    def fall(self):
        self.py+=1
        if self.py>450:
            self.active=True

    quarter = 0
    eighth =1
    rest = 2
def record():# returns a list of frequencies that were recorded
    # open stream object as input & output
    stream = p.open(format=FORMAT,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    output=True,
                    frames_per_buffer=chunk)


    frames = []
    #print("Recording...")
    for i in range(int(44100 / chunk /20)):
        data = stream.read(chunk)
        frames.append(data)
    #print("Finished recording.")

    # stop and close stream
    stream.stop_stream()
    stream.close()
    # terminate pyaudio object
    ##p.terminate()
    # save audio file
    # open the file in 'write bytes' mode
    wf = wave.open(filename, "wb")
    # set the channels
    wf.setnchannels(channels)
    # set the sample format
    wf.setsampwidth(p.get_sample_size(FORMAT))
    # set the sample rate
    wf.setframerate(sample_rate)
    # write the frames as bytes
    wf.writeframes(b"".join(frames))
    # close the file
    return b"".join(frames)
def drawScreen(background,mode):
    #screen.blit(background,(0,0))
    draw.rect(screen,(127,127,127),(0,0,800,600))
    print(mode)
    if mode=='tuner':
        ##drawing piano
        draw.rect(screen,WHITE,(0,450,800,150))
        for i in range(8):
            draw.rect(screen,BLACK,(i*(100),450,100,150),2)
        for i in range(2):
            draw.rect(screen,BLACK,(75+i*100,450,50,100))
        for i in range(3,6,1):
            draw.rect(screen,BLACK,(75+i*100,450,50,100))



    display.flip()
    

def findNote(frequencyList,freqIn):#finds the corresponding note from the freqency entered, and returns as a String
    lastVal = 8000
    for frequency in frequencyList:
        if freqIn<int(round(float(frequency[1]))) and freqIn>lastVal:
            return frequency[0][0]
        else:
            lastVal = int(float(frequency[1]))
    return "Your music sounds like Cardi B"

def TUNER(song):
    noteList=[]
    music=loadNotes(str(songs[song])) 
    for i in range(len(music)):
        note=Note(music[i][0],music[i][1])
        noteList.append(note)
    running=True
    fList=loadNotes('frequencies.txt')
    while running:
        for evt in event.get():
            if evt.type==K_RETURN:
                running=False
            if evt.type==QUIT:
                running=False
                       
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()
        keys = key.get_pressed()


        drawScreen(None,'tuner')

        for i in range(len(music)):
            noteList[i].fall()
            if noteList[i].active:
                testNote()
        freq = findFreq(fList)
        note = findNote(fList,freq)
        print(note)


def playAudio():
    # read data in chunks
    wf=wave.open(filename,'rb')
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    
    data = wf.readframes(chunk)

    # writing to the stream (playing audio)
    while data:
        stream.write(data)
        data = wf.readframes(chunk)


    wf.close()

def findFreq(frequencyList,dataIn):#returns an int with the current frequency going into the mic
    # open up a wave
    wf = wave.open("filename.wav", 'rb')
    swidth = wf.getsampwidth()
    RATE = wf.getframerate()
    # use a Blackman window
    window = np.blackman(chunk)
    # open stream
    p = pyaudio.PyAudio()
    stream = p.open(format =
                    p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = RATE,
                    output = True)

    # read some data
    data = wf.readframes(chunk)
    # play stream and find the frequency of each chunk
    while len(data) == chunk*swidth:
        # write data out to the audio stream
        #stream.write(data)
        # unpack the data and times by the hamming window
        indata = np.array(wave.struct.unpack("%dh"%(len(data)/swidth),data))*window
        # Take the fft and square each value
        fftData=abs(np.fft.rfft(indata))**2
        # find the maximum
        which = fftData[1:].argmax() + 1
        # use quadratic interpolation around the max
        if which != len(fftData)-1:
            y0,y1,y2 = np.log(fftData[which-1:which+2:])
            x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
            # find the frequency and output it
            thefreq = (which+x1)*RATE/chunk
            #print ("The freq is %f Hz." % (thefreq))
        else:
            thefreq = which*RATE/chunk
        return thefreq
        # read some more data
        data = wf.readframes(chunk)

def loop(count):
    if count>0:
        record()
        findFreq()
        loop(count-1)
    else:
        return False
def loadNotes(file):
    data=[]
    with open(file) as f:
        content = f.readlines()
    for line in content:
        space=line.find(' ')
        name=line[0:space]
        frequency=line[space+1:-1]
        data.append([name,frequency])
    return data

# the file name output you want to record into
filename = "filename.wav"
# set the chunk size of 1024 samples
chunk = 1024
# sample format
FORMAT = pyaudio.paInt16
# mono, change to 2 if you want stereo
channels = 1
# 44100 samples per second
sample_rate = 44100
record_seconds = 1
# initialize PyAudio object
p = pyaudio.PyAudio()



width,height=800,600
screen=display.set_mode((width,height))
RED=(255,0,0)
GREY=(127,127,127)
BLACK=(0,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
YELLOW=(255,255,0)
WHITE=(255,255,255)


songs=['songs/0.txt','Mary had a Little Clam','C Major']


TUNER(0)
drawScreen(0,'tuner')