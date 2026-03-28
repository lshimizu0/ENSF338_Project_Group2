import copy

graph = {
    'eng': {'ccit': 2, 'ict': 3},
    'ccit': {'eng': 2},
    'ict': {'eng': 3, 'link': 2},
    'link': {'ict': 2, 'scienceB': 2, 'mathSci': 2},
    'scienceB': {'link': 3, 'scienceA': 3, 'macHall': 1},
    'mathSci': {'link': 2, 'sciTheater': 2},
    'scienceA': {'scienceB': 3, 'sciTheater': 1},
    'macHall': {'scienceB': 1},
    'sciTheater': {'mathSci': 2, 'scienceA': 1}
}


def minPath(dict):
    smallestID = ''
    smallestInt = float('inf')
    for i in dict.keys():
        if dict.get(i) < smallestInt:
            smallestInt = dict.get(i)
            smallestID = i
    return smallestID


def pathAddition(graph, path):
    if not path:
        return float('inf')
    final = 0

    for i in range(len(path) - 1):
        final += graph.get(path[i]).get(path[i + 1])
    return final


def bestRoute(graph, start, end):
    if not graph.get(start):
        raise Exception("Starting position not found")
    currentRoute = copy.deepcopy(graph)
    path = [start]
    minPathList = []
    current = minPath(currentRoute.get(start))
    pathsTaken = [['eng']]

    breakEdge = False
    prev = start
    while path:
        if not breakEdge:
            path.append(current)
            pathsTaken.append(copy.deepcopy(path))
        else:
            breakEdge = False
        # if we are at the destination
        if (current == end):
            if pathAddition(graph, path) < pathAddition(graph, minPathList):
                minPathList = copy.deepcopy(path)
            path = [start]
            current = prev
            continue

        # Checking if allowed to go to next vertice
        while True:
            if not currentRoute.get(current):
                breakEdge = True
                break
            next = minPath(currentRoute.get(current))
            nextpath = copy.deepcopy(path)
            nextpath.append(next)
            if next in path or nextpath in pathsTaken:
                currentRoute.get(current).pop(next)
                continue
            break
        currentRoute = copy.deepcopy(graph)
        if breakEdge:
            current = prev
            path.pop()
            continue

        prev = current
        current = next
    return minPathList


print(bestRoute(graph, 'eng', 'link'))




