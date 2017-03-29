# Copyright (C) 2011 by Henry Yuen, Joseph Bebel

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


# Random kSat Routine
# written by Henry Yuen

# for ToughSat Project


import math
import copy
import sys
import shutil
import gc
import random


verbose = 0
testing = 0

assignment = {}

n = 5
formula = []

vars = {}
postfix_counter = 0

def make_var():
	global vars
	global postfix_counter
	postfix_counter = postfix_counter + 1
	if postfix_counter%10000 == 0:
		print postfix_counter
	
	return "X" + str(postfix_counter)

def make_conj(exprs):
	conj = ["&"]
	for e in exprs:
		conj.append(copy.copy(e))
	return conj
	
def make_disj(exprs):
	conj = ["V"]
	for e in exprs:
		conj.append(copy.copy(e))
	return conj

def make_neg(expr):
	conj = ["neg",copy.copy(expr)]
	return conj

#def make_val(v):
#	return ["val",v]
	
def make_iff(e1,e2):
	#same as equals, essentially
	return ["<->",copy.copy(e1),copy.copy(e2)]

def make_xor(e1,e2):
	#pos = make_conj([e1,make_neg(e2)])
	#neg = make_conj([e2,make_neg(e1)])
	#return make_disj([pos,neg])
	return ["+",copy.copy(e1),copy.copy(e2)]

def allocate_var(name,num):
	global vars
	vars[name] = []
	for i in range(num):
		varname = make_var()
		vars[name].append(["var",varname])

def measure_formula(formula):
	count = 0
	if formula[0] != "var" and formula[0] != "val":
		for i in range(1,len(formula)):
			count += measure_formula(formula[i])
	else:
		return 1
		
	return count

def print_formula(formula):
	s = ""
	t = formula[0]
	if t == "val":
		if formula[1] == 1:
			s += "T"
		else:
			s += "F"
	if t == "neg":
		s += "~"
		if formula[1][0] != "var":
			s += "("
			
		s += print_formula(formula[1])
		
		if formula[1][0] != "var":
			s += ")"
	
	
	if t == "<->":	#iff
		s += "("
		s += print_formula(formula[1])
		s += " <--> "
		s += print_formula(formula[2])
		s += ")"
	
	
	if t == "+":	#iff
		s += "("
		s += print_formula(formula[1])
		s += " + "
		s += print_formula(formula[2])
		s += ")"
	
	
	if t == "var":
		s += formula[1]
	if t == "V":
		s += "("
		for j in range(1,len(formula)-1):
			s += print_formula(formula[j])
			s += " V "
		s += print_formula(formula[len(formula)-1])
		s += ")"
	if t == "&":
		s += "("
		for j in range(1,len(formula)-1):
			s += print_formula(formula[j])
			s += " & "
		s += print_formula(formula[len(formula)-1])
		s += ")"
	
	return s

def evaluate_formula(formula,assignment):
	#print formula
	t = formula[0]
	if t == "val":
		return formula[1]
	if t == "neg":
		return (evaluate_formula(formula[1],assignment) + 1) % 2
	if t == "var":
		return assignment[formula[1]]
	if t == "V":
		for j in range(1,len(formula)):
			v = evaluate_formula(formula[j],assignment)
			if v == 1:
				return 1
		
		return 0
		
	if t == "&":
		for j in range(1,len(formula)):
			v = evaluate_formula(formula[j],assignment)
			if v == 0:
				return 0
		
		return 1
	if t == "+":
		v1 = evaluate_formula(formula[1],assignment)
		v2 = evaluate_formula(formula[2],assignment)
		
		return (v1 + v2) % 2
		
	if t == "<->":
		v1 = evaluate_formula(formula[1],assignment)
		v2 = evaluate_formula(formula[2],assignment)
		
		return (1 + v1 + v2) % 2
		
	return 0
	

	


		
#convert to CNF
def distribute_negs(formula):
	#print formula
	t = formula[0]
	if t == "neg":
		if formula[1][0] == "val":
			formula[1][1] = (formula[1][1]+1)%2	#negate the value
			formula = formula[1]
		elif formula[1][0] == "neg":
			#undo negation
			formula = formula[1][1]
		elif formula[1][0] in ["&","V"]:
			#distribute over
			if formula[1][0] == "&":
				formula[1][0] = "V"
			else:
				formula[1][0] = "&"
			
			for i in range(1,len(formula[1])):
				formula[1][i] = make_neg(formula[1][i])
			
			formula = formula[1]
		elif formula[1][0] in ["<->"]:
			#change it to xor
			formula[1][0] = "+"
			formula = formula[1]
			
		elif formula[1][0] in ["+"]:
			#change it to xor
			formula[1][0] = "<->"
			formula = formula[1]

	#it may have changed
	t = formula[0]
	if t == "val":
		return formula

	if t == "var":
		return formula
	
	for i in range(1,len(formula)):
		formula[i] = distribute_negs(formula[i])
	
	return formula


