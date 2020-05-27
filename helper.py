def caseStar(temp):
    return int(temp),''

def casePlus(temp,isPlus,dict,num):
    if(temp!=''):
        dict[temp]=num
        if(isPlus==False):
            dict[temp]*=-1
        temp=''
    isPlus=True
    return temp,isPlus

def caseMinus(temp,isPlus,dict,num):
    if(temp!=''):
        dict[temp]=num
        if(isPlus==False):
            dict[temp]*=-1
        temp=''
    isPlus=False
    return temp,isPlus

def caseGt(temp,isPlus,dict,num):
    dict[temp]=num
    if(isPlus==False):
        dict[temp]*=-1
    isPlus=True
    op='gt'
    temp=''
    return temp,isPlus,op

def caseLt(temp,isPlus,dict,num):
    dict[temp]=num
    if(isPlus==False):
        dict[temp]*=-1
    isPlus=True
    op='lt'
    temp=''
    return temp,isPlus,op
