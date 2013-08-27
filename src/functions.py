from numpy import array
from numpy import zeros


def FindPath (walkability,startX,startY,targetX,targetY):
    mapWidth = walkability.shape[1]
    mapHeight = walkability.shape[0]
    notfinished = 0
    notStarted = 0
    found = 1 
    nonexistent = 2 
    walkable = 0
#    unwalkable = 1
    newOpenListItemID=0
    addedGCost = 10
    openList=zeros((mapWidth*mapHeight+2),dtype=int)
    whichList=zeros((mapWidth+1,mapHeight+1),dtype=int) 
    openX=zeros((mapWidth*mapHeight+2),dtype=int)
    openY=zeros((mapWidth*mapHeight+2),dtype=int)
    parentX=zeros((mapWidth+1,mapHeight+1),dtype=int)
    parentY=zeros((mapWidth+1,mapHeight+1),dtype=int)
    Fcost=zeros((mapWidth*mapHeight+2),dtype=int)
    Gcost=zeros((mapWidth+1,mapHeight+1),dtype=int)    
    Hcost=zeros((mapWidth*mapHeight+2),dtype=int)
    pathLength=0      
    pathLocation=0

    if (startX == targetX and startY == targetY and pathLocation > 0):
        return found
    if (startX == targetX and startY == targetY and pathLocation == 0):
        return nonexistent

    if (walkability[targetX,targetY] != 0):
        return 0

    onClosedList = 2    
    onOpenList = 1
    pathLength  = notStarted
    pathLocation  = notStarted
    Gcost[startX,startY] = 0 

    numberOfOpenListItems = 1
    openList[1] = 1
    openX[1] = startX  
    openY[1] = startY

    while True:
        if (numberOfOpenListItems != 0):
            parentXval = openX[openList[1]]
            parentYval = openY[openList[1]] 
            whichList[parentXval,parentYval] = onClosedList

            numberOfOpenListItems = numberOfOpenListItems - 1
            openList[1] = openList[numberOfOpenListItems+1]      
            v = 1

            while True:
                u = v		
                if (2*u+1 <= numberOfOpenListItems):
                    if (Fcost[openList[u]] >= Fcost[openList[2*u]]) :
                        v = 2*u
                    if (Fcost[openList[v]] >= Fcost[openList[2*u+1]]) :
                        v = 2*u+1
                else:
                    if (2*u <= numberOfOpenListItems):
                        if (Fcost[openList[u]] >= Fcost[openList[2*u]]) :
                            v = 2*u

                if (u != v) :
                    openList[u],openList[v]=openList[v],openList[u]
                else:
                    break

            for b in [parentYval-1,parentYval, parentYval+1]:
                for a in [parentXval-1,parentXval, parentXval+1]:
                    if (a != -1 and b != -1 and a != mapWidth and b != mapHeight):
                        if (whichList[a,b] != onClosedList) and walkability [a,b] == 0 :
                            if (abs(a-parentXval)+abs(b-parentYval)==1) :
                                if (whichList[a,b] != onOpenList) :

                                    newOpenListItemID = newOpenListItemID + 1 
                                    m = numberOfOpenListItems+1
                                    openList[m] = newOpenListItemID
                                    openX[newOpenListItemID] = a
                                    openY[newOpenListItemID] = b

                                    Gcost[a,b] = Gcost[parentXval,parentYval] + addedGCost

                                    Hcost[openList[m]] = 10*(abs(a - targetX) + abs(b - targetY))
                                    Fcost[openList[m]] = Gcost[a,b] + Hcost[openList[m]]
                                    parentX[a,b] = parentXval 
                                    parentY[a,b] = parentYval	

                                    while (m != 1) :
                                        if (Fcost[openList[m]] <= Fcost[openList[m/2]]):
                                            openList[m],openList[m/2]=openList[m/2],openList[m]
                                            m = m/2
                                        else:
                                            break

                                    numberOfOpenListItems = numberOfOpenListItems+1
                                    whichList[a,b] = onOpenList

                                else:
                                    tempGcost = Gcost[parentXval,parentYval] + addedGCost

                                    if (tempGcost < Gcost[a,b]) :
                                        parentX[a,b] = parentXval
                                        parentY[a,b] = parentYval
                                        Gcost[a,b] = tempGcost
                                        for x in [x+1 for x in range(numberOfOpenListItems)]:
                                            if (openX[openList[x]] == a and openY[openList[x]] == b):
                                                Fcost[openList[x]] = Gcost[a,b] + Hcost[openList[x]]
                                                m = x
                                                while (m != 1):
                                                    if (Fcost[openList[m]] < Fcost[openList[m/2]]):
                                                        openList[m],openList[m/2]=openList[m/2],openList[m]
                                                        m = m/2
                                                    else:
                                                        break
                                                break 


        else:
            path = nonexistent 
            break

        if (whichList[targetX,targetY] == onOpenList):
            path = found 
            break

#    print whichList
    if (path == found):
        pathX = targetX 
        pathY = targetY
        while True:
            tempx = parentX[pathX,pathY]
            pathY = parentY[pathX,pathY]
            pathX = tempx
            pathLength = pathLength + 1
            if(pathX == startX and pathY == startY):
                break


        pathX = targetX 
        pathY = targetY
        cellPosition = pathLength
        pathBank=zeros((2,cellPosition),dtype=int)
        while True:
            cellPosition = cellPosition - 1
            pathBank [0,cellPosition] = pathX
            pathBank [1,cellPosition] = pathY

            tempx = parentX[pathX,pathY]
            pathY = parentY[pathX,pathY]
            pathX = tempx

            if (pathX == startX and pathY == startY):
                break

        return pathBank
    else:
        return False

