from sudoku.task_readers import GameFileReader


class Cell:
    def __init__(self, id, num=None):
        self.id = id
        self.num = num
        self.solution_cell = False

    @property
    def row(self):
        return int(self.id[1])

    @property
    def col(self):
        return self.id[0]

    @property
    def square(self):
        return 3 * self._get_row_index() + self._get_col_index() + 1

    def _get_row_index(self):
        if self.row < 4:
            return 0
        elif 4 <= self.row < 7:
            return 1
        else:
            return 2

    def _get_col_index(self):
        if self.col.lower() in ("a", "b", "c"):
            return 0
        elif self.col.lower() in ("d", "e", "f"):
            return 1
        else:
            return 2

    def __str__(self):
        return 'Cell(id={},value={})'.format(self.id, self.num)

    def __repr__(self):
        return "Cell(row={0},col={1},square={2},value={3})".format(self.row, self.col, self.square, self.num)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


class DuplicateCellException(Exception):
    pass


class Game:

    def __init__(self, input_cells):
        self.cells = input_cells

    def reconstruct_saved_game(self, formatted_solution_cells):
        cells = formatted_solution_cells.split(',')
        for cell in cells:
            self.add_cell(Cell(cell[:2], int(cell[3])))

    @classmethod
    def create_from_file(cls, filename, game_index):
        input_cells = GameFileReader(filename).get_game(game_index)
        return cls(input_cells)

    def add_cell(self, cell):
        if cell in self.cells:
            raise DuplicateCellException('Cell {} already is in game.'.format(cell))

        cell.solution_cell = True
        self.cells.append(cell)

    def get_solution_cells(self):
        return [cell for cell in self.cells if cell.solution_cell]

    def get_last_cell(self):
        return self.cells[len(self.cells)-1]

    def get_formatted_solution_cells(self):
        cells = [cell.id + '=' + str(cell.num) for cell in self.cells if cell.solution_cell]
        return ','.join(cells)

    def get_input_cells(self):
        return [cell for cell in self.cells if not cell.solution_cell]

    @property
    def empty_count(self):
        return 81 - self.filled_count

    @property
    def filled_count(self):
        return len([c for c in self.cells if c.num])

    def empty(self):
        for row in range(1, 10):
            for col in ["a", "b", "c", "d", "e", "f", "g", "h", "i"]:
                if Cell(col + str(row)) not in self.cells:
                    yield Cell(col + str(row))

    def filled(self):
        for c in self.cells:
            if c.num:
                yield c

    def compressed(self):
        lst = []
        for r in range(1, 10):
            s = ""
            for c in ["a", "b", "c", "d", "e", "f", "g", "h", "i"]:
                tmp_cell = Cell(str(c) + str(r))
                index = self.cells.index(tmp_cell)
                cell = self.cells[index]
                s += (str(cell.num) if cell.num else ".")
            lst.append(s)
        return lst

    def validate(self):
        return ("" +
                ("r" if not self._validate_rows() else "") +
                ("c" if not self._validate_cols() else "") +
                ("s" if not self._validate_squares() else ""))

    def _validate_rows(self):
        return self._validate_entity(list(range(1, 10)), "row")

    def _validate_cols(self):
        return self._validate_entity(["a", "b", "c", "d", "e", "f", "g", "h", "i"], "col")

    def _validate_squares(self):
        return self._validate_entity(list(range(1, 10)), "square")

    def _validate_entity(self, list, prop_name):
        for item in list:
            cells = [c for c in self.cells if getattr(c, prop_name) == item]
            ok = self._validate_group_cells(cells)
            if not ok:
                return False
        return True

    def _validate_group_cells(self, cells):
        d = {n: 0 for n in range(1, 10)}
        d[None] = 0
        for k, v in d.items():
            count = len([c for c in cells if c.num == k])
            if count > 1 and k:
                return False
        return True

    def get_cell_value(self, ident):
        cell = Cell(ident)
        if cell in self.cells:
            return self.cells[self.cells.index(cell)].num
        return None
