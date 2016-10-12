import random
from status_tree import Tree,Node

class Cell:
    def __init__(self,ident,num=None):
        self.id = ident
        self.num = num

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
        elif self.row >= 4 and self.row < 7:
            return 1
        else:
            return 2

    def _get_col_index(self):
        if self.col.lower() in ("a","b","c"):
            return 0
        elif self.col.lower() in ("d","e","f"):
            return 1
        else:
            return 2
        

    def __repr__(self):
        return "Cell(row={0},col={1},square={2},value={3})".format(self.row,self.col,self.square,self.num)

    def __eq__(self,other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

class GameStatus:
    
    def __init__(self,cells):
        self.input_cells = cells
        self.cells = []
        self._generate_empty_cells()
        #assign defined values
        for def_cell in self.input_cells:
            if def_cell in self.cells:
                self.cells[self.cells.index(def_cell)].num = def_cell.num

    def _generate_empty_cells(self):
        cols = ["a","b","c","d","e","f","g","h","i"]  #a-i
        rows = [n for n in range(1,10)]               #1-9
        self.cells = [Cell(str(c) + str(r)) for r in rows for c in cols]

    def print(self):
        cols = ["a","b","c","d","e","f","g","h","i"]  #a-i
        rows = [n for n in range(1,10)]               #1-9
        for r in rows:
            print("\n")
            if r in (4,7):
                print("--------------------------------\n")
            for c in cols:
                tmp_cell = Cell(str(c) + str(r))
                index = self.cells.index(tmp_cell)
                cell = self.cells[index]
                print(" " + (str(cell.num) if cell.num else ".") + " ",end="")
                if c in ("c","f","i"):
                    print("| ",end="")
        print("\n--------------------------------\n")

    def _statistics(self):
        d = {}
        filled = len([c for c in self.cells if c.num])
        no_filled = len(self.cells) - filled
        d["vyplneno"] = self.filled_count
        d["nevyplneno"] = self.empty_count
        d["celkem"] = filled + no_filled
        for i in range(1,10):
            d["vyplneno#" + str(i)] = len([c for c in self.cells if c.num and c.square==i])

        return d

    def print_statistics(self):
        d = self._statistics()
        for k,v in d.items():
            print(k + " = " + str(v) + "\n",end="")

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
        for r in range(1,10):
            s = ""
            for c in ["a","b","c","d","e","f","g","h","i"]:
                tmp_cell = Cell(str(c) + str(r))
                index = self.cells.index(tmp_cell)
                cell = self.cells[index]
                s = s + (str(cell.num) if cell.num else ".")
            lst.append(s)
        return lst

    def validate(self):
        return "" + \
               ("r" if not self._validate_rows() else "") + \
               ("c" if not self._validate_cols() else "") + \
               ("s" if not self._validate_squares() else "")

    def _validate_rows(self):
        return self._validate_entity(list(range(1,10)),"row")

    def _validate_cols(self):
        return self._validate_entity(["a","b","c","d","e","f","g","h","i"],"col")

    def _validate_squares(self):
        return self._validate_entity(list(range(1,10)),"square")

    def _validate_entity(self,list,prop_name):
        for item in list:
            cells = [c for c in self.cells if getattr(c,prop_name) == item]
            ok = self._validate_group_cells(cells)
            if not ok:
                return False
        return True
        
    def _validate_group_cells(self,cells):
        d = {n:0 for n in range(1,10)}
        d[None]=0
        for k,v in d.items():
            count = len([c for c in cells if c.num == k])
            if count > 1 and k != None:
                return False
        return True
        

class NumberSearchEngine:
    def __init__(self,game_status):
        self.game_status = game_status
        self.tree = Tree()

    def find_numbers(self):
        counter = 0
        prev = None
        self.tree = Tree()
        while self.game_status.empty_count > 0:
            found_cells = self._find_empty_cells_with_smallest_choice()
            self.add_to_tree(found_cells,prev)
            if len(found_cells) > 0:
                c = found_cells[0]
                c.cell.num = c.choices[0]
                prev = c.cell.id + str(c.cell.num)
                self.print_progress(found_cells)
            else:
                print("found nothing")

            print("missing vals=" + str(self.game_status.empty_count))
            counter = counter + 1
            if counter > 100:
                break
    
            
    def add_to_tree(self,found_cells,parent_id=None):
        for fcell in found_cells:
            for choice in fcell.choices:
                node = Node(fcell.cell.id + str(choice),fcell.cell.id + "=" + str(choice))
                self.tree.add_node(node,parent_id)
        

    def print_progress(self,found_cells):
        print("pocet=" + str(len(found_cells)))
        for cell in found_cells:
            print("bunka=" + str(cell))
            print("----------------------")
        
                
    def _find_empty_cells_with_smallest_choice(self):
        empty_cells = [c for c in self.game_status.empty()]
        cell_choices = []
        for c in empty_cells:
            choices = self._find_possible_value_for_cell(c)
            cell_choices.append(SearchResult(c,choices))
        lst = [choice for choice in cell_choices if len(choice.choices)>0]
        if len(lst) == 0:
            return []
        min_value = min(len(choice.choices) for choice in lst)
        min_cells = [choice for choice in cell_choices if len(choice.choices) == min_value]
        return min_cells

    def _find_possible_value_for_cell(self,cell):
        all_nums = {1,2,3,4,5,6,7,8,9}
        missing_vals_4_row = all_nums.difference(c.num for c in self.game_status.filled() if c.row == cell.row and c.id != cell.id)
        missing_vals_4_col = all_nums.difference(c.num for c in self.game_status.filled() if c.col == cell.col and c.id != cell.id)
        missing_vals_4_square = all_nums.difference(c.num for c in self.game_status.filled() if c.square == cell.square and c.id != cell.id)
        #return prunik
        tmp = missing_vals_4_row.intersection(missing_vals_4_col)
        result = tmp.intersection(missing_vals_4_square)
        return list(result)
        
class SearchResult:
    def __init__(self,cell,choices):
        self.cell = cell
        choices.sort()
        self.choices = choices

    def __repr__(self):
        return "SearchResult(cell={0} ,choices={1}".format(self.cell,",".join(str(i) for i in self.choices))

def get_game_inp():
    game_inp = []
    game_inp.append(Cell("a1",8))
    game_inp.append(Cell("d1",9))
    game_inp.append(Cell("e1",4))
    game_inp.append(Cell("i1",5))
    game_inp.append(Cell("e2",5))
    game_inp.append(Cell("g2",2))
    game_inp.append(Cell("a3",1))
    game_inp.append(Cell("c3",9))
    game_inp.append(Cell("d3",6))
    game_inp.append(Cell("f3",2))
    game_inp.append(Cell("a4",5))
    game_inp.append(Cell("c4",1))
    game_inp.append(Cell("i4",4))
    game_inp.append(Cell("a5",4))
    game_inp.append(Cell("b5",6))
    game_inp.append(Cell("h5",5))
    game_inp.append(Cell("i5",3))
    game_inp.append(Cell("a6",2))
    game_inp.append(Cell("g6",8))
    game_inp.append(Cell("i6",1))
    game_inp.append(Cell("d7",4))
    game_inp.append(Cell("f7",9))
    game_inp.append(Cell("g7",1))
    game_inp.append(Cell("i7",7))
    game_inp.append(Cell("c8",4))
    game_inp.append(Cell("e8",6))
    game_inp.append(Cell("a9",9))
    game_inp.append(Cell("e9",1))
    game_inp.append(Cell("f9",7))
    game_inp.append(Cell("i9",6))
    return game_inp
    

if __name__ == "__main__":
    #c = Cell("a1")
    #print(str(c))
    game_inp = get_game_inp()
    gs = GameStatus(game_inp)
    gs.print()
    ok = gs.validate()
    print("ok?" + str(ok))
    #lst=gs.compressed()
    #for r in lst:
    #    print(r + "\n")
    
    #engine = NumberSearchEngine(gs)
    #engine.find_numbers()
    #engine.tree.print()
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
