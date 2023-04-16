# mrtsubtitles
mrtsubtitles aims to provide near real-time transcription and translation of spoken language with the focus on theater plays. However, it can be used in any context.

## Table of content
- [Transcription and translation of scripted scenes](##Transcription and translation of scripted scenes)
- [Transcription and translation of improvised scenes / freely spoken text](##Transcription and translation of improvised scenes)
- [Representation of text to the audience](##Representation of text to the audience)
- [Actor / object tracking](##Actor / object tracking)
- [AR glasses](##AR glasses)
- [Limitations](##Limitations)

## Transcription and translation of scripted scenes
### How it works
For translation of a given script a [libreTranslate](https://github.com/LibreTranslate/LibreTranslate) api server is hosted. With [translater.py](translater.py) the script is being translated and the translation is saved to a file so it would be possible to correct mistakes.
For speech to text conversion [whisper.cpp](https://github.com/ggerganov/whisper.cpp) is used. Setting the flags `-t 8 --step 1000 --length 5000` makes whisper transcribe what is being said in almost real-time and consider what has been said shortly before to improve the translation on the go. When receiving new transcibed text [scriptmatcher.py](scriptmatcher.py) compares the text to all sentences in the script and chooses the one that is the closest by dividing the intersection of the sets of words of both pieces of text by the union of them. To get better results since the speech to text transcript isn't very accurate we doubled the this value. It is possible to prefer sentences that are close to the last used sentence in the script over those that have a bigger distance by adding a probability to the certainty value. The best values and curves for certainty threshold and probability are yet to be found. If the certainty is high enough the corresponding sentence of the script is being outputted and if wished also the matching translation. It is up to the user to process that text further and somehow present it to the audience.

### Usage 
#### Translation
```
python scriptmatcher.py alice.txt
```alice.txt can be any theater script (containing spoken text only for best performance) as a `.txt` file.

#### Transcription (and translation)
Clone [whisper.cpp](https://github.com/ggerganov/whisper.cpp) into a folder parallel to this one
```bash
cp stream-patched.cpp ../whisper.cpp/examples/stream/stream.cpp
cd ../whisper.cpp
make stream
cd -
./test.sh
```

## Transcription and translation of improvised scenes
### How it works
[whisper.cpp](https://github.com/ggerganov/whisper.cpp) transcribes what is being said in almost real-time and considers what has been said shortly before to improve the translation on the go. The output of the near live transcription can directly be translated into english with whisper. For other languages a [libreTranslate](https://github.com/LibreTranslate/LibreTranslate) api can be run and the output of whisper can be piped to an application that makes http requests to the running libreTranslate api. It is up to the user to process the received transcription and translation further.

### Usage
By the time of writing a http request can be made to a local libreTranslate api with default port `5000` by
```py
pload = {
        "q": "This is the text that I want to translate.", 
        "source": "en", 
        "target": "de"
        }
r = requests.post("http://127.0.0.1:5000/translate", pload)
obj = r.json()
translation = obj.get("translatedText")
print(translation)
```
Whisper can be used as described above without running `scriptmatcher.py` in [test.sh](test.sh).

## Representation of text to the audience
Thinking about how to provide the transcribed and translated text to the audience resulted in doing research in the field of [object tracking](##Actor / object tracking) and [AR glasses](##AR glasses).

## Actor / object tracking
### How it works
A software for detecting bright objects on dark background or dark objects on bright background that follows the detected object as it moves has been tested. Also, text has been attached to the object and was able to follow the moving object on a screen.

### Usage
*How to use the software and attach the text? Please provide a description.*

## AR glasses
The advantage of using AR glasses clearly is that everybody can choose their own language of subtitles as well as the possibility to show special effects such as hovering text over a person to each individual.
A difficulty is to provide AR glasses to the audiance and handling errors such as empty batteries or unexpected software behaviour.

*Please provide the results of further research and testing.*

## Limitations
As this project makes use of AI the results of transcriptions and translations won't always be correct and not every sentence in a provided script will be recognized. Please keep that in mind.
The parameter values and curves used in [scriptmatcher.py](scriptmatcher.py) are as of now only educated guesses. You might want to play around and find a better combination to improve accuracy.
