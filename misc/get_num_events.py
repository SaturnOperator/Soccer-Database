import json
import os

events = {}

def get_num_events(filePath):
    # Open and load the JSON file
    with open(filePath, 'r') as file:
        data = json.load(file)
    
    # for event in data: # Get one of all unique events types
    return len(data)


dirPath = "/Users/abdullah/comp_3005_final_project/open-data-0067cae166a56aa80b2ef18f61e16158d6a7359a/data/events/"
files = os.listdir(dirPath)


eventCount = 0

for file in files:
    filePath = os.path.join(dirPath, file)
    
    eventCount += get_num_events(filePath)

print(eventCount)