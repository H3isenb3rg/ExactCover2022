import app
import os


if __name__ == '__main__':
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    app.run(root)
