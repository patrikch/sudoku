import unittest

from sudoku.status_tree import Node, Tree
from sudoku.tree_visualizer import Visualizer


class TreeTestCase(unittest.TestCase):

    tree = Tree()

    def setUp(self):
        self.tree = Tree()
        self.tree.add_node(Node('A', done=True), None)
        self.tree.add_node(Node('B', done=False), None)
        self.tree.add_node(Node('C', done=False), None)
        self.tree.add_node(Node('A1', done=True), 'A')
        self.tree.add_node(Node('A2', done=False), 'A')
        self.tree.add_node(Node('A11', done=True), 'A1')
        self.tree.add_node(Node('A12', done=False), 'A1')
        self.tree.add_node(Node('A111', done=False), 'A11')
        self.tree.add_node(Node('A112', done=False), 'A11')
        self.tree.add_node(Node('A113', done=False), 'A11')

    def test_exists_node_should_find_node(self):
        wanted_node = Node('A111', done=False)
        self.assertTrue(self.tree.exists_node(wanted_node, 'A11'))

    def test_exists_node_should_not_find_node_which_is_not_in_tree(self):
        wanted_node = Node('A114', done=False)
        self.assertFalse(self.tree.exists_node(wanted_node, 'A11'))

    def test_exists_node_should_not_find_node_parent_id_is_not_in_tree(self):
        wanted_node = Node('A111', done=False)
        self.assertFalse(self.tree.exists_node(wanted_node, 'A3'))

    def test_exists_node_should_not_find_node_parent_id_and_node_are_not_in_tree(self):
        wanted_node = Node('A115', done=False)
        self.assertFalse(self.tree.exists_node(wanted_node, 'A3'))

    def test_find_nearest_not_done_node_brother(self):
        from_node = self.tree.find_in_nodes(self.tree.nodes, 'A111')
        nearest = self.tree.find_nearest_not_done_node(from_node, from_node.id)
        self.assertIsNotNone(nearest)
        self.assertEqual('A112', nearest.id)

    def test_find_nearest_not_done_node_another_brother(self):
        from_node = self.tree.find_in_nodes(self.tree.nodes, 'A111')
        self.tree.find_in_nodes(self.tree.nodes, 'A112').done = True
        nearest = self.tree.find_nearest_not_done_node(from_node, from_node.id)
        self.assertIsNotNone(nearest)
        self.assertEqual('A113', nearest.id)

    def test_find_nearest_not_done_node_parent_brother(self):
        from_node = self.tree.find_in_nodes(self.tree.nodes, 'A111')
        self.tree.find_in_nodes(self.tree.nodes, 'A112').done = True
        self.tree.find_in_nodes(self.tree.nodes, 'A113').done = True
        nearest = self.tree.find_nearest_not_done_node(from_node, from_node.id)
        self.assertIsNotNone(nearest)
        self.assertEqual('A12', nearest.id)

    def test_find_nearest_not_done_node_grandparent_brother(self):
        from_node = self.tree.find_in_nodes(self.tree.nodes, 'A111')
        self.tree.find_in_nodes(self.tree.nodes, 'A112').done = True
        self.tree.find_in_nodes(self.tree.nodes, 'A113').done = True
        self.tree.find_in_nodes(self.tree.nodes, 'A12').done = True
        nearest = self.tree.find_nearest_not_done_node(from_node, from_node.id)
        self.assertIsNotNone(nearest)
        self.assertEqual('A2', nearest.id)

    def test_find_nearest_not_done_node_grand_grandparent_brother(self):
        from_node = self.tree.find_in_nodes(self.tree.nodes, 'A111')
        self.tree.find_in_nodes(self.tree.nodes, 'A112').done = True
        self.tree.find_in_nodes(self.tree.nodes, 'A113').done = True
        self.tree.find_in_nodes(self.tree.nodes, 'A12').done = True
        self.tree.find_in_nodes(self.tree.nodes, 'A2').done = True
        nearest = self.tree.find_nearest_not_done_node(from_node, from_node.id)
        self.assertIsNotNone(nearest)
        self.assertEqual('B', nearest.id)

    def test_find_nearest_not_done_node_grand_grandparent_other_brother(self):
        from_node = self.tree.find_in_nodes(self.tree.nodes, 'A111')
        self.tree.find_in_nodes(self.tree.nodes, 'A112').done = True
        self.tree.find_in_nodes(self.tree.nodes, 'A113').done = True
        self.tree.find_in_nodes(self.tree.nodes, 'A12').done = True
        self.tree.find_in_nodes(self.tree.nodes, 'A2').done = True
        self.tree.find_in_nodes(self.tree.nodes, 'B').done = True
        nearest = self.tree.find_nearest_not_done_node(from_node, from_node.id)
        self.assertIsNotNone(nearest)
        self.assertEqual('C', nearest.id)

    def test_find_nearest_not_done_node_all_nodes_are_done(self):
        from_node = self.tree.find_in_nodes(self.tree.nodes, 'A111')
        self.tree.find_in_nodes(self.tree.nodes, 'A112').done = True
        self.tree.find_in_nodes(self.tree.nodes, 'A113').done = True
        self.tree.find_in_nodes(self.tree.nodes, 'A12').done = True
        self.tree.find_in_nodes(self.tree.nodes, 'A2').done = True
        self.tree.find_in_nodes(self.tree.nodes, 'B').done = True
        self.tree.find_in_nodes(self.tree.nodes, 'C').done = True
        nearest = self.tree.find_nearest_not_done_node(from_node, from_node.id)
        self.assertIsNone(nearest)

    def test_walk_through_nodes_deep_first(self):
        all_nodes = list(self.tree.walk_through_nodes_deep_first())
        self.assertEqual(len(all_nodes), 10)
        self.assertEqual(','.join(n.id for n in all_nodes), 'A,A1,A11,A111,A112,A113,A12,A2,B,C')

    def test_set_current_node(self):
        self.assertEqual(self._get_current_nodes_count(), 0)
        self.tree.set_current('A113')
        self.assertEqual(self._get_current_nodes_count(), 1)
        self.assertEqual(self.tree.get_current().id, 'A113')
        self.tree.set_current('A1')
        self.assertEqual(self._get_current_nodes_count(), 1)
        self.assertEqual(self.tree.get_current().id, 'A1')

    @unittest.skip('not implemented yet')
    def test_format_tree_to_be_printable(self):
        all_nodes = list(self.tree.walk_through_nodes_deep_first_with_signs())
        self.assertEqual(len(all_nodes), 10)
        self.assertEqual(','.join(n.id for n in all_nodes), 'A,+A1,+A11,+A111,A112,A113,-A12,-A2,-B,C')

    @unittest.skip('not implemented yet')
    def test_visualizer(self):
        visualizer = Visualizer(self.tree)
        self.assertEqual(visualizer.draw(),
                         """
A B C
A1 A2 - -
A11 A12 -
A111 A112 A113 -
                         """
                         )

    def test_walk_through_nodes_breadth_first(self):
        all_nodes = list(self.tree.walk_through_nodes_breadth_first())
        self.assertEqual(len(all_nodes), 10)
        self.assertEqual(','.join(n.id for n in all_nodes), 'A,B,C,A1,A2,A11,A12,A111,A112,A113')

    def test_walk_through_nodes_breadth_first_with_separators(self):
        all_nodes = list(self.tree.walk_through_nodes_breadth_first(add_separators=True))
        self.assertEqual(len(all_nodes), 22)
        self.assertEqual(','.join(n.id for n in all_nodes),
                         'A,B,C,|,A1,A2,-,-,|,A11,A12,-,|,A111,A112,A113,-,|,-,-,-,|')

    def _get_current_nodes_count(self):
        return len(list(n for n in self.tree.walk_through_nodes_deep_first() if n.current))

    def create_tree(self, nodes):
        nodes.split(',')
        self.tree = Tree()
