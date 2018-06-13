import sys
import subprocess as sp

COUNTTHREADS = 0

if(len(sys.argv) == 5):
    try:
        if(int(sys.argv[1]) > 3 or int(sys.argv[1]) < 1):
            print("Uncorrected value")
        else:
            COUNTTHREADS = int(sys.argv[1])
    except:
        print("Uncorrected type of arguments")
    IP = sys.argv[2]
    NAME = sys.argv[3]
    PORT = sys.argv[4]
else:
    print("Uncorrected count of arguments")

print('')

processes = []
try:
    for i in range(COUNTTHREADS):
        processes.append(sp.Popen('python3 thread%d.py %d %s %s %s' % \
            (i, COUNTTHREADS, IP, NAME, PORT), shell = True, stdout = sp.PIPE, universal_newlines=True))
except:
    print("Error making threads")

for p in processes:
    print()
    for line in p.stdout:
        print(line.replace('!', '#'), end='')
    p.wait()
    
f = open('break.txt','w')
f.write('False')
f.close()

