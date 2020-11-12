'''
Name: Josh Musgrave
Date: Nov 11 2020
CS 3530 - Design and Analysis of Algorithms
Bubble, Merge, and Heap sort assignment
'''

import time
import random

def generateArray(size):
	'''
	Takes an int as input and generates an array of that size with random 
	numbers from 1 to 100,000
	'''

	array = []
	for i in range(size):
		array.append(random.randint(0,100000))
		
	return array

def bubble(inputArray):
	'''
	Takes in an unsorted array
	Returns a tuple containing the sorted array and the number of comparisons 
	during the sort
	'''
	
	compareCount = 0

	'''
	The outer for loop counts down to limit the inner loop
	After the first pass the highest value in the array will be at the end
	There is no need to compare with that value so we can stop the inner loop
	when it gets there
	'''
	for i in range(len(inputArray)-1,0,-1):
		for j in range(i):
			compareCount += 1
			if inputArray[j]>inputArray[j+1]:
				temp = inputArray[j+1]
				inputArray[j+1] = inputArray[j]
				inputArray[j] = temp
		
	return inputArray, compareCount

def merge(inputArray, compareCount):
	'''
	Takes in an unsorted array and the running total for comparisons made
	during runtime. The comparisons must be passed to the function
	because it is called recursively
	'''

	#If array contains one element, it sorted and can be returned as-is
	if len(inputArray) == 1:
		return inputArray, compareCount

	sortedArray = []
	midpoint = len(inputArray) // 2

	#The array is split into two pieces about a midpoint
	arrayA = inputArray[:midpoint]
	arrayB = inputArray[midpoint:]

	#Each smaller array is recursively passed to merge()
	arrayTupleA = merge(arrayA, compareCount)
	arrayTupleB = merge(arrayB, compareCount)

	arrayA = arrayTupleA[0]
	arrayB = arrayTupleB[0]

	compareCount = arrayTupleA[1] + arrayTupleB[1]

	#The 0th elements of both arrays are compared and the lowest one is added
	#to sortedArray until one array is empty
	while (len(arrayA) > 0) and (len(arrayB) > 0):
		compareCount += 1
		if arrayA[0] < arrayB[0]:
			sortedArray.append(arrayA.pop(0))
		else:
			sortedArray.append(arrayB.pop(0))
	
	#The remainder of the non-empty array can then be added to sortedArray
	sortedArray = sortedArray + arrayA + arrayB
	
	return sortedArray, compareCount

def heapify(array, index, compareCount):
	'''
	Takes in an array to 'heapify', the index that needs to be checked, and
	the running total of comparisons
	Returns only compareCount since the array is changed without returning it
	'''
	
	k = index
	value = array[index]

	heap = False

	#2*k+1 is the index of the node's child. if that exceeds the length of the
	#array, the node is not a parent and algorithm is done with this node
	while not heap and 2*k+1 <= len(array)-1:
		j = 2*k+1

		#if j = len(array)-1, it is an only child so it also the greatest child
		if j < len(array)-1:
			compareCount += 1
			#The algorithm must compare a parent to the greatest of its two children
			if array[j] < array[j+1]:
				j = j + 1
		compareCount += 1
		if value >= array[j]:
			heap = True
		else:
			array[k] = array[j]
			k = j
	array[k] = value
	return compareCount

def heap(inputArray):
	compareCount = 0
	sortedArray = []
	#n / 2 - 1 is the first parent so that's where we start our HeapBottomUp
	for i in range(len(inputArray) // 2 - 1, -1, -1):
		compareCount = heapify(inputArray, i, compareCount)

	#Now that the array is a heap, the highest value is at the 0 index
	for i in range(len(inputArray)):
		#We can pop that and put it in our sorted array
		sortedArray = [inputArray.pop(0)] + sortedArray
		if len(inputArray) > 0:
			#The value at the end of the array is now placed at the 0 index
			inputArray = [inputArray.pop()] + inputArray
			#And use heapify to make the array a heap again
			compareCount = heapify(inputArray, 0, compareCount)
		
	return sortedArray, compareCount

def main():
	arraySize = int(input("How many elements would you like in your array? "))
	unsortedArray = generateArray(arraySize)
	unsortedBubble = unsortedArray[:]
	unsortedMerge = unsortedArray[:]
	unsortedHeap = unsortedArray[:]

	print("*****Testing sorts with",arraySize,"items*****")
	start = time.perf_counter()
	bubbleTuple = bubble(unsortedBubble)
	bubbleEnd = round(time.perf_counter() - start, 4)
	print("Bubble -",bubbleEnd,"seconds.",bubbleTuple[1],"comparisons.")

	start = time.perf_counter()
	mergeTuple = merge(unsortedMerge, 0)
	mergeEnd = round(time.perf_counter() - start, 4)
	
	print("Merge  -",mergeEnd,"seconds.",mergeTuple[1],"comparisons.")

	start = time.perf_counter()
	heapTuple = heap(unsortedHeap)
	heapEnd = round(time.perf_counter() - start, 4)
	print("Heap   -",heapEnd,"seconds.",heapTuple[1],"comparisons.")
	print()

	if bubbleTuple[0] == mergeTuple[0]:
		#we don't have to check if merge == heap because bubble == merge 
		if bubbleTuple[0] == heapTuple[0]:
			print(bubbleTuple[0][:20])
			print(mergeTuple[0][:20])
			print(heapTuple[0][:20])
		else:
			print("Bubble array doesn't equal Heap array.")
	else:
		print("Bubble array doesn't equal Merge array.")
	
	print("*****End of tests with",arraySize,"items*****")
	print()
	
main()
