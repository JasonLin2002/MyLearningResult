def connected_component(list_2D:list, x:int, y:int):
    if (list_2D[x][y] != 1):
        list_2D[x][y] = 1
        if (0 <= x-1 < len(list_2D[0])):
            connected_component(list_2D, x-1, y)
        
        if (0 <= x+1 < len(list_2D[0])):
            connected_component(list_2D, x+1, y)
        
        if (0 <= y-1 < len(list_2D)):
            connected_component(list_2D, x, y-1)

        if (0 <= y+1 < len(list_2D)):
            connected_component(list_2D, x, y+1)


def print_2D_array(list_2D:list):
    for i in list_2D:
        print(i)


t = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,0,1,1,1,1,1,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
    [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
    [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
    [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],
    [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],
    [0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0]
]

connected_component(t, 3, 10)

print_2D_array(t)
