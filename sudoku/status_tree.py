class Node:
    def __init__(self,ident,label):
        self.ident = ident
        self.label = label
        self.children = []
        self.done = False

    def __repr__(self):
        return "Node({0}, {1})".format(self.label,str(self.done))

class Tree:
    def __init__(self):
        self.nodes = []

    def add_node(self,node,parent_id=None):
        if not parent_id:
            self.nodes.append(node)
        else:
            parent = self.find_in_nodes(self.nodes,parent_id)
                
            if parent:
                parent.children.append(node)
            else:
                raise ValueError("Node not found (" + str(parent_id) + ")")

    def find_in_nodes(self,nodes,parent_id):
        if len(nodes) == 0:
            return None
        for n in nodes:
            if n.ident == parent_id:
                return n
            found = self.find_in_nodes(n.children,parent_id)
            if found:
                return found

        return None

    def find_nodes_by_filter(self,filter):
        selected = []
        self._find_last_done_in_nodes(filter,n.children,selected)
        

    def get_node_depth(self,node):
        depth = 0
        children = self.nodes
        while children != None

    def _find_last_done_in_nodes(self,filter,nodes,selected):
        for n in nodes:
            if filter in str(n):
                selected.append(n)
            if n.children:
                self._find_last_done_in_nodes(filter,n.children,selected)    
            
    def print(self):
        for n in self.nodes:
            self.print_node(n,"  ")

    def print_node(self,n,odsazeni):
        print(odsazeni + " - " + str(n))
        for ch in n.children:
            self.print_node(ch,odsazeni + "  ")
