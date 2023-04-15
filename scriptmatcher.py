import sys
import math

def script_prepare(scriptname):
    script = []
    keywords = []
    with open(scriptname) as scriptfile:
        for line in scriptfile:
            line = line.strip()
            if not line:
                continue
            script.append(line)
            keywords.append([word for word in line.split(" ") if len(word)>=4])
    return script,keywords

def jaccard_similarity(x,y):
    """ returns the jaccard similarity between two lists """
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return intersection_cardinality/float(union_cardinality)

def matchscore(x,match,keywords,lastmatch):
    jaccard = jaccard_similarity(keywords[x],match)
    bias = 1/(1.5**(abs(lastmatch+1-x)+2))
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
        words_filtered = [word for word in words if len(word)>=3]
        if not words_filtered:
            continue
        matchline = max(range(len(script)),key=lambda x:matchscore(x,words_filtered,keywords,lastmatch))
        if matchline!=lastmatch and matchscore(matchline,words_filtered,keywords,lastmatch)>0.6:
            print(script[matchline])
            lastmatch = matchline

if __name__=="__main__":
    sys.exit(main())