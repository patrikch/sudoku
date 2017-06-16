"""Module for work with tree and his nodes"""


class Node:
    """ Represent one node in tree """

    def __init__(self, ident, label='', done=False):
        """initialization with ident and label fields"""
        self.ident = ident
        self.label = label
        self.done = done
        self.children = []
        self.data = ''
        self.parent = None

    def __repr__(self):
        """object representation"""
        return 'Node(label={0},done={1},id={2})'.format(self.label, str(self.done), str(self.ident))

    def __eq__(self, other):
        return self.ident == other.ident

    def __hash__(self):
        return hash(self.ident)


class Tree:
    """ Represent tree containing nodes """

    def __init__(self):
        """initialization - create empty list of nodes"""
        self.nodes = []

    def __len__(self):
        return len(self.nodes)

    def add_node(self, node, parent_id=None):
        """ find parent node and add new child to this parent node """
        if not parent_id:
            self.nodes.append(node)
        else:
            parent = self.find_in_nodes(self.nodes, parent_id)
            if parent:
                node.parent = parent
                parent.children.append(node)
            else:
                raise ValueError('Node not found ({})'.format(str(parent_id)))

    def exists_node(self, node, parent_id):
        parent = self.find_in_nodes(self.nodes, parent_id)
        if not parent:
            return False
        found_node = self.find_in_nodes(parent.children, node.ident)
        return found_node

    def find_in_nodes(self, nodes, wanted_id):
        """
        searching node by id in nodes given in parameter.
        method works recursively
        """
        if len(nodes) == 0:
            return None
        for node in nodes:
            if node.ident == wanted_id:
                return node
            found = self.find_in_nodes(node.children, wanted_id)
            if found:
                return found

        return None

    def find_nearest_not_done_node(self, node, start_node_id):
        """
        try to find nearest node which is done=False to node in parameter
        """
        nodes = node.parent.children if node.parent else self.nodes
        # print(str(nodes))
        brothers = [brother for brother in nodes
                    if brother.ident != start_node_id and not brother.done]
        found = brothers[0] if len(brothers) > 0 else None
        if not found and node.parent:
            return self.find_nearest_not_done_node(node.parent, start_node_id)
        return found
    
    def print(self):
        for node in self.nodes:
            self.print_node(node)

    def print_node(self, node, indent=1):
        s = '  '
        print(s * indent + str(node))
        for child in node.children:
            self.print_node(child, indent+1)


if __name__ == "__main__":
    tree = Tree()
    tree.add_node(Node(1, "A1", True))
    tree.add_node(Node(2, "B1", False))
    tree.add_node(Node(3, "A11", True), 1)
    tree.add_node(Node(4, "A12", True), 1)
    tree.add_node(Node(5, "A111", False), 3)
    tree.add_node(Node(6, "A112", False), 3)
    tree.add_node(Node(7, "A121", True), 4)
    tree.add_node(Node(8, "A122", True), 4)
    tree.add_node(Node(9, "A1211", True), 7)
    n = Node(10, "A1212", False)
    tree.add_node(n, 7)
    tree.print()
    #nearest = tree.find_nearest_free_node(n, n.ident)
    #print(str(nearest))
