import config_parser
import sudoku_gen
import os

def run():
    """Executes the input generator"""
    base, rate = config_parser.parse_config()
    sudoku = sudoku_gen.Sudoku(base, rate)
    root_dir = os.path.join(os.getcwd(), "InputGenerator")
    input_dir = os.path.join(root_dir, "Generated Inputs")
    input_file_path = os.path.join(input_dir, "new_input.txt")

    with open(input_file_path, "w", encoding='UTF-8') as input_file:
        input_file.write(str(sudoku))


if __name__ == '__main__':
    run()