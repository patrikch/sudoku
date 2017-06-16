import unittest

from structures import Cell, Game
from task_readers import TextBlockReader
from engine import NumberSearchEngine, EmptyCellsWithNoChoicesException
from status_tree_v2 import Node, Tree


GAME_1 = """
    8..|94.|..5|
    ...|.5.|2..|
    1.9|6.2|...|
    5.1|...|..4|
    46.|...|.53|
    2..|...|8.1|
    ...|4.9|1.7|
    ..4|.6.|...|
    9..|.17|..6|
    """


class CellTestCase(unittest.TestCase):

    def test_cell_has_correct_column_row_square(self):
        cell = Cell('a1')
        self.assertEqual('a', cell.col)
        self.assertEqual(1, cell.row)
        self.assertEqual(1, cell.square)
        cell2 = Cell('i9')
        self.assertEqual('i', cell2.col)
        self.assertEqual(9, cell2.row)
        self.assertEqual(9, cell2.square)

    def test_cell_are_equal(self):
        cell = Cell('a1')
        cell2 = Cell('a1')
        cell3 = Cell('i9')
        self.assertEqual(cell, cell2)
        self.assertNotEqual(cell, cell3)


class GameStatusTestCase(unittest.TestCase):

    cells_with_numbers = []

    def setUp(self):
        self.cells_with_numbers = TextBlockReader(GAME_1).get_game()

    def test_game_is_correctly_prepared(self):
        game = Game(self.cells_with_numbers)
        self.assertEqual(len(self.cells_with_numbers), len(game.cells))
        self.assertEqual(81, game.empty_count + game.filled_count)
        for cell in self.cells_with_numbers:
            self.assertEqual(cell.num, game.get_cell_value(cell.id))
        self.assertEqual(len(self.cells_with_numbers), game.filled_count)
        self.assertEqual(81-len(self.cells_with_numbers), game.empty_count)

    def test_load_game_from_block_text(self):
        game_block = """
        ..1|..2|..3
        ..4|..5|..6
        ..7|..8|..9
        .1.|.2.|.3.
        .4.|.5.|.6.
        .7.|.8.|.9.
        1..|2..|3..
        4..|5..|6..
        7..|8..|9..
        """
        game = Game(TextBlockReader(game_block).get_game())
        self.assertEqual(27, game.filled_count)

    def test_validate_game_ok(self):
        game_block = """
                ..1|..2|..3
                ..4|..5|..6
                ..7|..8|..9
                .1.|.2.|.3.
                .4.|.5.|.6.
                .7.|.8.|.9.
                1..|2..|3..
                4..|5..|6..
                7..|8..|9..
                """
        game = Game(TextBlockReader(game_block).get_game())
        self.assertEqual('', game.validate())

    def test_validate_game_duplication_in_row(self):
        game_block = """
                ..1|1.2|..3
                ..4|..5|..6
                ..7|..8|..9
                .1.|.2.|.3.
                .4.|.5.|.6.
                .7.|.8.|.9.
                1..|2..|3..
                4..|5..|6..
                7..|8..|9..
                """
        game = Game(TextBlockReader(game_block).get_game())
        self.assertEqual('r', game.validate())

    def test_validate_game_duplication_in_column_and_square(self):
        game_block = """
                ..1|..2|..3
                ..4|..5|..6
                .17|..8|..9
                .1.|.2.|.3.
                .4.|.5.|.6.
                .7.|.8.|.9.
                1..|2..|3..
                4..|5..|6..
                7..|8..|9..
                """
        game = Game(TextBlockReader(game_block).get_game())
        self.assertEqual('cs', game.validate())

    def test_validate_game_duplication_in_all(self):
        game_block = """
                3.1|..2|..3
                ..4|..5|..6
                .17|..8|..9
                .1.|.2.|.3.
                .4.|.5.|.6.
                .7.|.8.|.9.
                1..|2..|3..
                4..|5..|6..
                7..|8..|9..
                """
        game = Game(TextBlockReader(game_block).get_game())
        self.assertEqual('rcs', game.validate())

    def test_get_formatted_solution_cells(self):
        game = Game(TextBlockReader(GAME_1).get_game())
        game.add_cell(Cell('b1', 5))
        game.add_cell(Cell('d2', 4))
        game.add_cell(Cell('e3', 3))
        self.assertEqual('b1=5,d2=4,e3=3', game.get_formatted_solution_cells())

    def test_reconstruct_saved_game(self):
        orig_game = Game(TextBlockReader(GAME_1).get_game())
        orig_game.add_cell(Cell('b1', 5))
        orig_game.add_cell(Cell('d2', 4))
        orig_game.add_cell(Cell('e3', 3))
        string_for_save = orig_game.get_formatted_solution_cells()
        new_game = Game(TextBlockReader(GAME_1).get_game())
        new_game.reconstruct_saved_game(string_for_save)
        self.assertEqual(len(orig_game.cells), len(new_game.cells))
        for index, cell in enumerate(orig_game.cells):
            self.assertEqual(cell, new_game.cells[index])
            self.assertEqual(cell.num, new_game.cells[index].num)


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
        nearest = self.tree.find_nearest_not_done_node(from_node, from_node.ident)
        self.assertIsNotNone(nearest)
        self.assertEqual('A112', nearest.ident)

    def test_find_nearest_not_done_node_another_brother(self):
        from_node = self.tree.find_in_nodes(self.tree.nodes, 'A111')
        self.tree.find_in_nodes(self.tree.nodes, 'A112').done = True
        nearest = self.tree.find_nearest_not_done_node(from_node, from_node.ident)
        self.assertIsNotNone(nearest)
        self.assertEqual('A113', nearest.ident)

    def test_find_nearest_not_done_node_parent_brother(self):
        from_node = self.tree.find_in_nodes(self.tree.nodes, 'A111')
        self.tree.find_in_nodes(self.tree.nodes, 'A112').done = True
        self.tree.find_in_nodes(self.tree.nodes, 'A113').done = True
        nearest = self.tree.find_nearest_not_done_node(from_node, from_node.ident)
        self.assertIsNotNone(nearest)
        self.assertEqual('A12', nearest.ident)

    def test_find_nearest_not_done_node_grandparent_brother(self):
        from_node = self.tree.find_in_nodes(self.tree.nodes, 'A111')
        self.tree.find_in_nodes(self.tree.nodes, 'A112').done = True
        self.tree.find_in_nodes(self.tree.nodes, 'A113').done = True
        self.tree.find_in_nodes(self.tree.nodes, 'A12').done = True
        nearest = self.tree.find_nearest_not_done_node(from_node, from_node.ident)
        self.assertIsNotNone(nearest)
        self.assertEqual('A2', nearest.ident)

    def test_find_nearest_not_done_node_grand_grandparent_brother(self):
        from_node = self.tree.find_in_nodes(self.tree.nodes, 'A111')
        self.tree.find_in_nodes(self.tree.nodes, 'A112').done = True
        self.tree.find_in_nodes(self.tree.nodes, 'A113').done = True
        self.tree.find_in_nodes(self.tree.nodes, 'A12').done = True
        self.tree.find_in_nodes(self.tree.nodes, 'A2').done = True
        nearest = self.tree.find_nearest_not_done_node(from_node, from_node.ident)
        self.assertIsNotNone(nearest)
        self.assertEqual('B', nearest.ident)

    def test_find_nearest_not_done_node_grand_grandparent_other_brother(self):
        from_node = self.tree.find_in_nodes(self.tree.nodes, 'A111')
        self.tree.find_in_nodes(self.tree.nodes, 'A112').done = True
        self.tree.find_in_nodes(self.tree.nodes, 'A113').done = True
        self.tree.find_in_nodes(self.tree.nodes, 'A12').done = True
        self.tree.find_in_nodes(self.tree.nodes, 'A2').done = True
        self.tree.find_in_nodes(self.tree.nodes, 'B').done = True
        nearest = self.tree.find_nearest_not_done_node(from_node, from_node.ident)
        self.assertIsNotNone(nearest)
        self.assertEqual('C', nearest.ident)

    def test_find_nearest_not_done_node_all_nodes_are_done(self):
        from_node = self.tree.find_in_nodes(self.tree.nodes, 'A111')
        self.tree.find_in_nodes(self.tree.nodes, 'A112').done = True
        self.tree.find_in_nodes(self.tree.nodes, 'A113').done = True
        self.tree.find_in_nodes(self.tree.nodes, 'A12').done = True
        self.tree.find_in_nodes(self.tree.nodes, 'A2').done = True
        self.tree.find_in_nodes(self.tree.nodes, 'B').done = True
        self.tree.find_in_nodes(self.tree.nodes, 'C').done = True
        nearest = self.tree.find_nearest_not_done_node(from_node, from_node.ident)
        self.assertIsNone(nearest)

    def create_tree(self, nodes):
        nodes.split(',')
        self.tree = Tree()


