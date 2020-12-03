

def read(filename):
    with open(filename, "r") as a_file:
        myList= []
        for line in a_file:
            myList.append(line.strip())
        return myList
            
    
def day1(p2 = False):
    expenses = [int(x) for x in read("day1.in")]
    if not p2:
        for i in expenses:
            if 2020-i in expenses: return i*(2020-i)
    else:
        for i in expenses:
            for j in expenses:
                k=2020-i-j
                if k in expenses: return k*i*j

def day2(p2 = False):
    numValid = 0 
    passwords = read("day2.in")
    for pw in passwords:
        keycode, txt = [x.strip() for x in pw.split(':')]
        key, code=keycode.split() 
        kMin,kMax = [int(i) for i in key.split('-')]
       
        if p2:
            if bool(txt[kMin-1] == code) != bool(txt[kMax-1] == code): # Ghetto XOR gate
                numValid +=1
        else:
            count = 0
            for char in txt: 
                if char == code: count +=1
            if kMin <= count <= kMax: numValid += 1
        
    return numValid
    
def day3(p2 = False):
    totalTreesHit= 1 # p2 mult patern, start at 1
    hillMap = read("day3.in")
    mWidth = len(hillMap[0])
    slopes = [(1,3),(1,1),(1,5),(1,7),(2,1)]  # Down 1, Over 3
    if not p2: slopes = [slopes[0]] # Only do the first slope for p1
    for slope in slopes:
        curPos = [0,0]
        treesHit = 0
        while curPos[0] < len(hillMap): # Break loop if outside hillMap
            if hillMap[curPos[0]][curPos[1]%mWidth]=='#':
                treesHit += 1
            #curPos= list(hillMap(sum,zip(curPos,slope)))  #  Not sure why this bit fails
            curPos[0] += slope[0]
            curPos[1] += slope[1]
        totalTreesHit *= treesHit
    return totalTreesHit

def main():
    print(day3(True))

if __name__=="__main__":
    main()
