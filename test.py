from pygame import *
import pyaudio
import wave
import numpy as np
from math import*

font.init()

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
    for i in range(int(44100 / chunk /42)):
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

def drawScreen(background,mode,freq,sel):
    if mode=='rhythm':
        ##drawing piano
        print('RHY')
        draw.rect(screen,(50,50,50),(0,0,800,600))
        draw.rect(screen,WHITE,(0,450,800,150))
        for i in range(8):
            draw.rect(screen,BLACK,(i*(100),450,100,150),2)
        for i in range(2):
            draw.rect(screen,BLACK,(75+i*100,450,50,100))
        for i in range(3,6,1):
            draw.rect(screen,BLACK,(75+i*100,450,50,100))
    elif mode=='tuner':
        print('TUNA')
        note=freq
        ##drawing tuner
        noteWord=Text(note,50,WHITE,255)
        draw.rect(screen,(50,50,50),(0,0,800,600))
        draw.circle(screen,WHITE,(400,400),100,5)
        draw.rect(screen,BLACK,(180,150,440,100))
        for i in range(10):
            draw.line(screen,WHITE,(220+i*40,150),(220+i*40,250))
        ##blit
        x,y=center(noteWord,400,400)
        screen.blit(noteWord,(x,y))
    elif mode=='menu':
        print('MENU')
        screen.blit(titleImage,(0,0))
        tuner=Text('Tuner',50,WHITE,255)
        rhythm=Text('Rhythm',50,WHITE,255)
        choose=Text('Song Choice',50,WHITE,255)
        screen.blit(tuner,(50,300))
        screen.blit(rhythm,(50,375))
        screen.blit(choose,(50,450))
        draw.circle(screen,YELLOW,(25,325+sel*75),25)


    elif mode=='choose':
        print('CHOOSE')
        draw.rect(screen,(50,50,50),(0,0,800,600))
        
    display.flip()

def Text(txt,size,col,alpha):
    Font=font.SysFont('Arial',size)
    fontPic=Font.render(str(txt), True, col)
    alphaFont=Surface(fontPic.get_size(),SRCALPHA)
    alphaFont.fill((255,255,255,alpha))
    fontPic.blit(alphaFont,(0,0),special_flags=BLEND_RGBA_MULT)
    return fontPic

def center(pic,x,y):
    w,h=pic.get_size()
    x-=w/2
    y-=h/2
    return x,y

def findNote(frequencyList,freqIn):#finds the corresponding note from the freqency entered, and returns as a String
    lastNote = ["?","8000.1"]
    note =0
    freq = 1
    logIn = log2(freqIn)
    for frequency in frequencyList:
        lastLog = log2( float(lastNote[freq]))
        currentLog = log2(float(frequency[freq]))
        if freqIn<int(round(float(frequency[freq]))) and freqIn>float(lastNote[freq]):#in between the last and current value
            if logIn-lastLog>currentLog-logIn:#closer to current value
                return frequency[note]
            else:
                return lastNote[note]
        else:
            lastNote = frequency
    return "Your music sounds like Cardi B"


def RHYTHM(song):
    freq=''
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


        drawScreen(None,'rhythym',freq,0)

        for i in range(len(music)):
            noteList[i].fall()
            if noteList[i].active:
                testNote()
        data = record()
        freq = findFreq(fList,data)
        note = findNote(fList,freq)
        print(note)

def TUNER():
    running=True
    freq=''
    fList=loadNotes('frequencies.txt')
    while running:
        for evt in event.get():
            if evt.type==KEYDOWN:
                if evt.key==K_ESCAPE:
                    running=False
            if evt.type==QUIT:
                running=False
                       
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()
        keys = key.get_pressed()

        
        data = record()
        freq = findFreq(fList,data)
        note = findNote(fList,freq)
        drawScreen(None,'tuner',freq,0)
        print(note)

def CHOOSE():
    running=True
    selection=0
    while running:
        for evt in event.get():
            if evt.type==KEYDOWN:
                if evt.key==K_ESCAPE:
                    running=False
                if evt.key==K_LEFT:
                    selection-=1
                if evt.key==K_RIGHT:
                    selection+=1
                if evt.key==K_RETURN:
                    sel=True
                if selection<0:
                    selection=1
                elif selection>3:
                    selection=0
            if evt.type==QUIT:
                quit()

        keys = key.get_pressed()

        drawScreen(None,'choose',0,selection)
        

def MENU():
    running=True
    selection=0
    sel=False
    song=0
    while running:
        for evt in event.get():
            if evt.type==KEYDOWN:
                if evt.key==K_ESCAPE:
                    running=False
                if evt.key==K_LEFT:
                    selection-=1
                if evt.key==K_RIGHT:
                    selection+=1
                if evt.key==K_RETURN:
                    sel=True
                if selection<0:
                    selection=1
                elif selection>3:
                    selection=0
            if evt.type==QUIT:
                quit()

        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()
        keys = key.get_pressed()

        drawScreen(None,'menu',0,selection)
        if sel:
            sel=False
            if selection==0:
                TUNER()
            if selection==1:
                RHYTHM(song)
            else:
                song=CHOOSE() 


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

titleImage=image.load('title.png').convert()

songs=['songs/0.txt','Mary had a Little Clam','C Major']


#TUNER()
#drawScreen(0,'tuner')
MENU()

quit()