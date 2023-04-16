import sys
import math
import re
import requests
import glob

word_length_threshold = 3

def script_prepare(scriptname):
    script = []
    translation = {}
    keywords = []
    with open(scriptname) as scriptfile:
        # for line in re.split("(?=[^a-zA-Z\s])",scriptfile.read().replace("\n"," ").replace("-"," ").replace("_"," ")):
        for line in scriptfile:
            line = line.strip()
            if not line:
                continue
            script.append(line)
            keywords.append([word.strip("\"?,._-i()") for word in line.split(" ") if len(word)>=word_length_threshold])
    for translationfile in glob.glob((".*.").join(sys.argv[1].rsplit(".",1))):
        lang = translationfile.rsplit(".",2)[1].strip(".")
        translation[lang] = []
        with open(translationfile) as script_trans:
            for line in script_trans:
                translation[lang].append(line.strip())
    return script,keywords,translation

def jaccard_similarity(x,y):
    """ returns the jaccard similarity between two lists """
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return intersection_cardinality/float(union_cardinality)

def matchscore(x,match,keywords,lastmatch):
    jaccard = jaccard_similarity(keywords[x],match)
    bias = math.e**(-1.5*(x/float(len(keywords)))**2)*0.3
    if abs(x-lastmatch<3):
        pass #print(f"  {x}: {jaccard}+{bias}")
    return jaccard*2 +bias

def main():
    script,keywords,translation = script_prepare(sys.argv[1])
    lastmatch = -1
    for line in sys.stdin:
        #print("    ["+line.strip()+"]")
        words = line.strip().split(" ")
        if len(words)<4:
            continue
        words_filtered = [word for word in words if len(word)>=word_length_threshold]
        if not words_filtered:
            continue
        matchline = max(range(len(script)),key=lambda x:matchscore(x,words_filtered,keywords,lastmatch))
        if matchline!=lastmatch and matchscore(matchline,words_filtered,keywords,lastmatch)>0.7:
            print(script[matchline])
            for lang in translation:
                print("||" + lang + "  " + translation[lang][matchline])                   
            lastmatch = matchline

if __name__=="__main__":
    sys.exit(main())
