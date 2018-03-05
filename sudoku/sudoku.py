from sudoku.utils import GameFormatter
from sudoku.structures import Cell


class GameStatus:

    #TODO: neukladat prazdne bunky, zachovavat poradi pridavani hodnot (bunek)

    def __init__(self, input_cells):
        self.cells = []
        self._generate_empty_cells()
        for cell in self.cells:
            if cell in input_cells:
                self.cells[self.cells.index(cell)].num = input_cells[input_cells.index(cell)].num

    def _generate_empty_cells(self):
        cols = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]  #a-i
        rows = [n for n in range(1, 10)]               #1-9
        self.cells = [Cell(str(c) + str(r)) for r in rows for c in cols]

    @property
    def empty_count(self):
        return len([c for c in self.cells if not c.num])

    @property
    def filled_count(self):
        return len([c for c in self.cells if c.num])

    def empty(self):
        for c in self.cells:
            if not c.num:
                yield c

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
        return self.cells[self.cells.index(Cell(ident))].num


def get_game_inp():
    game_inp = []
    game_inp.append(Cell("a1", 8))
    game_inp.append(Cell("d1", 9))
    game_inp.append(Cell("e1", 4))
    game_inp.append(Cell("i1", 5))
    game_inp.append(Cell("e2", 5))
    game_inp.append(Cell("g2", 2))
    game_inp.append(Cell("a3", 1))
    game_inp.append(Cell("c3", 9))
    game_inp.append(Cell("d3", 6))
    game_inp.append(Cell("f3", 2))
    game_inp.append(Cell("a4", 5))
    game_inp.append(Cell("c4", 1))
    game_inp.append(Cell("i4", 4))
    game_inp.append(Cell("a5", 4))
    game_inp.append(Cell("b5", 6))
    game_inp.append(Cell("h5", 5))
    game_inp.append(Cell("i5", 3))
    game_inp.append(Cell("a6", 2))
    game_inp.append(Cell("g6", 8))
    game_inp.append(Cell("i6", 1))
    game_inp.append(Cell("d7", 4))
    game_inp.append(Cell("f7", 9))
    game_inp.append(Cell("g7", 1))
    game_inp.append(Cell("i7", 7))
    game_inp.append(Cell("c8", 4))
    game_inp.append(Cell("e8", 6))
    game_inp.append(Cell("a9", 9))
    game_inp.append(Cell("e9", 1))
    game_inp.append(Cell("f9", 7))
    game_inp.append(Cell("i9", 6))
    return game_inp
    

if __name__ == "__main__":
    #c = Cell("a1")
    #print(str(c))
    game_inp = get_game_inp()
    gs = GameStatus(game_inp)
    GameFormatter(gs).print()
    #ok = gs.validate()
    #print("ok?" + str(ok))
    #lst=gs.compressed()
    #for r in lst:
    #    print(r + "\n")
    
    # .engine = NumberSearchEngine(gs)
    # .engine.find_numbers()
    # .engine.tree.print()
    #------------------------------
    
    #gs.print_statistics()
    #gs.print()
    #tmp = engine._find_empty_cells_with_smallest_choice()
    #print("pocet=" + str(len(tmp)))
    #print("bunka=" + str(tmp[0].cell))
    #print("choices=" + str(tmp[0].choices))
    #p = Playground(game_inp)
    #p.print()
    #result = p.find_numbers()
    #print("result=" + str(result))
    #p.print()
    #---------------------------
    #tmp = p._find_empty_cells_with_smallest_choice()
    #print("bunek:" + str(len(tmp[0])))
    #print("min_choice:" + str(tmp[1]))
