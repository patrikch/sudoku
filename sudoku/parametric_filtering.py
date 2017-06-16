
class Thing:
    def __init__(self, a=None, b=None):
        self.a = a
        self.b = b

    def __repr__(self):
        return "Thing(a={0},b={1})".format(self.a, self.b)

if __name__ == "__main__":
    ls = [Thing(1, 2), Thing(3, 4), Thing()]
    flt = [t for t in ls if getattr(t, "a") == 1]
    print(str(len(flt)))
    flt2 = [t for t in ls if getattr(t, "b") == 2]
    print(str(len(flt2)))
    print("done")
