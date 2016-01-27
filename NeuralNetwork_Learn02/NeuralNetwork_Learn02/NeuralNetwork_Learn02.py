import math
import random

inputnum = 3
hiddennum = 3
outputnum = 1

#teachnum = 20000 # loop num
error = 0.1

eta = 0.9 # learning rate
alfa = 0.1 # innertia rate

nodes = []
wires = []
teach = [0,1,1,0]
input = [[0,0,1],[0,1,1],[1,0,1],[1,1,1]]

class node:
	def __init__(self, id, state, **kwargs):
		self.value = 0
		self.id = id
		self.state = state
		nodes.append(self)
		return super().__init__(**kwargs)

	def activateFunc(self, value):
		return 1.0 / (1.0 + math.exp(-1 * value))

	def output(self):
		if self.state != "input":
			sum = 0
			for w in wires:
				if w.nodes[1].id == self.id:
					sum += w.output()
			self.value = self.activateFunc(sum)

	def input(self, value):
		self.value = value

	def modification(self, teach_c):
		if self.state == "output":
			return self.value * (1.0 - self.value) * (teach[teach_c] - self.value)
		if self.state == "hidden":
			return self.value * (1.0 - self.value) * modification_output(teach_c, self)

	def update(self, teach_c):
		for w in wires:
			if w.nodes[0].id == self.id:
				w.w += alfa * w.nodes[1].modification(teach_c) * self.value

	def output_debug(self):
		if self.state != "input":
			sum = 0
			for w in wires:
				if w.nodes[1].id == self.id:
					sum += w.output()
			print("sum : " + str(self.id) + "  " + str(sum))
			self.value = self.activateFunc(sum)
			print("act : " + str(self.id) + "  " + str(self.value))

class wire:
	def __init__(self, node1 , node2, **kwargs):
		self.nodes = []
		self.nodes.append(node1)
		self.nodes.append(node2)
		self.w = random.uniform(0,1)
		self.dw = 0
		wires.append(self)
		return super().__init__(**kwargs)

	def output(self):
		return self.w * self.nodes[0].value

	def update(self, teach_c):
		#temp = eta * self.nodes[1].modification(teach_c) * self.nodes[0].value + alfa * self.dw
		
		temp = alfa * self.nodes[1].modification(teach_c) * self.nodes[0].value
		self.w += temp
		self.dw = temp



def modification_output(teach_c, node):
	sum = 0
	for w in wires:
		if w.nodes[1].state == "output" and w.nodes[0].id == node.id:
			sum += w.w * w.nodes[1].modification(teach_c)
	return sum

def update(teach_c):
	#for w in reversed(wires):
	#	w.update(teach_c)
	for n in reversed(nodes):
		n.update(teach_c)

def input_output(teach_c):
	cnt = 0
	for n in nodes:
		if n.state == "input":
			n.input(input[teach_c][cnt])
			cnt += 1
			if cnt > 2:
				cnt = 0

	for n in nodes:
		n.output()

def debug_input_output(teach_c):
	cnt = 0
	for n in nodes:
		if n.state == "input":
			n.input(input[teach_c][cnt])
			cnt += 1
			if cnt > 2:
				cnt = 0

	for n in nodes:
		n.output_debug()

def getError():
	N = len(input)
	temp = 0
	for i in range(N):
		input_output(i)
		for n in nodes:
			if n.state == "output":
				temp += math.pow((teach[i] - n.value),2)

	#temp = (temp / N)
	temp *= 0.5
	return temp


def createNodes():
	id = 0;
	for i in range(inputnum):
		n = node(id,"input")
		id += 1
	for i in range(hiddennum):
		n = node(id,"hidden")
		id += 1
	for i in range(outputnum):
		n = node(id, "output")
		id += 1

	for n in nodes:
		for n2 in nodes:
			if n.state == "input" and n2.state == "hidden":
				wire(n,n2)
	for n in nodes:
		for n2 in nodes:
			if n.state == "hidden" and n2.state == "output":
				wire(n,n2)


def debug_output():
	for n in nodes:
		print(n.id, n.value)

def debug_inout(teach_c):
	print("in " , input[teach_c] , " out ", nodes[len(nodes)-1].value , " Error " , getError())


def debug_wirein(value):
	cnt = value.count
	c = 0
	for w in wires:
		w.w = value[c]

	


def result():
	for i in range(len(teach)):
		input_output(i)
		for n in nodes:
			if n.state == "output":
				print(i, n.value)

def result_wire():
    for e in wires:
        print(str(e.nodes[0].id) + " , " + str(e.nodes[1].id) + " , " + str(e.w))

# entry point

def main():
	createNodes()
	result()
	j = 0
	#for i in range(teachnum):
	while(True):
		#print("loop" , i)
		cnt = random.randint(0,len(teach) - 1)
		input_output(cnt)
		update(cnt)
		#debug_output()
		debug_inout(cnt)
		j += 1
		if getError() < error:
			print ("loop: " , j)
			return 0
		


if __name__ == "__main__":
    main()
    result()
    result_wire()