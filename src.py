import re

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
            #curPos= list(map(sum,zip(curPos,slope)))  #  Not sure why this bit fails
            curPos[0] += slope[0]
            curPos[1] += slope[1]
        totalTreesHit *= treesHit
    return totalTreesHit
    

def day4(p2 = False):
    passport = {
    "byr": None,
    "iyr": None,
    "eyr": None,
    "hgt": None,
    "hcl": None,
    "ecl": None,
    "pid": None,
    "cid": 0, # Ignore none input for this field
    "filledOut": False,
    "valid": False
    }
    
    # Limited Lambda helpers
    cmin = {
    "cm": (lambda hgt: 150 <= int(hgt) <= 193),
    "in": (lambda hgt: 59 <= int(hgt) <= 76)
    }
    ppValidations = {
    "byr": (lambda data: 1920 <= int(data) <= 2002),
    "iyr": (lambda data: 2010 <= int(data) <= 2020),
    "eyr": (lambda data: 2020 <= int(data) <= 2030),
    "hgt": (lambda data: bool(re.search("^\d+(cm|in)$", data)) and cmin[data[-2:]](data[:-2])),
    "hcl": (lambda data: bool(re.search("^#[a-f0-9]{6}$", data))),
    "ecl": (lambda data: data in "amb blu brn gry grn hzl oth".split()), # Is this bad practice? too lazy for commas
    "pid": (lambda data: bool(re.search("^\d{9}$", data))),
    "cid": (lambda data: True), # Ignore none input for this field',
    "filledOut": (lambda data: data), # Pass along
    "valid": (lambda data: True) # Assume True for check
    }
    
    ppList = []
    ppLines = read("day4.in")
    pp = passport.copy()
    for ppLine in ppLines:
        if ppLine == "" or ppLine == "\n":
            if not any([x is None for x in pp.values()]):
                pp['filledOut'] = True
                pp["valid"] = all([ppValidations[key](pp[key]) for key in [*pp]]) # List comprehension lambda bash
                print([ppValidations[key](pp[key]) for key in [*pp]])
            
            ppList.append(pp) # Append Current Dict
            pp = passport.copy() # Reset Dict to default
            continue
        for id,key in [x.split(':') for x in [keyCombo for keyCombo in ppLine.split()]]:
            try: pp[id] = key
            except: print("ERROR: UNEXPECTED INPUT:"+(id,key)) # Shouldn't happen?
    filledOut = len([pp for pp in ppList if pp["filledOut"]])
    valid = len([pp for pp in ppList if pp["valid"]])
    #invalid = len(ppList) - valid
    
    return (filledOut, valid)
     #ToDO: Filter Keys to better variable types
    
    
def day5(p2 = False):
    ROWS=128
    COLUMNS=8
    rules = { # Should have just done a binary coversion for this
    "F": (lambda set: (set[0], int(set[1]-(set[1]-set[0])/2), set[2], set[3])),
    "B": (lambda set: (int(set[0]+(set[1]-set[0])/2), set[1], set[2], set[3])),
    "L": (lambda set: (set[0], set[1], set[2], int(set[3]-(set[3]-set[2])/2))),
    "R": (lambda set: (set[0], set[1], int(set[2]+(set[3]-set[2])/2), set[3])),
    }
    seatChart= read('day5.in')
    seatsTaken=[]
    seatsTakenMap= [[False for x in range(ROWS)] for y in range(COLUMNS)]
    for seatKey in seatChart:
        lower = 0
        upper= ROWS
        lefter=0
        righter=COLUMNS
        for char in seatKey: lower,upper,lefter,righter = rules[char]((lower,upper,lefter,righter))
        seat = (lefter,lower) # (Column, Row)
        seatID= seat[1]*8+seat[0]
        seatsTaken.append(seatID)
        try: seatsTakenMap[lefter][lower]= True
        except: print(lefter,lower)
    
    if not p2: 
        return(max(seatsTaken))
    openSeats = [(x,y) for x in range(COLUMNS) for y in range(ROWS) if not seatsTakenMap[x][y] and 0 < y < ROWS]
    for x,y in openSeats:
         seatID = y*8+x
         if seatID+1 in seatsTaken and seatID-1 in seatsTaken:
            return(seatID)


def listAndSet(listIn):
        xSet = set(listIn[0])
        for x in listIn: xSet &= set(x)
        return xSet
def day6(p2 = False):
    answers= read('day6.in')
    if not p2:
        groupSets = [set("".join(group.split("\n"))) for group in '\n'.join(answers).split("\n\n")]
    else: 
        groupSets = [listAndSet(group.split("\n")) for group in '\n'.join(answers).split("\n\n")]
    return sum(list(map(lambda l: len(l), groupSets)))



def main():
    print(day6(True))

if __name__=="__main__":
    main()
