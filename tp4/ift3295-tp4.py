#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

class node:
    next_unique_id = 0

    def __init__(self,content=None,parent=None,childrens=[]):
        self.parent = parent
        self.id = node.next_unique_id
        node.next_unique_id += 1
        self.content = content
        self.childrens = childrens
        self.sequence=[]


           
    def __str__(self):
        if self.content is None:
            return str(self.id) 
        else :
            return str(self.id) + " " + str(self.content)
            
    def sankoff(self,index):
        """ Implémentation de l'algorithme de Sankoff pour la parcimonie."""
        if len(self.childrens)==0:
            #retourne un vecteur ou tous les elements sont np. (infini) sauf l'index correspondant au caractère à l'index i
          
            nullindex = characters.index(self.sequence[index])
            w = np.array([np.inf if i != nullindex else 0 for i in range(len(characters))])
          
            return w
        else:
            sankoffList=[]
            for c in self.childrens:
                sankoffList.append(c.sankoff(index))
            assert len(sankoffList)==2
            sank=np.zeros(len(characters))
            for i in range(len(sank)):                
                #min_left=-1
                #definir fonction qui retourne le vecteur de transitions
                min_left=np.min(sankoffList[0]+mutations[i])            
                min_right=np.min(sankoffList[1]+mutations[i])
                sank[i] = min_left+min_right
            return sank
                        

class binary_tree:
    def __init__(self, newick_expr):
        self.leaves = []
        self.root = self._parse_newick(newick_expr)        
        self.reset()
        for i in self.leaves:
            i.sequence = getSequence(i.content)        

    def _parse_newick(self, expr, parent=None):
        """parse a newick tree expression to a binary_tree object."""
        if expr[0] == '(':
            assert expr[-1] == ')',"Erreur de parentheses"
            e = node(parent=parent)
            parCount=0
            for i in range(len(expr)):
                if(parCount==1 and expr[i]==','):
                    virgPos=i
                    break
                if(expr[i]=='('):
                    parCount+=1
                elif(expr[i]==')'):
                    parCount-=1
            a = expr[1:virgPos] #Trouver la virgule du milieu et se debarasser des parentheses.
            b = expr[virgPos+1:-1]
            
            a,b = self._parse_newick(a,e), self._parse_newick(b,e)        
            e.childrens = [a,b]
            return e
        else :
            e = node(expr,parent)
            self.leaves.append(e)
            return e 
        
    def reset(self):
        """ Lorsque appelé, cette fonction retourne la fringe à son état initial et ne considère aucun noeud comme étant visité. """
        self.search_fringe = list(self.leaves)
        self.checked = set() 
        self.last = None
    
    def __iter__(self):
        """ """
        return self

    def __next__(self):
        return self.next
    
    def next(self):
        """ renvoit le prochain noeud, """
        if self.last is not None and self.last.parent is not None:
        
            if all(i.id in self.checked for i in self.last.parent.childrens):
                self.search_fringe.append(self.last.parent)
                
        
        if len(self.search_fringe) == 0 :
            raise StopIteration
        else :
            self.last = self.search_fringe.pop(0)
            self.checked.add(self.last.id)
            return self.last        

    def pullSequences(self):
        i=0
        sequences=[]
        for leaf in self.leaves:
            strSeq=leaf.content
            sequences.append(getSequence(strSeq,p))
        return sequences

def getMutations():
	m = open('mutations.txt','rb')
	print(f[0])	

newick_trees = []

def getSequence(string):
    p.seek(0)	
    seq=''
    take=False
    for line in p:
	    if line[0]=='>':
		    if line[1:-1]==string:
			    take=True
		    else:
			    take=False
	    elif(take):
		    seq+=line[:-1]
    return seq
    
if __name__ == '__main__':
    global characters
    global mutations
    
    import sys
    print("arguments : "+str(sys.argv))

    #Loading proteine values
    p = open(sys.argv[1],'rb')



    #Loading and parsing newick trees
    f = open(sys.argv[2], 'rb')
    for line in f:

        if all([i in line for i in '(',',',')']):  
            line = line[:-3] #Stripping the line of ; and /n
            line = line.replace(' ','')
            newick_trees.append(binary_tree(line))            

    #Loading mutations values
    mut = open(sys.argv[3],'rb').read()
    lines = mut.split('\n')
    characters = lines[0].replace(' ','') #the global variable characters represent the alphabet we are working with. 

    #This part is to create numpy array of transition values accordingly to the mutatation.txt file 
    mutations = np.zeros((len(characters),len(characters)))    
    for y, i in enumerate(lines[1:]):
        #Thats kinda sketch but is there to remove multiple space
        last_len = len(i)+1
        actual_len = len(i)
        while last_len != actual_len :
            i = i.replace('  ', ' ')
            last_len = actual_len
            actual_len = len(i)
        #End of sketchy part             
        l = i.split(' ')
        mutations[y] = l[1:]

    #Preprocess to know the indexes where none of the sequences contains a hole '-'.
    sequences = [i.sequence for i in newick_trees[0].leaves]
    good_index = []
    for x in range(np.min([len(i) for i in sequences])):
        if all([s[x] != '-' for s in sequences]):
            good_index.append(x) 
    #print('goodindexes',good_index)    


    #Calculating the cost for all trees
    tree_cost = []
    for i,tree in enumerate(newick_trees):
        total_cost = 0
        for x in good_index:
            total_cost += np.min(tree.root.sankoff(x))
        print("Arbre "+str(i)+" : "+str(total_cost))
        tree_cost.append(total_cost)

    print("L'arbre "+str(np.argmin(tree_cost))+" est le meilleur des "+str(len(tree_cost))+" arbres en entrée.")
