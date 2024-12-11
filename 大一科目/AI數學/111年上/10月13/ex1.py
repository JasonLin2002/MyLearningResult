a=set()
b=set()
print("Enter group A's subjects:")

while True:
  enter=input()
  if enter != "end":
        a.add(enter)
  if enter=="end":
        break


print("Enter group B's subjects:")
while True:
  enter=input()
  if enter != "end":
        b.add(enter)
  if enter =="end":
        break

print(a|b)
print(a&b)
print(b-a)
print(a^b)