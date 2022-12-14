import matrix_a as ma
import os

def test1_matrix_a(input_root: str):
    example1_root = os.path.join(input_root, "example_1.txt")

    matrix_a = ma.MatrixA(example1_root, 3)

    assert len(matrix_a) == 8

    expected_m = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
    assert matrix_a.m == expected_m, f"Set M should be"

    matrix_a.load_chunk_by_number(0)
    assert matrix_a.curr_chunk == [{0, 2, 9}, {3, 6, 7, 8}, {1, 3, 7}], f"Found: {matrix_a.curr_chunk}"
    matrix_a.load_chunk_by_number(1)
    assert matrix_a.curr_chunk == [{5, 4, 1}, {4, 5, 6, 8}, {1, 2, 9}], f"Found: {matrix_a.curr_chunk}"
    matrix_a.load_chunk_by_number(2)
    assert matrix_a.curr_chunk == [{0, 4, 5}, {0, 3, 7}], f"Found: {matrix_a.curr_chunk}"

    matrix_a.load_chunk_by_index(0)
    assert matrix_a.curr_chunk == [{0, 2, 9}, {3, 6, 7, 8}, {1, 3, 7}], f"Found: {matrix_a.curr_chunk}"
    matrix_a.load_chunk_by_index(3)
    assert matrix_a.curr_chunk == [{1, 4, 5}, {4, 5, 6, 8}, {1, 2, 9}], f"Found: {matrix_a.curr_chunk}"
    matrix_a.load_chunk_by_index(5)
    assert matrix_a.curr_chunk == [{1, 4, 5}, {4, 5, 6, 8}, {1, 2, 9}], f"Found: {matrix_a.curr_chunk}"
    matrix_a.load_chunk_by_index(6)
    assert matrix_a.curr_chunk == [{0, 4, 5}, {0, 3, 7}], f"Found: {matrix_a.curr_chunk}"
    matrix_a.load_chunk_by_index(7)
    assert matrix_a.curr_chunk == [{0, 4, 5}, {0, 3, 7}], f"Found: {matrix_a.curr_chunk}"

    assert matrix_a[6] == {0, 4, 5}, f"Found: {matrix_a[6]}"
    assert matrix_a[0] == {0, 2, 9}, f"Found: {matrix_a[0]}"
    assert matrix_a.curr_chunk == [{0, 2, 9}, {3, 6, 7, 8}, {1, 3, 7}], f"Found: {matrix_a.curr_chunk}"
    assert matrix_a[3] == {1, 4, 5}, f"Found: {matrix_a[3]}"
    assert matrix_a.curr_chunk == [{1, 4, 5}, {4, 5, 6, 8}, {1, 2, 9}], f"Found: {matrix_a.curr_chunk}"

    print("Test 1 passed!")

def test2_matrix_a(input_root: str):
    file_path = os.path.join(input_root, "2_75_0_4_02092022114638.txt")

    matrix_a = ma.MatrixA(file_path)

    assert len(matrix_a) == 52, f"Found: {len(matrix_a)}"
    assert matrix_a[0] == {0, 16, 32, 48}, f"Found: {matrix_a[0]}"
    assert matrix_a[50] == {14, 31, 43, 63}, f"Found: {matrix_a[50]}"

    print("Test 2 passed!")

def test3_matrix_a(input_root: str):
    file_path = os.path.join(input_root, "3_75_0_4_02092022115236.txt")

    matrix_a = ma.MatrixA(file_path)

    assert len(matrix_a) == 561, f"Found: {len(matrix_a)}"
    assert matrix_a[0] == {0, 86, 167, 248}, f"Found: {matrix_a[0]}"
    assert matrix_a[50] == {10, 90, 171, 243}, f"Found: {matrix_a[50]}"

    print("Test 3 passed!")



if __name__ == '__main__':
    root = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "Test Inputs")
    test1_matrix_a(root)
    test2_matrix_a(root)
    test3_matrix_a(root)