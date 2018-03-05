import unittest

from sudoku.structures import Game, Cell
from sudoku.engine_v2 import NumberSearchEngine, EmptyCellsWithNoChoicesException
from sudoku.task_readers import TextBlockReader


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
        node = engine.tree.find_deepest_node()
        self.assertEqual(node.id[:2], game.cells[len(game.cells)-1].id)
        with self.assertRaises(EmptyCellsWithNoChoicesException):
            engine._find_empty_cells_with_smallest_choice()

    def test_engine_check_create_new_plan_after_one_unsuccessivelly_finished_plan(self):
        game = Game(TextBlockReader(GAME_1).get_game())
        engine = NumberSearchEngine(game)
        self.assertEqual(0, len(engine.game_archive))
        engine.find_numbers(False)
        self._print_tree(engine)
        old_game = engine.game
        old_current = engine.tree.get_current()
        engine.create_new_game_plan_to_continue()
        new_game = engine.game
        new_current = engine.tree.get_current()
        self._print_tree(engine)
        self.assertNotEqual(old_game.cells[len(old_game.cells)-1], new_game.cells[len(new_game.cells)-1])
        self.assertNotEqual(old_current, new_current)

    def _print_tree(self, engine):
        all_nodes = list(engine.tree.walk_through_nodes_breadth_first(add_separators=True))
        print(','.join(n.id for n in all_nodes) + '\n')

    @unittest.skip('not done')
    def test_engine_try_to_solve_whole_game(self):
        game = Game(TextBlockReader(GAME_1).get_game())
        engine = NumberSearchEngine(game)
        self.assertTrue(engine.find_numbers())
        self.assertEqual(engine.game.empty_count, 0)
        self.assertEqual(engine.game.filled_count, 81)
        self.assertEqual(engine.game.validate(), '')