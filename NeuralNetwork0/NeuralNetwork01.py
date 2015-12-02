
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
		temp = 0
		if self.state == "output":
			for w in self.wire:
				if w.nodes[1] == self:
					temp = w.back_output()
		
		for w in self.wire:
			if w.nodes[1] == self:
				if self.state == "inner":
					w.update(temp)
				elif self.state == "output":
					w.update(0)

	def setWire(self, node):
		for n in node:
			w = Wire(self)
			w.setNode(n)
			self.wire.append(w)
			wires.append(w)

	def setWireinst(self, wire):
		self.wire.append(wire)

	def output(self):
		if self.state != "input":
			put = 0
			for w in self.wire:
				put += w.output_fromNode(self)
			self.value = activateFunc(put)
		return self.value

	def initInput(self, inval):
		self.value = inval

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

	def update(self, sum):
		n0 = self.nodes[0].value
		n1 = self.nodes[1].value
		
		if self.nodes[0].state == "input":
			#self.w = self.w - rate * (n1 - self.output()) * self.output()
			self.w = self.w + eta * (n1 * (1 - n1) * sum) * n0 + rate * self.w
		elif self.nodes[0].state == "inner":
			#self.w = self.w - rate * (n1 - teach) * self.output()
			self.w = self.w + eta * (n1 * (1 - n1) * (teach - n1)) * n0 + rate * self.w

	def back_output(self):
		return self.nodes[1].value * self.w

	def output(self):
		return self.nodes[0].value * self.w

	def output_fromNode(self, node):
		if node.state == self.nodes[1].state:
			return self.output()
		return 0


# function

def activateFunc(u):
	try:
		res =  1 / (1 + math.exp(-u))
	except:
		res = 0
	return res

def dataInput(num):
	f = openData("t10k-images.idx3-ubyte")
	buf = f.read(16) # ヘッダ部分の読み込み
	f.read(28*28*(num-1))
	for n in nodes:
		if n.state == "input":
			buf = f.read(1)
			data = struct.unpack('B'*(len(buf)),buf)
			n.initInput(data[0])

	for n in nodes:
		n.output()

	for n in reversed(nodes):
		n.update()

	
def updateNode(num):
	dataInput(num)	
	teach = getLabel(num)

	for n in reversed(nodes):
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

def outputprint(flag):
	if flag == 0:
		for w in wires:
			if w.nodes[1].state == "output":
				print(w.w)
	elif flag == 1:
		for n in nodes:
			if n.id >= (inputNum + innerNum):
				print(n.id, n.value)
				

# main


inputRow = 28
inputCol = 28
innerNum = 50
inputNum = inputRow * inputCol
outputNum = 1

rate = 0.03
eta = 0.1
teach = 0

loopnum = 10

debugFlag = 1

nodes = []
wires = []

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

for i in range(loopnum):
	print("loop " , i +1)
	updateNode(1)
	outputprint(debugFlag)


print("")
dataInput(2)
outputprint(debugFlag)