class NumberSearchEngineTestCase(unittest.TestCase):

    GAME_2 = """
        8..|94.|3.5|
        3.6|.5.|2.9|
        1.9|6.2|48.|

        5.1|7.3|9.4|
        46.|2.8|.53|
        2.3|59.|8.1|

        6..|4.9|1.7|
        7.4|.6.|5.2|
        9..|.17|..6|
        """

    def test_engine_after_make_step_new_node_in_tree(self):
        game = Game(TextBlockReader(GAME_1).get_game())
        engine = NumberSearchEngine(game)
        self.assertEqual(0, len(engine.tree))
        engine.make_step()
        self.assertNotEqual(0, len(engine.tree))

    def test_engine_find_possible_value_for_cell(self):
        game = Game(TextBlockReader(GAME_1).get_game())
        engine = NumberSearchEngine(game)
        # B1
        choices = engine._find_possible_value_for_cell(Cell('b1'))
        self.assertEqual([2, 3, 7], choices)
        # C1
        choices = engine._find_possible_value_for_cell(Cell('c1'))
        self.assertEqual([2, 3, 6, 7], choices)
        # F1
        choices = engine._find_possible_value_for_cell(Cell('f1'))
        self.assertEqual([1, 3], choices)
        # G1
        choices = engine._find_possible_value_for_cell(Cell('g1'))
        self.assertEqual([3, 6, 7], choices)
        # H1
        choices = engine._find_possible_value_for_cell(Cell('h1'))
        self.assertEqual([1, 3, 6, 7], choices)

    def test_engine_get_all_empty_cells_choices(self):
        game = Game(TextBlockReader(self.GAME_2).get_game())
        self.assertEqual('', game.validate())
        engine = NumberSearchEngine(game)
        result = engine._get_all_empty_cells_choices()
        self.assertEqual(game.empty_count, len(result))
        empty_cells = [cell for cell in game.empty()]
        for item in result:
            self.assertIn(item.cell, empty_cells)

    def test_engine_find_empty_cells_with_smallest_choice_unsolvable_cells_exception(self):
        game = Game(TextBlockReader(self.GAME_2).get_game())
        self.assertEqual('', game.validate())
        engine = NumberSearchEngine(game)
        with self.assertRaises(EmptyCellsWithNoChoicesException):
            engine._find_empty_cells_with_smallest_choice()

    def test_engine_check_after_one_step(self):
        game = Game(TextBlockReader(GAME_1).get_game())
        engine = NumberSearchEngine(game)
        self.assertEqual(0, len(engine.game_archive))
        original_cells = len(engine.game.cells)
        self.assertTrue(engine.make_step())
        self.assertEqual(len(engine.game.cells), original_cells+1)

    def test_engine_check_after_one_unsuccessivelly_finished_plan(self):
        game = Game(TextBlockReader(GAME_1).get_game())
        engine = NumberSearchEngine(game)
        self.assertEqual(0, len(engine.game_archive))
        engine.find_numbers(False)
        self.assertEqual(len(engine.game_archive), 1)
        game = engine.game_archive[0]
        self.assertEqual('', game.validate())
        with self.assertRaises(EmptyCellsWithNoChoicesException):
            engine._find_empty_cells_with_smallest_choice()

    def test_engine_try_to_solve_whole_game(self):
        game = Game(TextBlockReader(GAME_1).get_game())
        engine = NumberSearchEngine(game)
        self.assertTrue(engine.find_numbers())
        self.assertEqual(engine.game.empty_count, 0)
        self.assertEqual(engine.game.filled_count, 81)
        self.assertEqual(engine.game.validate(), '')


