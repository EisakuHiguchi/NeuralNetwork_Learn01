
import math
import struct
import random

class Node:
	state = ""
	def __init__(self,id, **kwargs):
		self.id = id
		self.wire = []
		self.value = 0
		self.bias = 0
		return super().__init__(**kwargs)

	def update(self):
		for w in self.wire:
			if w.nodes[1] == self:
				if self.state == "inner":
					w.update2(activateFunc(self.value))
				else:
					#w.update(activateFunc(w.w * self.value + self.bias))
					w.update(activateFunc(self.value))
					#w.update(self.value)

	def setWire(self, node):
		for n in node:
			w = Wire(self)
			w.setNode(n)
			self.wire.append(w)

	def setWireinst(self, wire):
		self.wire.append(wire)

	def output(self, node):
		for w in self.wire:
			if w.nodes[1]  == node:
				#return activateFunc(w.w * self.value + self.bias)
				return w.w * self.value + self.bias

	def initInput(self, inval):
		self.value = inval

	def innerInput(self):
		self.value = 0
		for w in self.wire:
			if w.nodes[1] == self:
				self.value += w.nodes[0].output(self)
		if self.state == "inner":
			self.value = activateFunc(self.value)

	def __cmp__(self, other):
		return self.id - other.id


class Wire:
	def __init__(self, node, **kwargs):
		self.w = random.uniform(0,3)
		self.rate = rate
		self.nodes = [node]
		return super().__init__(**kwargs)
	
	def setNode(self, node):
		self.nodes.append(node);
		node.setWireinst(self)

	def setWeight(self, val):
		self.w = val

	def update(self, val):
		self.w = self.w - rate * (val - output) * input

	def update2(self, val):
		n1 = self.nodes[1]
		n0 = self.nodes[0]
		self.w = self.w - rate * (n0.value - n1.value * self.w) * n1.value


# function

def activateFunc(u):
	try:
		res =  1 / (1 + math.exp(-u))
	except:
		res = 0
	return res
	
def updateNode(num):
	f = openData("t10k-images.idx3-ubyte")
	buf = f.read(16) # ヘッダ部分の読み込み
	f.read(28*28*(num-1))
	for n in nodes:
		if n.state == "input":
			buf = f.read(1)
			data = struct.unpack('B'*(len(buf)),buf)
			n.initInput(data[0])

	for n in nodes:
		n.innerInput()
	output = getLabel(num)
	for n in nodes:
		n.update()
	f.close()

def getLabel(num):
	labelFile = open("t10-labels.txt");
	for i in range(num):
		label = labelFile.readline()
	labelFile.close()
	return int(label)

def openData(filename):
	f = open(filename,'rb')
	#f.read(16) # ヘッダ部分の読み込み
	return f

def outputprint():
	for n in nodes:
		if n.id > (inputNum + innerNum):
			print(n.id, n.value)
			#for w in n.wire:
			#	print(" ", " ", w.w)


# main

input = 2
outputNum = 4
rate = 0.3
inputRow = 28
inputCol = 28
layer = 3
innerNum = 50
inputNum = inputRow * inputCol
output = 0

loopnum = 50

nodes = []

for i in range(inputNum + innerNum + outputNum):
	n = Node(i)
	nodes.append(n)

f = openData("t10k-images.idx3-ubyte")

for n in nodes:
	if n.id < inputNum:
		n.state = "input"
		for i in range(innerNum):
			n.setWire([nodes[i + inputNum]])

	elif n.id < (inputNum + innerNum):
		n.state = "inner"		
		for i in range(outputNum):
			n.setWire([nodes[i + inputNum + innerNum]])

	else:
		n.state = "output"

f.close()

#for i in nodes:
#for j in range(inputNum):
#	i = nodes[j]
#	print(i.id , i.state, i.value)
	#for w in i.wire:
	#	print("	",w.nodes[0].id, w.nodes[1].id)

for i in range(loopnum):
	print("loop " , i +1)
	updateNode(1)
	outputprint()
