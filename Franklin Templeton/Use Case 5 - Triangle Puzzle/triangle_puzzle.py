import time

filename = 'Use Case1 - triangle_test_100rows.txt'
m = []

with open(filename, 'r') as f:
    line = f.readline()
    while line:
        m.append(list(map(int, line.split())))
        line = f.readline()

n = len(m)

sums = {}

def getSum(row, col):
    if (row, col) in sums:
        return sums[(row, col)]

    if row == n:
        return 0

    res = m[row][col] + max(getSum(row+1, col), getSum(row+1, col+1))
    sums[(row,col)] = res
    return res

start = time.time()
print(getSum(0, 0))
end = time.time()

print('Time = ', end-start)