def variabilize_values(formula):
	t = formula[0]
	if t == "var":
		return formula
	
	if t == "val":
		return vars["constants"][formula[1]]
	
	for i in range(1,len(formula)):
		formula[i] = variabilize_values(formula[i])
		
	return formula

def associatize(formula):
	threshold = 3
	t = formula[0]
	if t in ["&","V"]:
		if len(formula) > threshold:
			sub_formula = [t]
			sub_formula.extend(formula[threshold-1:])
			#formula = [t,formula[1],sub_formula]
			temp_formula = [t]
			temp_formula.extend(formula[1:threshold-1])
			temp_formula.append(sub_formula)
			formula = temp_formula
	
	if t not in ["val","var"]:
		for i in range(1,len(formula)):
			formula[i] = associatize(formula[i])
	
	return formula
	
#auxiliary helper function
#to take a formula in a tree structure (consisting of AND and OR and IFF and XOR operations only)
#and assign every internal node a dummy variable
def flatten_formula_tree(formula,nodevar):
	t = formula[0]
	
	flattened_subtree = []
	flattened_clause = []
	
	if t in ["&","V","<->","+"]:
		flattened_clause = [t]
		for i in range(1,len(formula)):
			e = formula[i]
				
			#check if we have to create new variables (we have encountered a leaf or an internal node)
			if e[0] in ["&","V","<->","+"]:
				e_nodevar = ["var",make_var()]
				flattened_clause.append(e_nodevar)
				
				#now we flatten this branch of the tree
				flattened_subtree.extend(flatten_formula_tree(e,e_nodevar))
			else:
				flattened_clause.append(e)	#e1 is either neg or var
	else:
		return []

	#so now our clause looks like: v1 <-> (v2 & v3 & ...)
	
	flattened_subtree.append(["<->",nodevar,flattened_clause])
	return flattened_subtree
			
		
def convert_1_to_3(expr):
	#create auxiliary variables
	v1 = ["var",make_var()]
	v2 = ["var",make_var()]
	v1_neg = make_neg(v1)
	v2_neg = make_neg(v2)
	
	return [make_disj([expr,v1,v2]),	\
			make_disj([expr,v1,v2_neg]),	\
			make_disj([expr,v1_neg,v2]),	\
			make_disj([expr,v1_neg,v2_neg])]


#extract all the variables present in a clause
#assuming all we have are <->, &, V, negs, and vars
def extract_variables(formula):
	if formula[0] == "var":
		return [formula[1]]
	
	v = []
	for i in range(1,len(formula)):
		v2 = extract_variables(formula[i])
		for u in v2:
			if u not in v:
				v.append(u)
	return v
	
def write_cnf_clauses_to_dimacs(clauses):
	output = ""
	for clause in clauses:
		s = ""
		t = clause[0]
		
		if t in ["&","V"]:	
			for i in range(1,len(clause)):
				t = clause[i][0]
				if t == "neg":
					s += "-" + str(clause[i][1][1][1: ]) + " "
				else:	#it's a var
					s += str(clause[i][1][1:]) + " "
		elif t in ["neg"]:
			s += "-" + str(clause[1][1][1: ]) + " "
		elif t in ["var"]:
			s += str(clause[1][1:]) + " "
		
		
		s += "0\n"
		output += s
	
	return output
	
def convert_clause_to_cnf(clause):
	#otherwise, make truth table!
	#extract the variables in this clause
	vs = extract_variables(clause)
	#create all possible assignments for the v's
	cnf_clauses = []
	
	for j in range(2**len(vs)):
		temp_assgn = {}
		v = []
		
		for k in range(len(vs)):
			bit = (j >> k) % 2
			temp_assgn[vs[k]] = bit
			if bit == 0:
				v.append(["var",vs[k]])
			else:
				v.append(make_neg(["var",vs[k]]))
		
		#test the truth assignment
		val = evaluate_formula(clause,temp_assgn)
		
		#if we have a 0, we have winner winner chicken dinner
		if val == 0:
			cnf_clauses.append(make_disj(v))	
	
	return cnf_clauses

