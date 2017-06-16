from status_tree_v2 import Tree, Node
from structures import Game, Cell


class NumberSearchEngine:

    def __init__(self, game):
        self.game_archive = []
        self.game = game
        self.tree = Tree()
        self.prev_node_name = None

    def find_numbers(self, if_fail_create_new_plan=True):
        self.prev_node_name = None
        self.tree = Tree()
        while self.game.empty_count > 0:
            ok = self.make_step(if_fail_create_new_plan)
            if not ok and not if_fail_create_new_plan:
                return False

        return True

    def save_game_current_status(self):
        if self.prev_node_name:
            prev_node = self.tree.find_in_nodes(self.tree.nodes, self.prev_node_name)
            if not prev_node.data:
                prev_node.data = self.game.get_formatted_solution_cells()

    def find_next_number(self):
        try:
            found_cells = self._find_empty_cells_with_smallest_choice()
        except EmptyCellsWithNoChoicesException:
            return False

        if len(found_cells) > 0:
            c = found_cells[0]
            c.cell.num = c.choices[0]
            self.add_to_tree(found_cells, c.cell.id + "=" + str(c.cell.num), self.prev_node_name)
            self.prev_node_name = c.cell.id + '=' + str(c.cell.num)
            # self.print_progress(found_cells)
            return True
        else:
            return False

    def make_step(self, if_fail_create_new_plan=True):
        self.save_game_current_status()
        ok = self.find_next_number()
        if ok:
            try:
                print('new cell:' + self.prev_node_name)
                self.game.add_cell(Cell(self.prev_node_name[:2], int(self.prev_node_name[3])))
            except IndexError:
                print('[' + self.prev_node_name + ']')
        else:
            print('chybi:' + str(self.game.empty_count))
            self.game_archive.append(self.game)
            if if_fail_create_new_plan:
                self.create_new_game_plan_to_continue()
        return ok

    def create_new_game_plan_to_continue(self):
        prev_node = self.tree.find_in_nodes(self.tree.nodes, self.prev_node_name)
        node_to_continue = self.tree.find_nearest_not_done_node(prev_node, self.prev_node_name)
        new_game = Game(self.game.get_input_cells())
        print('new data:' + node_to_continue.parent.data)
        new_game.reconstruct_saved_game(node_to_continue.parent.data)
        new_game.add_cell(Cell(node_to_continue.ident[:2], int(node_to_continue.ident[3])))
        self.game = new_game

        self.prev_node_name = node_to_continue.parent.ident

    def add_to_tree(self, found_cells, selected, parent_id=None):
        for found_cell in found_cells:
            for choice in found_cell.choices:
                ident = found_cell.cell.id + '=' + str(choice)
                node = Node(ident)
                if ident == selected:
                    node.done = True
                if not self.tree.exists_node(node, parent_id):
                    self.tree.add_node(node, parent_id)

    def print_progress(self, found_cells):
        print("pocet=" + str(len(found_cells)))
        for cell in found_cells:
            print("bunka=" + str(cell))
            print("----------------------")

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
