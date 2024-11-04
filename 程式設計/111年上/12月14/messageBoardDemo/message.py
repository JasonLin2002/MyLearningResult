def caesarEncoder(str1):
    list1=list(str1)
    for i in range(len(list1)):
        list1[i]=chr(ord(list1[i])+3)
    str1=''.join(list1)
    return str1
def caesarDecoder(str2):
    list2=list(str2)
    for i in range(len(list2)):
        list2[i]=chr(ord(list2[i])-3)
    str2=''.join(list2)
    return str2


def leaveMessage(account,str1):
    f = open("messageFile.txt","a")
    account=caesarEncoder(account)
    str1=caesarEncoder(str1)
    f.write("{} {} {}\n" .format(account,caesarEncoder(":"), str1))
    f.close()
def readMessage():
    f = open("messageFile.txt","r")
    for i in f:
        print(caesarDecoder(i))
    f.close()


    
def checkAccount(account,password):
    f = open("account.txt","r")
    c=dict()
    b=eval(f.read())
    for i in b:
        c[caesarDecoder(i)] = caesarDecoder(b[i])
    if (account in c) and (password == c[account]):
        return True
    else:
        return False
    f.close()

    

if __name__=='__main__'  :
    print(caesarEncoder("a"))
    print(caesarDecoder('d'))
    leaveMessage('abcd','cdef')
    readMessage()
    print(checkAccount('Jack',"10000000"))