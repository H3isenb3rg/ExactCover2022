class MatrixA(object):
    def __init__(self, file_path: str) -> None:
        self.chunk = 50
        self.curr_chunk = 0
        # Apro file
        # Salvo riga di inizio della matrice
        # Salvo M
        # Leggo le prime 'chunck' righe

        # Conto righe rimanenti e salvo numero
        self.len=0
        pass

    def __len__(self):
        return self.len

    def __getitem__(self, key):
        # Se indice richiesto dentro chunk attuale allora ritorno set
        # Altrimenti carico chunk richiesto e ritorno set
        pass

    def load_next_chunk(self, i: int):
        pass

    