def getPre(current):
    if current != 1:
        return current - 1
    else:
        return 1


def getNext(current, maxPageCount):
    if current < maxPageCount:
        return current + 1
    else:
        return maxPageCount