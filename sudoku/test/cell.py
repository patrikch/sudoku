import unittest
from sudoku.structures import Cell

__all__ = (
    'CellTestCase',
)


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
