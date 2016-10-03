class Node:
    def __init__(self,ident,label):
        self.ident = ident
        self.label = label
        self.children = []

    def __repr__(self):
        return "Node({0}, {1})".format(self.ident,self.label)

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
            

    def print(self):
        for n in self.nodes:
            self.print_node(n,"  ")

    def print_node(self,n,odsazeni):
        print(odsazeni + " - " + str(n.ident))
        for ch in n.children:
            self.print_node(ch,odsazeni + "  ")
            

if __name__ == "__main__":
    tr = Tree()
    tr.add_node(Node(1,"node_1"))
    tr.add_node(Node(2,"node_2"))
    tr.add_node(Node(3,"sub_1_node_1"),1)
    tr.add_node(Node(4,"sub_2_node_1"),1)
    tr.add_node(Node(5,"sub_1_node_2"),2)
    tr.add_node(Node(6,"sub_2_node_2"),2)
    tr.add_node(Node(7,"sub_sub_1"),3)
    tr.add_node(Node(8,"sub_sub_2"),5)
    tr.add_node(Node(9,"sub_sub_1"),7)
    tr.add_node(Node(10,"sub_sub_2"),6)
    tr.print()
    print("done")
    
    
            
