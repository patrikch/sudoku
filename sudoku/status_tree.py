class Node:
    def __init__(self,ident,label):
        self.ident = ident
        self.label = label
        self.children = []
        self.done = False
        self.level = 0

    def __repr__(self):
        return "Node({0}, done={1})".format(self.label,str(self.done))


class Tree:
    def __init__(self):
        self.nodes = []

    def add_node(self, node, parent_id=None):
        if not parent_id:
            self.nodes.append(node)
        else:
            parent = self.find_in_nodes(self.nodes, parent_id)
                
            if parent:
                node.level = parent.level + 1
                parent.children.append(node)
            else:
                raise ValueError("Node not found (" + str(parent_id) + ")")

    def find_in_nodes(self, nodes, wanted_id):
        if len(nodes) == 0:
            return None
        for n in nodes:
            if n.ident == wanted_id:
                return n
            found = self.find_in_nodes(n.children, wanted_id)
            if found:
                return found

        return None

    def find_lowest_node_matching_filter(self,filter):
        selected = []
        self._find_all_nodes_matching_filter(filter,self.nodes,selected)
        #just log
        for sn in selected:
            print(str(sn) + ",level=" + str(sn.level))
        #find biggest depth
        biggest = max(sn.level for sn in selected)
        print("biggest=" + str(biggest))
        biggest_nodes = [sn for sn in selected if sn.level == biggest]
        if len(biggest_nodes) > 0:
            return biggest_nodes[0]
        return None

    def _find_all_nodes_matching_filter(self,filter,nodes,selected):
        for n in nodes:
            if filter in str(n):
                selected.append(n)
            if n.children:
                self._find_all_nodes_matching_filter(filter,n.children,selected)    

    def find_sibling_matching_filter(self,node,filter):
        pass

    def get_node_parent(self,node):
        pass
    
    def print(self):
        for n in self.nodes:
            self.print_node(n,"  ")

    def print_node(self,n,odsazeni):
        print(odsazeni + " - " + str(n))
        for ch in n.children:
            self.print_node(ch,odsazeni + "  ")

def create_node(id,label,done=False):
    node = Node(id,label)
    node.done = done
    return node

if __name__ == "__main__":
    tree = Tree()
    tree.add_node(create_node(1,"A1",True))
    tree.add_node(create_node(2,"B1",False))
    tree.add_node(create_node(3,"A11",True),1)
    tree.add_node(create_node(4,"A12",True),1)
    tree.add_node(create_node(5,"A111",True),3)
    tree.add_node(create_node(6,"A112",False),3)
    tree.add_node(create_node(7,"A121",True),4)
    tree.add_node(create_node(8,"A122",False),4)
    tree.add_node(create_node(9,"A1211",True),7)
    n = tree.find_lowest_node_matching_filter("done=True")
    print(str(n))
    print("done")
