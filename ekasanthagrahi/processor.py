from pydub import AudioSegment 
import speech_recognition as sr 
audio = AudioSegment.from_wav("recording.wav") 
n = len(audio) 
counter = 1
fh = open("recognized.txt", "w+") 
interval = 60 * 1000
overlap = 1.5 * 1000
start = 0
end = 0
flag = 0
for i in range(0, 2 * n, interval):
    if i == 0: 
        start = 0
        end = interval 
    else: 
        start = end - overlap 
        end = start + interval  
    if end >= n: 
        end = n 
        flag = 1
    chunk = audio[start:end] 
    filename = 'chunk'+str(counter)+'.wav'
    chunk.export(filename, format ="wav") 
    print("Processing chunk "+str(counter)+". Start = "+str(start)+" end = "+str(end))
    counter = counter + 1
    r = sr.Recognizer() 
    with sr.AudioFile(filename) as source: 
        audio_listened = r.listen(source) 
    try:     
        rec = r.recognize_google(audio_listened) 
        fh.write(rec+" ") 
    except sr.UnknownValueError: 
        print("Could not understand audio") 
    except sr.RequestError as e: 
        print("Could not request results.") 
    if flag == 1: 
        fh.close() 
        break