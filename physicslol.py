def getPointFunc1(xPos):
    return 1.5 + 0.5*0.85*(xPos*xPos)
def getPointFunc2(xPos):
    return (1.5 * xPos) + 0.5*-.1*(xPos*xPos)

xEnd = 1.6
x = 1.4
lowestDistance = 100000
lowestDistanceX = -1
run = True
while run:
    x += 0.001
    distance = getPointFunc1(x) - getPointFunc2(x)
    if(lowestDistance > distance):
        lowestDistance = distance
        lowestDistanceX = x
    if x >= xEnd:
        run = False
print(str(lowestDistance) + " " + str(lowestDistanceX))