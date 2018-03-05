import re


class GameFileReader:

    def __init__(self, filename):
        self.filename = filename
        self.games = {}

    def _read_file(self):
        self.games = {}
        index = 0
        with open(self.filename, encoding='utf-8') as file:
            for line in file:
                if line.startswith('----'):
                    index += 1
                    self.games[index] = []
                    continue
                if re.match(r'^[.1-9]{3}|[.1-9]{3}|[.1-9]{3}$', line.strip()):
                    self.games[index].append(line.strip())

    def get_game(self, index=1):
        if len(self.games) == 0:
            self._read_file()
        game_list = self.games[index]
        return TextBlockReader('\n'.join(game_list)).get_game()


class TextBlockReader:

    def __init__(self, text_block):
        self.text_block = text_block

    def get_game(self):
        from sudoku.structures import Cell

        tmp = self.text_block.split('\n')
        lines = [line.strip() for line in tmp if len(line.strip()) > 0]
        cells = []
        columns = ["a", "b", "c", "", "d", "e", "f", "", "g", "h", "i"]
        for index, item in enumerate(lines):
            for col_index, cell_value in enumerate(item):
                if cell_value != '|' and cell_value != '.':
                    cells.append(Cell(columns[col_index] + str(index + 1), int(cell_value)))
        return cells


