import sys
import subprocess
import time

COUNTTHREADS = 0

PASSWORD = sys.argv[2]

#print(PASSWORD)

try:
    if(int(sys.argv[1]) > 3 or int(sys.argv[1]) < 1):
            print("Uncorrected value")
    else:
            COUNTTHREADS = int(sys.argv[1])
except:
    print("Uncorrected type of arguments")

print('Third thread was started at %s !!!' % time.asctime(time.localtime(time.time())))

a  = ('e','t','a','o','i','n','s','h','r',
                'd','l','c','u','m','w','f','g','y',
                'p','b','v','k','j','x','q','z','1',
                '2','3','4','5','6','7','8','9','0',
                '_','-'     
            )

def check():
    f = open('threads/break.txt','r')
    breaking = f.read().split()
    f.close()
    try:
        if(breaking[0]=="False"):
            return False
        else:
            return True
    except:
        return True
def end():
    print('Third thread: %s ' % PASSWORD)
    f = open('threads/break.txt','w')
    f.write('True')
    f.close()

for b in range(((len(a)//COUNTTHREADS)+1)*2,((len(a)//COUNTTHREADS)+1)*3):
    if(not check()):
        for c in range(len(a)):
            if(not check()):
                for d in range(len(a)):
                        for e in range(len(a)):
                            if(not check()):
                                for f in range(len(a)):
                                    if(not check()):
                                        for g in range(len(a)):
                                            if(not check()):
                                                for h in range(len(a)):
                                                    if((str(a[b])+str(a[c])+str(a[d])+str(a[e])+str(a[f])+str(a[g])+str(a[h]))==PASSWORD):
                                                        end()
                                                        '''
                                                                
                                                        if(not check()):
                                                            for i in range(len(a)):
                                                                if((str(a[b])+str(a[c])+str(a[d])+str(a[e])+str(a[f])+str(a[g])+str(a[h])+str(a[i]))==res):
                                                                    print(res)
                                                                    #breaking = False
                                                                if(not check()):
                                                                    for j in range(len(a)):
                                                                        if((str(a[b])+str(a[c])+str(a[d])+str(a[e])+str(a[f])+str(a[g])+str(a[h])+str(a[i])+str(a[j]))==res):
                                                                           print(res)
                                                                           #breaking = False
'''

print('Third thread was stoped at %s !!!' % time.asctime(time.localtime(time.time())))
