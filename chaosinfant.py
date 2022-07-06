import urllib.request,urllib.parse,time,wave,contextlib,cv2,moviepy.video.io.ImageSequenceClip,random,os,requests
from moviepy.editor import *
import numpy as np
from pydub import AudioSegment
from moviepy.editor import VideoFileClip, concatenate_videoclips
class Line():
    def __init__(self,who,what,where):
        self.who = who
        self.what = what
        self.where = where
class Script():
    def __init__(self,characters,scenes):
        self.characters = characters
        self.voice = characters[list(characters)[0]][0]
        self.character = list(characters)[0]
        self.scenes = scenes
        self.scenepath = scenes[list(scenes)[0]]
        self.scene = list(scenes)[0]
        self.lines = []
        self.script = "[SCENE: " + self.scene + "]\n"
        word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
        response = urllib.request.urlopen(word_site)
        txt = str(response.read())
        self.wordlist = txt.split("\\n")
    def setCharacter(self,character):
        self.voice = self.characters[character][0]
        self.character = character
    def addLine(self,line):
        self.line = line
        self.script += "[" + self.character + "]" + " " + self.line + "\n"
        self.lines.append(Line(self.character,self.line,self.scene))
    def changeScene(self,scene):
        self.scene = scene
        self.scenepath = self.scenes[scene]
        self.script += "[SCENE: " + self.scene + "]\n"
    def randomGenerateScript(self):
        for _ in range(random.randint(7,20)):
            newScene = random.choice(list(self.scenes))
            if (random.randint(0,2) == 0) and newScene != self.scene:
                self.changeScene(newScene)
            self.setCharacter(random.choice(list(self.characters)))
            currSentence = ""
            for _ in range(random.randint(2,6)):
                currSentence += (random.choice(self.wordlist) + " ")
            currSentence = currSentence[:-1]
            self.addLine(currSentence)
    def print(self):
        print(self.script[:-1])
    def generateWAV(self):
        combined = AudioSegment.empty()
        self.sceneLengths = []
        self.sceneOrder = []
        prevScene = ""
        currLen = 0
        for x in self.lines:
            if x.where == prevScene:
                newScene = 0
            else:
                newScene = 1
                prevScene = x.where
            while True:
                failed = 0
                try:
                    url = "https://tetyys.com/SAPI4/SAPI4?text=" + urllib.parse.quote(x.what) + "&voice=" + urllib.parse.quote(self.characters[x.who][0]) + "&pitch=169&speed=170"
                    with urllib.request.urlopen(url,timeout=15) as inp:
                        response = inp.read()
                    with open("voicelines/"+x.what+x.who+".wav","bw+") as File:
                        File.write(response)
                except urllib.error.HTTPError:
                    failed = 1
                if failed:
                    time.sleep(0.2)
                    pass
                else:
                    if newScene:
                        self.sceneLengths.append(0)
                        self.sceneOrder.append(x.where)
                    with contextlib.closing(wave.open("voicelines/"+x.what+x.who+".wav",'r')) as f:
                        frames = f.getnframes()
                        rate = f.getframerate()
                        duration = frames / float(rate)
                    self.sceneLengths[-1] += duration
                    audio = AudioSegment.from_file("voicelines/"+x.what+x.who+".wav", format="wav")
                    combined += audio
                    break
        file_handle = combined.export("output.mp3", format="mp3")
    def generateMP4(self):
        os.system("rm -f clips/*; rm -f voicelines/*")
        total = 0
        for x in self.sceneLengths:
            total += x
        toConcatenate = []
        for j,x in enumerate(self.sceneLengths):
            # write file named the order of the scene so eg first scene is 1.mp4 then 2.mp4
            clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip([self.scenes[self.sceneOrder[j]]],fps=10).set_duration(x)
            toConcatenate.append(clip)
        final_clip = concatenate_videoclips(toConcatenate)
        final_clip.write_videofile("prefinal.mp4", verbose=False, logger=None)
        clips = [VideoFileClip("prefinal.mp4")]
        for x in list(self.characters):
            clips.append(moviepy.video.io.ImageSequenceClip.ImageSequenceClip([self.characters[x][1]],fps=10).resize(1.5).set_position((random.uniform(0.2,0.7),random.uniform(0.2,0.7)),relative=True).set_duration(final_clip.duration))
        final = CompositeVideoClip(clips).set_audio(AudioFileClip("output.mp3"))
        final.write_videofile("final.mp4", verbose=False, logger=None)

def scriptReader(script,out):
    for x in script.split("\n"):
        if x:
            if x[-1] == "]":
                scene = x.replace('[','').replace(']','')
                out.changeScene(scene)
            else:
                character = x.split(" ")[0][1:].replace("]",'')
                out.setCharacter(character)
                out.addLine(x.split(']')[1][1:])

characters = {'Linus':['Sam','/home/stan/Documents/chaosinfantgoodman.png'],'Child':['Adult Male #2, American English (TruVoice)','/home/stan/Documents/charchaoschild.png']}
scenes = {'Store':'store.png','Blank':'white.png','Building':'building.png'}
script = Script(characters,scenes)
fileToOpen = "script.txt"
content = ""
with open(fileToOpen) as File:
    content = File.read()
scriptReader(content,script);
#script.randomGenerateScript()
script.print()
script.generateWAV()
script.generateMP4()
