import math
import random

inputnum = 3
hiddennum = 3
outputnum = 1

teachnum = 500 # loop num

eta = 0.9 # learning rate
alfa = 0.9 # innertia rate

nodes = []
wires = []
teach = [0,1,1,0]
input = [[0,0,1],[0,1,1],[1,0,1],[1,1,1]]

mod_output = 0


class node:
	def __init__(self, id, state, **kwargs):
		self.value = 0
		self.id = id
		self.state = state
		nodes.append(self)
		return super().__init__(**kwargs)

	def activateFunc(self, value):
		return 1 / (1 + math.exp(-value))

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
			return self.value * (1 - self.value) * (teach[teach_c] - self.value)
		if self.state == "hidden":
			return self.value * (1 - self.value) * modification_output(teach_c)

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
		return self.w * nodes[1].value

	def update(self, teach_c):
		temp = eta * self.nodes[1].modification(teach_c) * nodes[0].value + alfa * self.dw
		self.w += temp
		self.dw = temp



def modification_output(teach_c):
	sum = 0
	for w in wires:
		if w.nodes[1].state == "output":
			sum += w.w * w.nodes[1].modification(teach_c)
	return sum

def update(teach_c):
	for w in reversed(wires):
		w.update(teach_c)

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


def checkend():
	N = len(input)
	temp = 0
	for i in range(N):
		for n in nodes:
			if n.state == "output":
				input_output(i)
				temp += (teach[i] - n.value)**2

	temp = (temp / N)
	print("Error", temp)
	if temp <= 0.001:
		#before_e = temp / N
		return True
	return False


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
			elif n.state == "hidden" and n2.state == "output":
				wire(n,n2)


def debug_output():
	for n in nodes:
		print(n.id, n.value)


def result():
	for i in range(len(teach)):
		input_output(i)
		for n in nodes:
			if n.state == "output":
				print(i, n.value)

def result_wire():
    for e in wires:
        print(e.nodes[0].id + " , " + e.nodes[1].id + " , " + e.w)

# entry point

def main():
	createNodes()
	result()
	for i in range(teachnum):
		print("loop" , i)
		cnt = random.randint(0,len(teach) - 1)
		input_output(cnt)
		update(cnt)
		debug_output()
		if checkend():
			return 0
		


if __name__ == "__main__":
    main()
    result()
