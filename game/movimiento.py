class Movimiento:
    # Mapeado de filas y columnas para los movimientos.
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {val: key for key, val in ranksToRows.items()}  # Invertimos el diccionario
    filToCol = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colToFil = {val: key for key, val in filToCol.items()}

    def __init__(self, start, end, tb, en_passant_posible=False, is_castle=False):
        self.startFil = start[0]
        self.startCol = start[1]
        self.endFil = end[0]
        self.endCol = end[1]
        self.piezaMov = tb[self.startFil][self.startCol]
        self.piezaCap = tb[self.endFil][self.endCol]  # Recordar la opción de "--"
        self.moveID = self.startFil * 1000 + self.startCol * 100 + self.endFil * 10 + self.endCol
        # self.isEnPassant = False
        # Movimientos únicos
        self.isEnPassant = en_passant_posible
        if self.isEnPassant:
            self.piezaCap = 'bp' if self.piezaMov == 'wp' else 'wp'
        # Promoción
        self.isPromocion = (self.piezaMov == 'wp' and self.endFil == 0) or (self.piezaMov == 'bp' and self.endFil == 7)
        # Castling
        self.isCastle = is_castle
        self.isCaptura = self.piezaCap != '--'

    def get_basic_move_notation(self):
        return self.get_rank_file(self.startFil, self.startCol) + self.get_rank_file(self.endFil, self.endCol)

    # def get_FEN_notation(self):

    def get_rank_file(self, fil, col):
        return self.colToFil[col] + self.rowsToRanks[fil]

    # Override del equals como en Java para comparar objetos entre sí
    def __eq__(self, other):
        if isinstance(other, Movimiento):
            return self.moveID == other.moveID
        return False

    def __str__(self):
        if self.isCastle:
            return "O-O" if self.endCol == 6 else "O-O-O"

        final_sq = self.get_rank_file(self.endFil, self.endCol)
        if self.piezaMov[1] == 'p':
            if self.isCaptura:
                return self.colToFil[self.startCol] + "x" + final_sq
            else:
                return final_sq

        mov_texto = self.piezaMov[1]
        if self.isCaptura:
            mov_texto += 'x'
        return mov_texto + final_sq
