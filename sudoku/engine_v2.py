from sudoku.status_tree import Tree, Node
from sudoku.structures import Game, Cell


class NumberSearchEngine:

    def __init__(self, game):
        self.game_archive = []
        self.game = game
        self.tree = Tree()

    def find_numbers(self, if_fail_create_new_plan=True):
        self.tree = Tree()
        while self.game.empty_count > 0:
            ok = self.make_step(if_fail_create_new_plan)
            if not ok and not if_fail_create_new_plan:
                return False

        return True

    def save_game_current_status(self):
        current = self.tree.get_current()
        if current:
            if not current.data:
                current.data = self.game.get_formatted_solution_cells()

    def find_next_number(self):
        try:
            #print(self.game.get_formatted_solution_cells() + '\n')
            found_cells = self._find_empty_cells_with_smallest_choice()
        except EmptyCellsWithNoChoicesException:
            return False

        if len(found_cells) > 0:
            c = found_cells[0]
            c.cell.num = c.choices[0]
            current_node = self.tree.get_current()
            new_current_node_id = c.cell.id + "=" + str(c.cell.num)
            self.add_to_tree(found_cells, new_current_node_id, current_node.id if current_node else None)
            self.tree.set_current(new_current_node_id)
            print('new current node:{}'.format(self.tree.get_current()))
            return True
        else:
            return False

    def make_step(self, if_fail_create_new_plan=True):
        self.save_game_current_status()
        ok = self.find_next_number()
        if ok:
            current_node = self.tree.get_current()
            self.game.add_cell(Cell(current_node.id[:2], int(current_node.id[3])))
        else:
            print('chybi:' + str(self.game.empty_count) + '\n')
            print('game:' + self.game.get_formatted_solution_cells())
            self.game_archive.append(self.game)
            if if_fail_create_new_plan:
                self.create_new_game_plan_to_continue()
        return ok

    def create_new_game_plan_to_continue(self):
        current_node = self.tree.get_current()
        current_node.done = True
        print('find nearest for:{}'.format(current_node) + ',done=' + str(current_node.done) + '\n')
        node_to_continue = self.tree.find_nearest_not_done_node(current_node, current_node.id)
        self.print_tree()
        new_game = Game(self.game.get_input_cells())
        new_game.reconstruct_saved_game(node_to_continue.parent.data)
        new_game.add_cell(Cell(node_to_continue.id[:2], int(node_to_continue.id[3])))
        self.tree.set_current(node_to_continue.id)
        node_to_continue = self.tree.get_current()
        print('new current node:{}'.format(node_to_continue) + ',done=' + str(node_to_continue.done) + '\n')
        #current_node = self.tree.get_current()
        #print('new current node:{}'.format(current_node))
        self.game = new_game

    def add_to_tree(self, found_cells, selected, parent_id=None):
        for found_cell in found_cells:
            for choice in found_cell.choices:
                id = found_cell.cell.id + '=' + str(choice)
                node = Node(id)
                if id == selected:
                    node.done = True
                if not self.tree.exists_node(node, parent_id):
                    self.tree.add_node(node, parent_id)

    def print_progress(self, found_cells):
        print("pocet=" + str(len(found_cells)))
        for cell in found_cells:
            print("bunka=" + str(cell))
            print("----------------------")

    def print_tree(self):
        all_nodes = list(self.tree.walk_through_nodes_breadth_first(add_separators=True))
        print(','.join(n.id for n in all_nodes) + '\n')

    def _find_empty_cells_with_smallest_choice(self):
        cell_choices = self._get_all_empty_cells_choices()
        unsolvable_cells = [choice.cell for choice in cell_choices if len(choice.choices) == 0]
        if len(unsolvable_cells) > 0:
            raise EmptyCellsWithNoChoicesException('Following cells are unsolvable {}'.format(
                ', '.join(str(cell.id) for cell in unsolvable_cells)))

        lst = [choice for choice in cell_choices if len(choice.choices) > 0]
        if len(lst) == 0:
            return []
        min_value = min(len(choice.choices) for choice in lst)
        min_cells = [choice for choice in cell_choices if len(choice.choices) == min_value]
        return min_cells

    def _get_all_empty_cells_choices(self):
        empty_cells = [c for c in self.game.empty()]
        cell_choices = []
        for c in empty_cells:
            choices = self._find_possible_value_for_cell(c)
            cell_choices.append(SearchResult(c, choices))
        return cell_choices


    def _find_possible_value_for_cell(self, cell):
        all_nums = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        missing_vals_4_row = all_nums.difference(c.num for c in self.game.filled() if c.row == cell.row and
                                                 c.id != cell.id)
        missing_vals_4_col = all_nums.difference(c.num for c in self.game.filled() if c.col == cell.col and
                                                 c.id != cell.id)
        missing_vals_4_square = all_nums.difference(c.num for c in self.game.filled() if c.square == cell.square
                                                    and c.id != cell.id)
        #return prunik
        tmp = missing_vals_4_row.intersection(missing_vals_4_col)
        result = tmp.intersection(missing_vals_4_square)
        return list(result)


class SearchResult:
    def __init__(self, cell, choices):
        self.cell = cell
        choices.sort()
        self.choices = choices

    def __repr__(self):
        return "SearchResult(cell={0} ,choices={1}".format(self.cell, ",".join(str(i) for i in self.choices))


class EmptyCellsWithNoChoicesException(Exception):
    pass
