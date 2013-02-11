numBuckets = 47

def create():
    global numBuckets
    hSet = []
    for i in range(numBuckets):
        hSet.append([])
    return hSet

def hashElem(e):
    global numBuckets
    return e%numBuckets

def insert(hSet, i):
    global numBuckets
    hSet[hashElem(i)].append(i)

def remove(hSet, i):
    newBucket = []
    for j in hSet[hashElem(i)]:
        if j!= i:
            newBucket.append(j)
    hSet[hashElem(i)] = newBucket

def member(hSet, i):
    return i in hSet[hashElem(i)]

numBuckets = 3
def test1():
    s = create()
    for i in range(40):
        insert(s, i)
    insert(s, 325)
    insert(s, 325)
    insert(s, 987654321)
    print s
    print member(s, 325)
    remove(s, 325)
    print member(s, 987654321)


def hashElem(e):
    global nunmBuckets
    if type(e) == int:
        val = e
    if type(e) == str:
        #convert s to an int
        val = 0
        shift = 0
        for c in e:
            val = val + shift*ord(c)
            shift += 1
    return val%numBuckets

def test2():
    d = create()
    strs = ['ah', 'ha', 'j2a', 'big dog', 'small bird']
    for s in strs:
        insert(d, s)
    for i in range(40):
        insert(d, i)
    print d
