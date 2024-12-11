import numpy as np
n = int(input("n = "))
m = int(input("m = "))
list1 = [] 
list2 = []
for i in range(m):
    list_n = [] 
    for j in range(n):
        val_n = int(input("Equation {} no.[{}]= ".format(i, j))) 
        list_n.append(val_n)
    list1.append(list_n)
for i in range(m):
    val_n2 = int(input("Equation [{}] = " .format(i)))
    list2.append(val_n2)
a = np.array(list1) 
b = np.array(list2)
print(np.linalg.solve(a, b))
# n = 3
# m = 3
# Equation 0 no.[0]= 6
# Equation 0 no.[1]= 4
# Equation 0 no.[2]= -1
# Equation 1 no.[0]= -6
# Equation 1 no.[1]= -5
# Equation 1 no.[2]= 7
# Equation 2 no.[0]= 2
# Equation 2 no.[1]= 0
# Equation 2 no.[2]= 3
# Equation [0] = 9
# Equation [1] = 6
# Equation [2] = 14
# [ 4.10714286 -3.42857143  1.92857143]