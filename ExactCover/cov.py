import os

class Cover:
    def __init__(self, dir_path: str, filename: str, alg: str) -> None:
        self.cov = []

        self.dir_path = os.path.join(os.path.join(dir_path, filename.split(".")[0]), alg)
        os.makedirs(self.dir_path, exist_ok=True)

        self.alg = alg
        self.filename = filename

        self.comments_path = os.path.join(self.dir_path, f"comments.txt")
        self.results_path = os.path.join(self.dir_path, filename)

    def init_out_file(self):
        """Creates/Resets the comments and results file"""
        # Clear the results file
        open(self.results_path, "w").close()

        # Init the comments file
        self.write_comment(f"Exact Coever Version = {self.alg}", mode="w")            
        self.write_comment(f"Input file = {self.filename}")
        
    def append(self, indexes: list):
        indexes.sort()
        self.cov.append([str(i) for i in indexes])
        with open(self.results_path, "a") as out_file:
            out_file.write(" ".join(str(i) for i in indexes))
            out_file.write(" -\n")

    def write_comment(self, comment: str, begin: str ="", end: str="\n", mode: str="a"):
        with open(self.comments_path, mode, encoding='UTF-8') as out_file:
            out_file.write(f"{begin}{comment}{end}")

    def cardinalities_distribution(self) -> dict:
        cards = {}
        for cov in self.cov:
            card = len(cov)
            if card in cards.keys():
                cards[card]+=1
            else:
                cards[card] = 1

        return cards            

    def __len__(self):
        return len(self.cov)