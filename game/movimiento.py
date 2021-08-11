class Movimiento:
    # Mapeado de filas y columnas para los movimientos.
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {val: key for key, val in ranksToRows.items()}  # Invertimos el diccionario
    filToCol = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colToFil = {val: key for key, val in filToCol.items()}

    def __init__(self, start, end, tb):
        self.startFil = start[0]
        self.startCol = start[1]
        self.endFil = end[0]
        self.endCol = end[1]
        self.piezaMov = tb[self.startFil][self.startCol]
        self.piezaCap = tb[self.endFil][self.endCol]  # Recordar la opción de "--"

    def get_basic_move_notation(self):
        return self.get_rank_file(self.startFil, self.startCol) + self.get_rank_file(self.endFil, self.endCol)

    # def get_FEN_notation(self):

    def get_rank_file(self, fil, col):
        return self.colToFil[col] + self.rowsToRanks[fil]
