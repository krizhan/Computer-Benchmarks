import subprocess

fileData = open("numaData.txt", "r") 
fileContents = fileData.readlines()

measurements = {}
max_value = 0

for cpu_line in range(0, len(fileContents), 6):
    cpu_index = int(fileContents[cpu_line].split()[3])
    copy_rate = float(fileContents[cpu_line + 2].split()[1]) * 10
    scale_rate = float(fileContents[cpu_line + 3].split()[1]) * 10
    add_rate = float(fileContents[cpu_line + 4].split()[1]) * 10
    triad_rate = float(fileContents[cpu_line + 5].split()[1]) * 10
    measurements[cpu_index] = {"Copy": copy_rate, "Scale": scale_rate, "Add": add_rate, "Triad": triad_rate}
    
    max_value = max(max_value, copy_rate, scale_rate, add_rate, triad_rate)

max_value = max_value / 10 * 1.05

nudeCpuFileContents = open("numaCPUs.txt", "r") .readlines()

node_cpus = {}

for node_line in nudeCpuFileContents:
    nodeLineContents = node_line.split()
    node_id = int(nodeLineContents[1])
    node_cpus[node_id] = map(lambda x: int(x), nodeLineContents[3:])

node_averages = {}
for each_node in node_cpus:
    average = {"Copy": 0, "Scale": 0, "Add": 0, "Triad": 0}
    for each_cpu in node_cpus[each_node]:
        average["Copy"] += measurements[each_cpu]["Copy"]
        average["Scale"] += measurements[each_cpu]["Scale"]
        average["Add"] += measurements[each_cpu]["Add"]
        average["Triad"] += measurements[each_cpu]["Triad"]
    average["Copy"] = round(average["Copy"] / (10 * len(node_cpus[each_node])), 1)
    average["Scale"] = round(average["Scale"] / (10 * len(node_cpus[each_node])), 1)
    average["Add"] = round(average["Add"] / (10 * len(node_cpus[each_node])), 1)
    average["Triad"] = round(average["Triad"] / (10 * len(node_cpus[each_node])), 1)
    node_averages[each_node] = average


averageDataFile = open("averageData.tsv", "w")
averageDataFile.write("Node Copy Scale Add Triad\n")
for each_row in node_averages:
    node = str(each_row)
    copy_val = str(node_averages[each_row]["Copy"])
    scale_val = str(node_averages[each_row]["Scale"])
    add_val = str(node_averages[each_row]["Add"])
    triad_val = str(node_averages[each_row]["Triad"])
    averageDataFile.write(node + " " + copy_val + " " + scale_val + " " + add_val + " " + triad_val + "\n")

averageDataFile.close()    
    
scriptName = "plotNUMAaverages.sh"
    
newScript = open(scriptName, "w") 
newScript.write('''
#!/bin/sh
gnuplot << ---EOF---
''');
newScript.write('''
reset
set title 'NUMA Node Average Memory Bandwidth'
set xlabel 'Node ID'
set ylabel 'Memory Bandwidth (MB/s)'
set key
set xtics rotate out
set style data histogram
set style fill solid border
set style histogram clustered
set term png
''');
newScript.write("set output \"NUMAaverages.png\"\n");
newScript.write("set yrange [0:%f]\n" % (max_value))
newScript.write('''
plot for [COL=2:5] 'averageData.tsv' using COL:xticlabels(1) title columnheader
---EOF---
''')

newScript.close()
rc = subprocess.Popen(['bash', scriptName])
rc.communicate()


for each_node in node_cpus:
    fileName = "node" + str(each_node) + "data.tsv"
    nodeDataFile = open(fileName, "w")
    nodeDataFile.write("CPU Copy Scale Add Triad\n")
    for each_cpu in node_cpus[each_node]:
        cpu = str(each_cpu)
        copy_val = str(measurements[each_cpu]["Copy"] / 10)
        scale_val = str(measurements[each_cpu]["Scale"] / 10)
        add_val = str(measurements[each_cpu]["Add"] / 10)
        triad_val = str(measurements[each_cpu]["Triad"] / 10)
        nodeDataFile.write(cpu + " " + copy_val + " " + scale_val + " " + add_val + " " + triad_val + "\n")
    nodeDataFile.close()

    scriptName = "plotNUMAaverages.sh"
    
    newScript = open(scriptName, "w") 
    newScript.write('''
#!/bin/sh
gnuplot << ---EOF---
''');
    newScript.write('''
reset
set key
set xlabel 'CPU ID'
set ylabel 'Memory Bandwidth (MB/s)'
set xtics rotate out
set style data histogram
set style fill solid border
set style histogram clustered
set term png
''');
    newScript.write("set title 'Node %d Memory Bandwidth'\n" % (each_node))
    newScript.write("set output \"Node%dBandwidth.png\"\n" % (each_node))
    newScript.write("set yrange [0:%f]\n" % (max_value))
    newScript.write("plot for [COL=2:5] '%s' using COL:xticlabels(1) title columnheader\n" % (fileName));
    newScript.write('''
---EOF---
''')

    newScript.close()

    rc = subprocess.Popen(['bash', scriptName])
    rc.communicate()
    
        
