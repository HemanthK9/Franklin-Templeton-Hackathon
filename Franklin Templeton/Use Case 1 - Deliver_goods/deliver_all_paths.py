n = 6

path = []
maxpath = tuple()
visited = [0]*n

maxSum = 0

def visit(currSum, path, v, visited):
    global maxSum
    global maxpath

    path.append(v)
    visited[v] = 1

    if sum(visited) == n:
        print(path)
        if currSum > maxSum:
            maxSum = currSum
            maxpath = tuple(path)
        return
    for i in range(n):
        if not visited[i]:
            currSum += abs(v-i)
            visit(currSum, path.copy(), i, visited.copy())
            currSum -= abs(v-i)

    path.pop()

for i in range(n):
    #print(i, visited, path)
    visit(0, path, i, visited)
    visited[i] = 0

print(maxSum, maxpath)