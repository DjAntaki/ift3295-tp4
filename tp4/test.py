
class node:
    next_unique_id = 0

    def __init__(self,content=None,parent=None,childrens=[]):
        
        if parent is not None:
            parent.childrens.append(self)
        self.parent = parent
        
        self.id = node.next_unique_id
        node.next_unique_id += 1
        self.content = content
        self.childrens = childrens


class binary_tree:
    def __init__(self, newick_expr):
        self.leafs = []
        self.root = self._parse_newick(newick_expr)        
        self.reset()

    def _parse_newick(self, expr, parent=None):
        """parse a newick tree to this representation"""
        if expr[0] == '(':
            assert expr[-1] == ')'
            e = node(parent=parent)
            #a,b = expr.split(',') Trouver la virgule du milieu et se débarasser des parenthèses.
            a,b = self.parse_newick(a,e), self.parse_newick(b,e)        
            return e
        else :
            e = node(expr,parent)
            self.leafs.append(e)
            return e 
        
    def reset(self):
        self.search_fringe = self.leafs.copy()
        self.checked = set() 
    
    def __next__(self):
        if self.last is not None :
            if all(i.id in self.checked for i in self.last.parent.childrens):
                self.search_fringe.append(self.last.parent)
                
        if len(self.search_fringe) == 0 :
            yield None
        else :
            self.last = self.search_fringe.pop(0)
            self.checked.add(self.last.id)
            yield self.last        

newick_trees = []

if __name__ == '__main__':

    import sys
    print("arguments :")
    print(sys.argv)
    f = open(sys.argv[1], 'rb')
    n = f.readline()
    for line in f:
        line = line[:-3] #Stripping the line of ; and /n
        print(line)
        newick_trees.append(binary_tree(line))            
            
#    w = sys.argv[2]

