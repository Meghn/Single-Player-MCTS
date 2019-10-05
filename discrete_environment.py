import numpy as np
import itertools as iter
import copy

volume = 10.0

class State:
	def __init__(self, items, bins):
		self.items = items
		self.bins = bins

def get_next_state(current_state):
	#actions = GetActions(current_state)
	Bins = current_state.bins
	current_bin_volume = sum(Bins[-1])
	pos = [-1.0]
	if(current_bin_volume == volume):
		actions = pos
	else:
		for i in range(len(current_state.items)):
			if(current_bin_volume + current_state.items[i] <= volume):
				pos.append(i)
		actions = pos
	i = np.random.randint(0, len(actions))
	Action = actions[i]
	#next_state = ApplyAction(current_state, Action)
	Items = current_state.items[:]
	Bins = copy.deepcopy(current_state.bins[:])
	if(Action == -1.0):
		Bins.append([])
	else:
		Bins[-1].append(Items[Action])
		del Items[Action]
	next_state = State(Items,Bins)
	return next_state

def eval_next_state(current_state):
	Bins = current_state.bins
	current_bin_volume = sum(Bins[-1])
	pos = [-1.0]
	if(current_bin_volume == volume):
		actions = pos
	else:
		for i in range(len(current_state.items)):
			if(current_bin_volume + current_state.items[i] <= volume):
				pos.append(i)
		actions = pos
	next_states = []
	for i in range(len(actions)):
		Action = actions[i]
		Items = current_state.items[:]
		Bins = copy.deepcopy(current_state.bins[:])
		if(Action == -1.0):
			Bins.append([])
		else:
			Bins[-1].append(Items[Action])
			del Items[Action]
		next_state = State(Items,Bins)
		next_states.append(next_state)
	if(actions == []):
		Items = current_state.items[:]
		Bins = copy.deepcopy(current_state.bins[:])
		if(actions == -1.0):
			Bins.append([])
		else:
			Bins[-1].append(Items[actions])
			del Items[actions]
		next_state = State(Items,Bins)
		next_states.append(next_state)
	return next_states

def is_terminal(State):
	if(sum(State.items) == 0.0):
		return True
	else:
		return False

def get_result(current_state):
	Opt = 5.0
	return 5000.0 * Opt/len(current_state.bins)