def convert_4cnf_to_3cnf_efficient(formula):
	#takes a 4cnf clause and converts it to 3cnf
	#print print_formula(formula)
	dummyvar = ["var",make_var()]
	
	cnf_clauses = []

	part1 = formula[0:3]
	part1.append(dummyvar)
	
	#print print_formula(part1)
	cnf_clauses.append(part1)
	
	part2 = ["<->",dummyvar,["V"] + formula[3:5]]
	#print print_formula(part2)
	cnf_clauses.extend(convert_clause_to_cnf(part2))
	
	return cnf_clauses

	
def convert_to_3cnf_canonical(formula):
	#formula = distribute_negs(formula)
	#print print_formula(formula)
	formula = associatize(formula)

	#now that we've variabilized the values
	#and we've distributed the negs
	#and we've associatized
	#we're ready to rock and roll - convert to 3CNF baby!
	#print print_formula(formula)
	
	#our input formula is in a tree data structure now
	#give dummy variables to all the internal nodes
	root_nodevar = ["var",make_var()]
	clauses = flatten_formula_tree(formula,root_nodevar)
	
	#print print_formula(make_conj(clauses))
	
	#now, we can convert each clause
	#to CNF
	#add the root nodevar
	cnf_clauses = convert_1_to_3(root_nodevar)
	#cnf_clauses = [root_nodevar]
	
	for i in range(len(clauses)):
		clause = clauses[i]
		#if the clause is already disjunctive then we're fine
		if clause[0] == "V":
			cnf_clauses.append(clause)
			continue
		
		cnf_clauses.extend(convert_clause_to_cnf(clause))
	
	#write_cnf_clauses_to_file(fh,cnf_clauses)
	return cnf_clauses

def convert_to_3cnf_efficient(formula):
	t = formula[0]
	
	#print print_formula(formula)
	
	if t in ["var","neg"]:
		return convert_1_to_3(formula)
	
	if t in ["&"]:
		return convert_to_3cnf_canonical(formula)
	
	#we're of the "V" type now
	l = len(formula)
	
	if l == 2:
		return convert_1_to_3(formula[1])
		
	if l == 3:
		return convert_2_to_3(formula[1],formula[2])
		
	if l == 4:
		return [formula]	#is already in 3CNF form
	
	if l == 5:
		return convert_4cnf_to_3cnf_efficient(formula)
	

	return convert_to_3cnf_canonical(formula)
	
#=============================================================================================================
#
#
#						MAIN FACTORING CODE
#
#
#
#=============================================================================================================
def halt():
	a = 0
	b = 3/a

def generate_instance(NUM_CLAUSES,NUM_VARIABLES,LIT_PER_CLAUSE,op_3cnf):
	global formula
	global vars
	global postfix_counter
	global num_clauses
	
	formula = []

	vars = {}
	postfix_counter = 0

	num_clauses = 0
	
	allocate_var("v",NUM_VARIABLES)

	formula = []

	for i in range(NUM_CLAUSES):
		lits = []
		vs = random.sample(xrange(NUM_VARIABLES),LIT_PER_CLAUSE)
		for j in range(LIT_PER_CLAUSE):
			if random.random() > 0.5:
				lits.append(vars["v"][vs[j]])
			else:
				lits.append(make_neg(vars["v"][vs[j]]))
			
		formula.append(make_disj(lits))
		
	if op_3cnf:
		cnf_clauses = []
		for f in formula:
			g = convert_to_3cnf_efficient(f)
			#g = convert_4cnf_to_3cnf_canonical(f)
			
			cnf_clauses.extend(g)
			#cnf_clauses.append(f)
			#print print_formula(make_conj(g))
			#break
		formula = cnf_clauses
		
	#halt()
		
	#print print_formula(make_conj(cnf_clauses))

	num_clauses = len(formula)
	num_variables = postfix_counter

	output = "c A SAT instance generated from a " + str(LIT_PER_CLAUSE) + "-CNF formula that had " + str(NUM_CLAUSES) + " clauses and " + str(NUM_VARIABLES) + " variables\n"
	output += "p cnf " + str(num_variables) + " " + str(num_clauses) + "\n"
	output += write_cnf_clauses_to_dimacs(formula)
	return output

	
def main():
	#generate partial product sums
	args = sys.argv

	if len(args) != 6:
		print "Usage: random_ksat.py <k> <numvars> <numclauses> <op_3cnf> <outputfile>"
		return

	k = int(args[1])
	numvars = int(args[2])
	numclauses = int(args[3])
	op_3cnf = args[4] == "1"
	
	output = generate_instance(numclauses,numvars,k,op_3cnf)
	
	f = open(args[5],"w")
	f.write(output)
	f.close()
	

if __name__ == '__main__':
    main()


