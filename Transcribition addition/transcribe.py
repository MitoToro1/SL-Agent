#speech to text lib
#some APIs

#Examples:
#Vosk - no internet, Eng and Rus
#Faster-Whisper multilingual, depends on the internet

#funcs: (* - optional)
#transcribe audio file

#imports:
try:
    from pathlib import Path
    from datetime import datetime

    import wave
    from vosk import Model, KaldiRecognizer
    import json

    import librosa
    import soundfile as sf
    import numpy as np

    import faster_whisper as FW

except Exception as e:
    print(f"-[!]- transcribe.py imports couldn't load!\nError:{e}")


#global vars
pathToMasterFolder = Path(__file__).parent
pathToDefaultTxtSave = pathToMasterFolder / 'Transcribitions of audio'
pathToDefaultConversionSave = pathToMasterFolder / 'Audios to transcribe'
pathToVoskModel = pathToMasterFolder / '' #ENTER MODEL NAME
#model recommendations:
#small - faster, bigger - better accuracy


#cusstom exceptions
class ConversionError(Exception):
    '''
    Couldn't convert file to needed format!
    '''
    


#funcs
def create_n_write_txt(whatToWrite, fileName, whereCreate=pathToDefaultTxtSave):
    '''
    Function for easy writing stuff and creating txt
    whereCreate mustn't include file name! 
    '''
    with open(whereCreate / fileName, 'w+') as f:
        f.write(whatToWrite)

def convert_to_wav(audioPath, toSavePath=None): #not tested, not done
    '''
    Function for converting various audio files into ".wav"
    Needed for vosk, since it accepts only wav files, while FW supports almost any.
    Can convert only FLAC/WAV/OGG/MP3
    '''
    if toSavePath is None:
        toSavePath = pathToDefaultConversionSave
    
    audio, sr = librosa.load(audioPath, sr=16000, mono=True)
    audio = (audio * 32767).astype(np.int16)

    sf.write(toSavePath, audio, 16000, subtype="PCM_16")
    print(f'---[] Converted {audioPath} to {toSavePath}')

    return toSavePath + ""


def transcribe_audio_by_vosk(audioPath) -> str:
    '''
    Function for transcribing audio file by using vosk lib,
    Used if no internet is available.
    Requiers only wav files!!!
    also requires local model for running.
    '''
    try:
        if audioPath[:-3] != 'wav': #if doens't meet requirement
            try:
                print("-[!]- Couldn't transcribe the file, it doesn't meet requrements of file format!\nFor alternative way of transcribing file needs to be .wav!\n Trying to convert...")
                audioPath = convert_to_wav(audioPath)
            except Exception as e: 
                print(f'-[!]- Error: {e}')
                raise ConversionError
        model = Model(pathToVoskModel)
        wf = wave.open(audioPath, 'rb')
        rec = KaldiRecognizer(model, wf.getframerate()) #Matches audio sample rate

        #Process audio:
        text = []
        while True:
            data = wf.readframes(4000) #Chunk size
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())
                if res.get("text"):
                    text.append(res['text'])

        final = json.loads(rec.FinalResult())
        if final.get('text'):
            text.append(final['text'])

        result = ' '.join(text)
        wf.close()
        return result
    except ConversionError as e:
        print(f"Couldn't transcribe the file :(\nError:{e}")
        return ':('    

def transcribe_audio_by_FW(audioPath) -> str:
    '''
    Function for transcribing audio file by using faster-whisper lib.
    supports almost any file
    '''
    model = FW.WhisperModel('base', device='cpu', compute_type='int8')
    #model may vary: tiny, base, small, medium, large-v3
    #device may vary: cpu OR cuda (which is GPU)

    #transcribing audio:
    segments, info = model.transcribe(audioPath, beam_size=5)
    print(f"--[] Detected language: {info.language}")
    
    for segment in segments:
        res += (f"[{segment.start:.2f}s - {segment.end:.2f}s]{segment.text}") + "\n"

    return res

def transcribe_audio(audioPath, whereToSave=None) -> str:
    '''
    Transcribe audio file and save text into txt file
    '''


    if whereToSave is None:
        whereToSave = pathToDefaultTxtSave
    
    res = ''
    try: 
        res = transcribe_audio_by_FW(audioPath)
    except Exception as e:
        print("-[!}- Couldn't transcribe {audioPath} audio!\nError:{e}\nTrying to use other methods...")
        res = transcribe_audio_by_vosk(audioPath)

    name = 'Transcribed Audio (' + str(datetime.today().date()) + '' + ')'
    
    
    create_n_write_txt(res, name, whereToSave)
    

def test():
    '''
    testing function
    '''

    print(transcribe_audio(1, 2))
    
test()