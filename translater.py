import sys
#import math
#import re
import requests

OUTPATH = "german_transl.txt"

def main():
    script = []
    with open(sys.argv[1]) as infile:
        for line in infile:
            script.append(line.strip())
    langs = [] # Query available languages
    langpayload = requests.get("http://127.0.0.1:5000/languages").json()
    for entry in langpayload:
        langs.append(entry.get("code"))
    print(langs)
    for lang in langs:
        if lang==sys.argv[2]:
            continue
        with open(("."+lang+".").join(sys.argv[1].rsplit(".",1)),"w") as outfile:
            # write
            for line in script:
                if not line:
                    outfile.write("\n")
                    continue
                pload = {
                        "q": line,
                        "source": sys.argv[2],
                        "target": lang
                    }
                r = requests.post("http://127.0.0.1:5000/translate",pload).json()
                print(r)
                outfile.write(r.get("translatedText")+"\n")

if __name__=="__main__":
    sys.exit(main())
