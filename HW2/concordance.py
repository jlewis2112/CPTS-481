
"""
Joseph Lewis
481 HW2
concordance mod
"""

punct = ['.','?',',','!',':',';']


#used to remove all punctuation in a word
def removePunct(word):
    for c in punct:
        if c in word:
            word = word.replace(c, "")
    return word
    
"""
This functions reads a opened file
and returns a dict with the words as keys.
The enteries are occurences of lines
"""  
def concordance(f, unique = True):
    numLines = 1
    concord = {}
    lines = f.readlines()
    for line in lines:
        linex = line.strip()
        lineList = linex.split(" ")
        for word in lineList:
            if word != "":
                wordx = word.lower()
                wordx = removePunct(wordx)
                if(unique == True):
                    if wordx in concord:
                        if numLines in concord[wordx]:
                            pass
                        else:
                            concord[wordx].append(numLines)
                    else:
                        concord[wordx] = [numLines]
                else:
                    if wordx in concord:
                        concord[wordx].append(numLines)
                    else:
                        concord[wordx] = [numLines]
        numLines += 1
    return concord
 
#test cases   
if __name__ == "__main__":
    f = open("testfile", "r")
    concord = concordance(f)
    print("result of concord unique case")
    print(concord)
    print(concord == {"hello":[1,3],"world":[1],"hi":[2]})
    f.close()
    f = open("testfile", "r")
    concord = concordance(f, False)
    print("result of concord not unique case")
    print(concord)
    print(concord == {"hello":[1,1,3],"world":[1,1],"hi":[2]})
                    
            
	 
