#====================================================================
# Sarah Middleton
# 
# parse_cmscore_output.py
# Parses cmscore output for a db and combines into a single bitscore file.
# Format: rows = sequences, columns = CMs, each cell holds a bitscore
#
# Required args: RESULTS_FOLDER, OUT_FILE
# Usage: python parse_cmscore_output.py ../demo/demo1/cmscore_results_rfam ../demo/demo1/demo1.bitscore
#====================================================================
import sys, subprocess, glob


# command line options, if present (all or nothing)
if len(sys.argv) == 3:
	RESULTS_FOLDER = sys.argv[1].rstrip("/")
	OUT_FILE = sys.argv[2]
else:
	print "Must indicate all command line options: RESULTS_FOLDER, OUT_FILE"
	print "Exiting."
	sys.exit(1)

# get list of results in folder
seqCount = 0
fileNames = glob.glob(RESULTS_FOLDER + "/scores_*.cm.txt")
fileNames.sort()
if len(fileNames) == 0:
	print ">> Error: no score files found. There may have been a problem during scoring."
	print ">> Exiting."
	sys.exit(1)

# go through each file, extract bitscores 
# check if any IDs got cut off
cmList = []
data = {}
for fileName in fileNames:
	ins = open(fileName, 'r')
	lines = ins.readlines()
	ins.close()
	
	# get cm name (12th line)
	tmpList = lines[12].split()
	cmName = tmpList[2]
	cmList.append(cmName)
	
	# get scores
	for line in lines:
		if line[0] != "#": #skip these lines
			columns = line.split()
			if len(columns) == 5:
				id = columns[0]
				score = columns[2] #we use the first score, unbanded d&c cyk, because "non-banded CYK variants are guaranteed to find the optimal alignment and score of each sequence" (Infernal 1.0 userguide pg. 93)
				if id not in data:
					data[id] = {}
				if cmName in data[id]:
					print ">> Warning: repeat id:", id, "in", cmName
					print ">> The ID may have been truncated by Infernal. Max length for a seq ID is 25 characters."
					#print "Exiting."
					#sys.exit(1)
				data[id][cmName] = score

# print results
outs = open(OUT_FILE, 'w')
numCMs = len(cmList)
numSeqs = 0
for cm in cmList: # print header
	outs.write(cm + "\t")
outs.write("\n")
for id in sorted(data.keys()):
	outs.write(id + "\t")
	numSeqs += 1
	for cm in cmList:
		if cm in data[id]:
			outs.write(data[id][cm] + "\t")
		else:
			print ">> Error: score missing for", id, cm
			print ">> This shouldn't happen. Exiting."
			sys.exit(1)
	outs.write("\n")
outs.close()

if numSeqs == 0:
	print ">> Error: no sequences found. There may have been a problem reading the score files."
	print ">> Exiting."
	sys.exit(1)
if numCMs == 0:
	print ">> Error: no CMs found. There may have been a problem reading the score files."
	print ">> Exiting."
	sys.exit(1)

print ""
print "Number of sequences:", numSeqs
print "Number of features:", numCMs
print "Bitscore file printed to", OUT_FILE
print ""





