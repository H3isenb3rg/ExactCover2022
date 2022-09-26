class Cover:
    def __init__(self, full_path: str, alg: str) -> None:
        self.cov = []
        self.full_path = full_path

        # Init Out File
        filename = full_path.split("\\")[-1]
        
        self.write_comment(alg, mode="w")            
        self.write_comment(f"Output of file: {filename}\n")
        
    def append(self, indexes: list):
        indexes.sort()
        self.cov.append([str(i) for i in indexes])
        with open(self.full_path, "a") as out_file:
            out_file.write(" ".join(str(i) for i in indexes))
            out_file.write(" -\n")
            out_file.flush()

    def write_comment(self, comment: str, begin: str =";;; ", end: str="\n", mode: str="a"):
        with open(self.full_path, mode, encoding='UTF-8') as out_file:
            out_file.write(f"{begin}{comment}{end}")
            out_file.flush()

    def __len__(self):
        return len(self.cov)