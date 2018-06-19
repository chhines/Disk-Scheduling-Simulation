#Colton Hines
#Problem Set 4
#COSC 335
#Simulating Disk Scheduling Algorithms

import random
import math

bestAlgorithm = math.inf #Integer to determine algorithm with the least amount of read head movement
bestTotal = math.inf # Best current total number of cylinders traversed per algorithm

# Switch-statement to output the best algorithm.
def best(ba): 
    switcher = {
        1: "FCFS is best.",
        2: "SSTF is best.",
        3: "Scan is best.",
        4: "Look is best.",
        5: "C-Scan is best.",
        6: "C-Look is best.",
    }
    return switcher.get(ba, "N/A")

# Function to generate a list of 1000 random integers between 0 and 4999 inclusive.
def generateRequests():
  randomRequests = random.sample(range(0,5000), 1000)
  return randomRequests

# First-come first-serve algorithm. Adds the distance between the current cylinder and its neighbor in order of appearance in the work queue.
def FCFS(n,requests):
  total = 0
  seekTime = 0
  for x in requests:
    total = total + int(abs(n - x))
    n = x
  seekTime = int(0.76 + (0.24 * math.sqrt(total)))
  global bestAlgorithm
  global bestTotal
  if(total < bestTotal):
    bestAlgorithm = 1
    bestTotal = total
  print("FCFS")
  print("=================================")
  print("Total cylinders traversed: ", total)
  print("Total seek time: ", seekTime, "milliseconds")
  print("=================================")
  print()
  
# Shortest seek time first algorithm. Adds the distance between the current cylinder and its closest neighbor in the work queue to the total distance.
def SSTF(n,requests):
  total = 0
  seekTime = 0
  while(len(requests) > 0):
    nearest = math.inf
    for x in requests:
      if(int(abs(n-x)) < (abs(n-nearest))):
        nearest = x
    
    total = total + int(abs(n-nearest))
    n = nearest
    requests.remove(nearest)
  seekTime = int(0.76 + (0.24 * math.sqrt(total)))
  global bestAlgorithm
  global bestTotal
  if(total < bestTotal):
    bestAlgorithm = 2
    bestTotal = total
  print("SSTF")
  print("=================================")
  print("Total cylinders traversed: ", total)
  print("Total seek time: ", seekTime, "milliseconds")
  print("=================================")
  print()
  
# Scan algorithm. Similar to the SSTF algorithm except the direction of the read head is descending (extra condition is added to the if statement to make sure the next cylinder considered lower on the disk than the current cylinder. When the head reaches the lowest cylinder in the work queue, the current cylinder and the next closest cylinder are added to total since the read head travels all the way to 0 before changing direction. Read head position is tracked by a variable (seekDownCount) containing the number of cylinders lower than the original read head position.
def Scan(n,requests): #Read head direction descending
  total = 0
  seekTime = 0
  seekDownCount = 0
  for x in requests:
    if(x<n):
      seekDownCount = seekDownCount + 1
  
  while(len(requests) > 0):
    nearest = math.inf
    if(seekDownCount > 0):
      for x in requests:
        if(((int(abs(n-x))) < (abs(n-nearest))) and (x < n)):
          nearest = x
      total = total + int(abs(n-nearest))
      n = nearest
      requests.remove(nearest)
      seekDownCount = seekDownCount - 1
    if(seekDownCount == 0):
      nearest = math.inf
      for x in requests:
        if((int(abs(n-x))) < (abs(n-nearest))):
          nearest = x
      total = total + n + nearest
      n = nearest
      requests.remove(nearest)
      seekDownCount = seekDownCount - 1
    else:
      nearest = math.inf
      for x in requests:
        if((int(abs(n-x))) < (abs(n-nearest))):
          nearest = x
      total = total + int(abs(n-nearest))
      n = nearest
      requests.remove(nearest)
      seekDownCount = seekDownCount - 1
  seekTime = int(0.76 + (0.24 * math.sqrt(total)))
  global bestAlgorithm
  global bestTotal
  if(total < bestTotal):
    bestAlgorithm = 3
    bestTotal = total
  print("Scan")
  print("=================================")
  print("Total cylinders traversed: ", total)
  print("Total seek time: ", seekTime, "milliseconds")
  print("=================================")
  print()
  
  # Look algorithm. Similar to Scan, except when the read head switches direction only the distance to the nearest cylinder is added to the total. Read head direction is ascending to match the in-class assignment for testing purposes (although the direction shouldn't matter for total distance traveled).
