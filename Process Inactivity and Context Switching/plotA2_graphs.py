import subprocess

fileData = open("data/partA2data.txt", "r") 
fileContents = fileData.readlines()

totalDuration = {}
nextDuration = {}
eachDuration = {}
maxDuration = 0
for line in fileContents:
    if "Error" in line:
        print("Error running experiment, try again")
    
    process = int(line.split()[1][:-1])
    nextDuration = float(line.split()[12][1:])
    currentTime = float(line.split()[7][1:])
    maxDuration = max(maxDuration, round(currentTime, 10) + 2 * round(nextDuration, 10))
    if process not in totalDuration:
        totalDuration[process] = [round(currentTime, 10)]
        eachDuration[process] = [round(nextDuration, 10)]
    else:
        totalDuration[process].append(round(currentTime, 10))
        eachDuration[process].append(round(nextDuration, 10))

for each_process in totalDuration:
    totalDuration[each_process].pop(0)
    eachDuration[each_process].pop(0)
    scriptName = "data/plotScript" + str(each_process) + ".sh"
    
    newScript = open(scriptName, "w") 
    newScript.write('''
#!/bin/sh
gnuplot << ---EOF---
''');
    newScript.write("set title 'Context Switch: Process %d Plot'\n" % each_process);
    newScript.write('''
set xlabel 'Time (ms)'
set nokey
set noytics
set term postscript color eps 10
set size 0.45, 0.35
    ''')
    newScript.write("set output 'data/Process%d_Plot.eps'\n" % each_process);
    newScript.write("set object 1 rect from 0, 1 to %f, 2 fc rgb \"%s\" fs solid\n " %  (totalDuration[each_process][0] + eachDuration[each_process][0], "red"))
    
    totalPeriods = len(eachDuration[each_process]) / 2
    
    max_value = 2
    for period in range(0, totalPeriods):
        active_index = 2 * period
        inactive_index = 2 * period + 1
        newScript.write("set object %d rect from %f, 1 to %f, 2 fc rgb \"%s\" fs solid\n " % (active_index + 2, totalDuration[each_process][active_index], totalDuration[each_process][active_index] + eachDuration[each_process][active_index], "blue"))
        newScript.write("set object %d rect from %f, 1 to %f, 2 fc rgb \"%s\" fs solid\n" % (inactive_index + 2, totalDuration[each_process][inactive_index], totalDuration[each_process][inactive_index] + eachDuration[each_process][inactive_index], "red"))
        max_value = inactive_index
        
    newScript.write("set object %d rect from %f, 1 to %f, 2 fc rgb \"%s\" fs solid\n" % (max_value + 3, totalDuration[each_process][max_value] + eachDuration[each_process][max_value], maxDuration, "red"))
    newScript.write("plot [0:%f] [0:3] 0\n" % (maxDuration))
    newScript.write("---EOF---\n")
    newScript.close()

    rc = subprocess.Popen(['bash', scriptName])
    rc.communicate()
