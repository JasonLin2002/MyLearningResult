visited = [0]
output = ""
count = 0

def setNum(n:int, num:int=0):
    global output
    global count
    if (num != 0):
        visited.append(num)
        output = output + str(num)
    is_leaf = True
    for i in range(1, n+1):
        if (i not in visited):
            is_leaf = False
            setNum(n, i)
    if (is_leaf):
        count += 1
        print(output)
    output = output[:-1]
    visited.remove(num)



setNum(3, 0)

print(count)