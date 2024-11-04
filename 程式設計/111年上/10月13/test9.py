x, y, z = map(int, input().split())
if x<=y and y<=z:
    if x+y>z:
        print("Ture")
    else:
        print('Flase')
else:
    print('Flase')