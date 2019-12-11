def findWorst(n):
    worstSum = n*(n-1)//2
    if n%2 == 0:
        worstSum -= ((n+1)//2 + 1)
    else:
        worstSum -= (n//2 + 1)
    return worstSum

n = 6


path = []
visited = [0]*n
worstSum = findWorst(n+1)
print(worstSum)

def visit(currSum, path, v, visited):
    global worstSum
    #global maxpath

    path.append(v)
    visited[v] = 1

    if sum(visited) == n:
        if currSum == worstSum:
            print(path)
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
