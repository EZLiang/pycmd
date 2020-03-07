from typing import List, Callable

def digest(ln: str) -> List[str]:
    lst = []
    instr = False
    cstr = ""
    newvar = True
    for i in ln:
        if (not instr) and (i == " "):
            newvar = True
            lst += [cstr]
            cstr = ""
            continue
        if newvar and (i == "\""):
            instr = True
        elif instr and (i == "\""):
            instr = False
        else:
            cstr += i
        newvar = False
    lst += [cstr]
    return lst


class PyCmdInterface:
    def __init__(self, master: PyCmdLn) -> None:
        self.master = master
        self.PIPE = []

    def prompt(self, text: str = "") -> str:
        a = input(text)
        self.PIPE += [a]
        return a

    def display(self, text: str, end: str = "\n") -> None:
        print(text, end=end)

    def var(self, name: str, val: str) -> None:
        self.master.envars[name] = val

    def terminate(self):
        self.master.running = False

    def __getitem__(self, item: int) -> str:
        return self.PIPE[item]


class PyCmdLn:
    def __init__(self, **envars):
        if envars is None:
            self.envars = {}
        else:
            self.envars = envars
        self.functions = {}
        self.running = False

    def addfunc(self, name: str, func: Callable[[List[str], PyCmdInterface], None]) -> None:
        self.functions[name] = func

    def _runline(self, ln: str) -> None:
        a = digest(ln)
        cmd = a.pop(0)
        inter = PyCmdInterface(self)
        func = self.functions[cmd]
        func(a, inter)

    def mainloop(self):
        self.running = True
        while self.running:
            a = input("C:\> ")
            self._runline(a)
