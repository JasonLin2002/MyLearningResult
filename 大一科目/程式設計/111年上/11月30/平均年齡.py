a=eval(input())
b=0
c_dict={"users":[],'avg_age':0}
for i in a:
    b=b+i[1]
    c_dict['users'].append(i[0])
c_dict['avg_age']='{:.2f}'.format(b/len(a))
print(c_dict)