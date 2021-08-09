class Movimiento:
    def __init__(self, start, end, tb):
        self.startFil = start[0]
        self.startCol = start[1]
        self.endFil = end[0]
        self.endCol = end[1]
        self.piezaMov = tb[self.startFil][self.startCol]
        self.piezaCap = tb[self.endFil][self.endCol] # Recordar la opción de "--"
