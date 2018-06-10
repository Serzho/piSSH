import sys
import subprocess

COUNTTHREADS = 0

PASSWORD = ''

if(len(sys.argv) == 3):
    try:
        if(int(sys.argv[1]) > 3 or int(sys.argv[1]) < 1):
            print("Uncorrected value")
        else:
            COUNTTHREADS = int(sys.argv[1])
    except:
        print("Uncorrected type of arguments")
    PASSWORD = sys.argv[2]
else:
    print("Uncorrected count of arguments")

print('')

process = []

try:
    for i in range(COUNTTHREADS):
        process.append(subprocess.Popen('python threads/thread%d.py %d %s' % \
                                        (i, COUNTTHREADS, PASSWORD), shell = True))
except:
    print("Error making threads")

for p in process:
    p.wait()

f = open('threads/break.txt','w')
f.write('False')

