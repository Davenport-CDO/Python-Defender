import psutil
import os
import signal

knownRunningProcesses = list()
blacklisted = list()

if(os.path.isfile("black.txt")):
    print("Loading from blacklist...")
    for line in open("black.txt", "r"):
        blacklisted.append(line[:-1])

    for line in blacklisted:
        print(line)

    print("Done.")

for proc in psutil.process_iter():
    knownRunningProcesses.append(proc.name())

def setBlacklist():
    x = open("black.txt", "w")
    for e in blacklisted:
        x.write(e + "\n")
    
while True:
    newProcesses = list()
    
    for proc in psutil.process_iter():
        if(proc.name() in blacklisted):
            print("Attempting to kill blacklisted process: {0}".format(proc.name()))
            try:
                proc.kill()
                print("Process killed!")
            except:
                try:
                    os.kill(proc.pid, signal.SIGKILL)
                    print("Process killed!")
                except:
                    try:
                        proc.terminate()
                        print("Process killed!")
                    except:
                        print("Failed to kill process!")
            
        
        elif proc.name() not in knownRunningProcesses:
            newProcesses.append(proc)
            try:
                proc.suspend()
            except:
                pass

        

    for proc in newProcesses:
        answer = input("New Process: {0} with Prcoess ID: {1}. Kill it(1). Do Not(2)".format(proc.name(), proc.pid))
        if int(answer) == 1:
            blacklisted.append(proc.name())
            setBlacklist()
            try:
                proc.kill()
            except:
                try:
                    os.kill(proc.pid, signal.SIGKILL)
                except:
                    try:
                        proc.terminate()
                    except:
                        pass
        else:
            proc.resume()
            knownRunningProcesses.append(proc.name())
            

        
