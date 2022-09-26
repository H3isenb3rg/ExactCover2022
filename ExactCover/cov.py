class Cover:
    def __init__(self, full_path: str, alg: str) -> None:
        self.cov = []
        self.full_path = full_path

        # Init Out File
        filename = full_path.split("\\")[-1]

        # First comment manual to use mode 'w' and clean/create output file
        with open(self.full_path, "w") as out_file:
            out_file.write(f";;; {alg}\n")
            
        self.write_comment(f"Output of file: {filename}\n")
        
    def append(self, indexes: list):
        indexes.sort()
        self.cov.append([str(i) for i in indexes])
        with open(self.full_path, "a") as out_file:
            out_file.write(" ".join(str(i) for i in indexes))
            out_file.write(" -\n")
            out_file.flush()

    def write_comment(self, comment: str):
        with open(self.full_path, "a") as out_file:
            out_file.write(f";;; {comment}\n")
            out_file.flush()

    def execution_ended(self):
        with open(self.full_path, "a") as out_file:
            out_file.write(f"\n")
            out_file.flush()

    def __len__(self):
        return len(self.cov)