

class GameFormatter:

    def __init__(self, game):
        self.game = game

    def print(self):
        from structures import Cell
        cols = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]  #a-i
        rows = [n for n in range(1, 10)]                      #1-9
        for r in rows:
            print("\n")
            if r in (4, 7):
                print("--------------------------------\n")
            for c in cols:
                tmp_cell = Cell(str(c) + str(r))
                index = self.game.cells.index(tmp_cell)
                cell = self.game.cells[index]
                print(" " + (str(cell.num) if cell.num else ".") + " ", end="")
                if c in ("c", "f", "i"):
                    print("| ", end="")
        print("\n--------------------------------\n")

    def _statistics(self):
        d = {}
        filled = len([c for c in self.game.cells if c.num])
        no_filled = len(self.game.cells) - filled
        d["vyplneno"] = self.game.filled_count
        d["nevyplneno"] = self.game.empty_count
        d["celkem"] = filled + no_filled
        for i in range(1, 10):
            d["vyplneno#" + str(i)] = len([c for c in self.game.cells if c.num and c.square == i])

        return d

    def print_statistics(self):
        d = self._statistics()
        for k, v in d.items():
            print(k + " = " + str(v) + "\n", end="")