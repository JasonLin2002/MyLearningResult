import message
print("****************************************")
print("*               ~welcome~              *")
print("****************************************")

while True:
    print('****************************************')
    print()
    print('press 1 :login')
    print('press 2 :exit')
    print('****************************************')
    print()
    a=input()
    if a=='2':
        break
    elif a=='1':
        b=input('Account:')
        c=input('Password:')
        if message.checkAccount(b,c):
            while True:
                print('****************************************')
                print()
                print('press 1 :leave a message')
                print('press 2 :read message')
                print("press 3 :logout")
                print('****************************************')
                e=input()
                if e=="3":
                    break
                elif e=='1':
                    f=input('message:')
                    message.leaveMessage(b,f)
                elif e=="2":
                    message.readMessage()
        
