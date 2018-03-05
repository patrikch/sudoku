import unittest

from sudoku.structures import Cell, Game
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