def Look(n,requests): # Read head direction ascending.
  total = 0
  seekTime = 0
  seekDownCount = 0
  for x in requests:
    if(x>n):
      seekDownCount = seekDownCount + 1
  
  while(len(requests) > 0):
    nearest = math.inf
    if(seekDownCount > 0):
      for x in requests:
        if(((int(abs(n-x))) < (abs(n-nearest))) and (x > n)):
          nearest = x
      total = total + int(abs(n-nearest))
      n = nearest
      requests.remove(nearest)
      seekDownCount = seekDownCount - 1
    if(seekDownCount <= 0):
      nearest = math.inf
      for x in requests:
        if(((int(abs(n-x))) < (abs(n-nearest)))):
          nearest = x
      total = total + int(abs(n-nearest))
      n = nearest
      requests.remove(nearest)
      seekDownCount = seekDownCount - 1
  seekTime = int(0.76 + (0.24 * math.sqrt(total)))
  global bestAlgorithm
  global bestTotal
  if(total < bestAlgorithm):
    bestAlgorithm = 4
    bestTotal = total
  print("Look")
  print("=================================")
  print("Total cylinders traversed: ", total)
  print("Total seek time: ", seekTime, "milliseconds")
  print("=================================")
  print()
  
# C-Scan algorithm. Same as Scan except the read head jumps to the end of the disk. The distance between the top and bottom cylinders and the maximum and minimum cylinders are added to total because the read head seeks to the edge of the disk before jumping. The jump is not included in read head traversal.
def CScan(n,requests): # Read head direction descending.
  total = 0
  seekTime = 0
  seekDownCount = 0
  for x in requests:
    if(x<n):
      seekDownCount = seekDownCount + 1
  
  while(len(requests) > 0):
    nearest = math.inf
    if(seekDownCount > 0):
      for x in requests:
        if(((int(abs(n-x))) < (abs(n-nearest))) and (x < n)):
          nearest = x
      total = total + int(abs(n-nearest))
      n = nearest
      requests.remove(nearest)
      seekDownCount = seekDownCount - 1
    if(seekDownCount == 0):
      farthest = 0
      for x in requests:
        if((int(abs(n-x))) > farthest):
          farthest = x
      total = total + n + int(abs(4999 - farthest))
      n = farthest
      requests.remove(farthest)
      seekDownCount = seekDownCount - 1
    if(seekDownCount < 0):
      nearest = math.inf
      for x in requests:
        if((int(abs(n-x))) < (abs(n-nearest))):
          nearest = x
      total = total + int(abs(n-nearest))
      n = nearest
      requests.remove(nearest)
      seekDownCount = seekDownCount - 1
  seekTime = int(0.76 + (0.24 * math.sqrt(total)))
  global bestAlgorithm
  global bestTotal
  if(total < bestTotal):
    bestAlgorithm = 5;
    bestTotal = total
  print("C-Scan")
  print("=================================")
  print("Total cylinders traversed: ", total)
  print("Total seek time: ", seekTime, "milliseconds")
  print("=================================")
  print()
  
# C-Look algorithm. Similar to the look algorithm, except that when it reaches the lowest value in the work queue it immediately jumps to the highest value in the work queue. Once again the jump is not counted as read head movement making this algorithm extremely efficient.
def CLook(n,requests):# Read head direction descending
  total = 0
  seekTime = 0
  seekDownCount = 0
  for x in requests:
    if(x<n):
      seekDownCount = seekDownCount + 1
  
  while(len(requests) > 0):
    nearest = math.inf
    if(seekDownCount > 0):
      for x in requests:
        if(((int(abs(n-x))) < (abs(n-nearest))) and (x < n)):
          nearest = x
      total = total + int(abs(n-nearest))
      n = nearest
      requests.remove(nearest)
      seekDownCount = seekDownCount - 1
    if(seekDownCount == 0):
      farthest = 0
      for x in requests:
        if((int(abs(n-x))) > farthest):
          farthest = x
      n = farthest
      requests.remove(farthest)
      seekDownCount = seekDownCount - 1
    if(seekDownCount < 0):
      nearest = math.inf
      for x in requests:
        if((int(abs(n-x))) < (abs(n-nearest))):
          nearest = x
      total = total + int(abs(n-nearest))
      n = nearest
      requests.remove(nearest)
      seekDownCount = seekDownCount - 1
  seekTime = int(0.76 + (0.24 * math.sqrt(total)))
  global bestAlgorithm
  global bestTotal
  if(total < bestTotal):
    bestAlgorithm = 6
    bestTotal = total
  print("C-Look")
  print("=================================")
  print("Total cylinders traversed: ", total)
  print("Total seek time: ", seekTime, "milliseconds")
  print("=================================")
  print(best(bestAlgorithm))

r = generateRequests()
head = -1
while((head < 0) or (head > 4999)):
  head = int(input("Please enter a head cylinder between 0 and 4999 for the disk scheduling algorithm computatons: "))
FCFS(head, r[:])
SSTF(head, r[:])
Scan(head, r[:])
Look(head, r[:])
CScan(head, r[:])
CLook(head, r[:])
