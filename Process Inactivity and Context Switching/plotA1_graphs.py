import subprocess

fileData = open("data/partA1data.txt", "r") 
fileContents = fileData.readlines()

totalDuration = []
currentTime = 0
eachDuration = []

for line in fileContents:
    if "Error" in line:
        print("Error running experiment, try again")
        
    
    totalDuration.append(round(currentTime, 10))
    nextDuration = float(line.split()[12][1:])
    eachDuration.append(round(nextDuration, 10))
    currentTime += nextDuration

scriptName = "data/plotA1Script.sh"

newScript = open(scriptName, "w") 
newScript.write('''
#!/bin/sh
gnuplot << ---EOF---
set title 'Active and Inactive Periods'
set xlabel 'Time (ms)'
set nokey
set noytics
set term postscript color eps 10
set size 0.45, 0.35
set output "data/PartA1_Plot.eps"
''')
totalPeriods = len(eachDuration) / 2

for period in range(0, totalPeriods):
    active_index = 2 * period
    inactive_index = 2 * period + 1
    newScript.write("set object %d rect from %f, 1 to %f, 2 fc rgb \"%s\" fs solid\n " % (active_index + 1, totalDuration[active_index], totalDuration[active_index] + eachDuration[active_index], "blue"))
    newScript.write("set object %d rect from %f, 1 to %f, 2 fc rgb \"%s\" fs solid\n" % (inactive_index + 1, totalDuration[inactive_index], totalDuration[inactive_index] + eachDuration[inactive_index], "red"))
    
newScript.write("plot [0:%f] [0:3] 0\n" % (totalDuration[-1] + 2 * eachDuration[-1]))
newScript.write("---EOF---\n")
    
newScript.close()

rc = subprocess.Popen(['bash', scriptName])
rc.communicate()