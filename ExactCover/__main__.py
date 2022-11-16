import app
import os

if __name__ == '__main__':
    root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    input_root = os.path.join(root, "Inputs")
    output_path = os.path.join(root, "Outputs")
    app.launch(input_root, output_path)
