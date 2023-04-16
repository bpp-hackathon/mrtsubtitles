import sys
import math
import re

word_length_threshold=4

def script_prepare(scriptname):
    script = []
    keywords = []
    with open(scriptname) as scriptfile:
        for i,line in enumerate(scriptfile):
            line = line.strip()
            if not line:
                continue
            script.append(line)
            for keyword in [word.strip("\"?,._-") for word in line.split(" ") if len(word)>=word_length_threshold]:
                keywords.append((i,keyword))
    return script,keywords

def hamming_distance(s1, s2):
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

def matchscore(x,match,keywords,lastmatch):
    jaccard = jaccard_similarity(keywords[x],match)
    bias = math.e**(-1.5*(x/float(len(keywords)))**2)*0.3
    if abs(x-lastmatch<3):
        print(f"  {x}: {jaccard}+{bias}")
    return jaccard+bias

def main():
    script,keywords = script_prepare(sys.argv[1])
    lastmatch = -1
    for line in sys.stdin:
        print("    ["+line.strip()+"]")
        words = line.strip().split(" ")
        if len(words)<4:
            continue
        words_filtered = [word for word in words if len(word)>=word_length_threshold]
        if not words_filtered:
            continue
        matchline = max(range(len(script)),key=lambda x:matchscore(x,words_filtered,keywords,lastmatch))
        if matchline!=lastmatch and matchscore(matchline,words_filtered,keywords,lastmatch)>0.5:
            print(script[matchline])
            lastmatch = matchline

if __name__=="__main__":
    sys.exit(main())
