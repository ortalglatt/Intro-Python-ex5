import os
import sys


ARGS_LENGTH = 4
WORDS_IN_ARGS = 0
MATRIX_IN_ARGS = 1
OUTPUT_IN_ARGS = 2
DIRECTIONS_IN_ARGS = 3
DIRECTIONS = ['u', 'd', 'r', 'l', 'w', 'x', 'y', 'z']
ERROR_DEFAULT_MSG = "ERROR!"
ARGS_LEN_MSG = " There is more or less then 4 parameters."
WORD_LIST_MSG = " The word list file doesn't exist."
MATRIX_MSG = " The matrix file doesn't exist."
DIRECTIONS_MSG = " The directions are not valid."
SPACE = " "
COMMA = ","
ENTER = "\n"
WORD_IN_TUPLE = 0
NUM_IN_TUPLE = 1


def is_args_valid(args):
    """This function get a list of strings and check if their are 4 strings in
    the list, if the word list file and the matrix file are exist, and if the
    directions are valid. It returns a msg with the current errors."""
    msg = ERROR_DEFAULT_MSG
    if len(args) != ARGS_LENGTH:
        msg += ARGS_LEN_MSG
    elif not os.path.isfile(args[WORDS_IN_ARGS]):
        msg += WORD_LIST_MSG
    elif not os.path.isfile(args[MATRIX_IN_ARGS]):
        msg += MATRIX_MSG
    else:
        for letter in args[DIRECTIONS_IN_ARGS]:
            if letter != SPACE and letter not in DIRECTIONS:
                msg += DIRECTIONS_MSG
    return msg


def check_input_args(args):
    """This function get a list of strings and check if it's a valid list. If
    the list is valid, it returns None. If the list isn't valid, it returns an
    error message."""
    msg = is_args_valid(args)
    if msg == ERROR_DEFAULT_MSG:
        return None
    else:
        return msg


def read_wordlist_file(filename):
    """This function get a name of a word list file, and return a list of the
    words that appear in the given file."""
    words = []
    file_words = open(filename)
    for line in file_words:
        word = str(line.strip())
        words.append(word)
    file_words.close()
    return words


def read_matrix_file(filename):
    """This function get a name of a matrix file, and return a list of lists of
    all the letters in every line."""
    matrix = []
    file_matrix = open(filename)
    for line in file_matrix:
        matrix_line = line.strip().split(COMMA)
        matrix.append(matrix_line)
    file_matrix.close()
    return matrix


def times_word_in_string(word, string, counter):
    """This function get a word, a string and a counter, and count how many
    times the word appear in the string. It returns the current counter."""
    while word in string:
        counter += 1
        word_index = string.index(word)
        string = string[word_index + 1:]
    return counter


def words_in_mat_left_to_right(word_list, matrix, words_and_times_dic):
    """This function get a word list and a matrix, and return a dictionary of
    the words that appear from right to left in the matrix, and how many times
    they appear."""
    for word in word_list:
        word_counter = 0
        for row in matrix:
            row_str = ''.join(row)
            word_counter = times_word_in_string(word, row_str, word_counter)
        if word_counter > 0:
            words_and_times_dic[word] += word_counter
    return


def mat_reverse_rows(matrix):
    """This function take a matrix (list of lists), and return a new matrix
    that it's rows contain the same letters in the opposite order."""
    reverse_matrix = list()
    for row in matrix:
        new_row = row[::-1]
        reverse_matrix.append(new_row)
    return reverse_matrix


def mat_transpose(matrix):
    """This function take a matrix (list of lists), and return the transposed
    matrix, by turning every row to a column."""
    row_len = len(matrix[0])
    col_len = len(matrix)
    new_matrix = list()
    for row in range(row_len):
        new_row = list()
        for col in range(col_len):
            new_row.append(matrix[col][row])
        new_matrix.append(new_row)
    return new_matrix


def without_max_diagonal_list(matrix, row_len, col_len, max_diagonal):
    """This function get a matrix and some datums about the matrix, and return
    a list of all the diagonals that their length is smaller then the length of
    the that smaller then the maximum diagonal."""
    new_matrix_1 = list()
    for i in range(1, max_diagonal):
        new_row_1 = list()
        new_row_2 = list()
        for j in range(i):
            new_row_1.append(matrix[j][row_len-i+j])
            new_row_2.append(matrix[col_len-i+j][j])
        new_matrix_1.append(new_row_1)
        new_matrix_1.append(new_row_2)
    return new_matrix_1


def max_diagonal_list(matrix, row_len, col_len, max_diagonal):
    """This function get a matrix and some datums about the matrix, and return
    a list of all the diagonals that their length is equal to the length of the
    maximum diagonal."""
    num_max_diagonals = max(row_len, col_len) - max_diagonal + 1
    new_matrix_2 = list()
    for i in range(num_max_diagonals):
        new_list = list()
        if col_len >= row_len:
            for j in range(max_diagonal):
                new_list.append(matrix[i+j][j])
        else:
            for j in range(max_diagonal):
                new_list.append(matrix[j][i+j])
        new_matrix_2.append(new_list)
    return new_matrix_2


def mat_diagonal_rows(matrix):
    """This function get a matrix and return a list of lists, that every
    sublist contain the letters in one of the diagonals."""
    row_len = len(matrix[0])
    col_len = len(matrix)
    max_diagonal = min(row_len, col_len)

    new_matrix_1 = without_max_diagonal_list(matrix, row_len, col_len,
                                             max_diagonal)
    new_matrix_2 = max_diagonal_list(matrix, row_len, col_len, max_diagonal)
    new_matrix = new_matrix_1 + new_matrix_2
    return new_matrix


def dictionary_to_list(dic):
    """This function get a dictionary and return a list of tuples. Every tuple
    contains the key and the value."""
    words_and_times = list()
    for word in dic:
        if dic[word] != 0:
            new_tuple = (word, dic[word])
            words_and_times.append(new_tuple)
    return words_and_times


def find_words_in_matrix(word_list, matrix, directions):
    """This function get a word list, a matrix and a string of letters, that
    every letter symbolize a direction. The function check how many times every
    word from the word list appear in the matrix in the given directions, and
    return a list of all the words with the times they appear."""
    words_and_times_dic = {word: 0 for word in word_list}
    if 'r' in directions:
        words_in_mat_left_to_right(word_list, matrix, words_and_times_dic)
    if 'l' in directions:
        l_matrix = mat_reverse_rows(matrix)
        words_in_mat_left_to_right(word_list, l_matrix, words_and_times_dic)
    if 'd' in directions:
        d_matrix = mat_transpose(matrix)
        words_in_mat_left_to_right(word_list, d_matrix, words_and_times_dic)
    if 'u' in directions:
        u_matrix = mat_reverse_rows(mat_transpose(matrix))
        words_in_mat_left_to_right(word_list, u_matrix, words_and_times_dic)
    if 'y' in directions:
        y_matrix = mat_diagonal_rows(matrix)
        words_in_mat_left_to_right(word_list, y_matrix, words_and_times_dic)
    if 'z' in directions:
        z_matrix = mat_diagonal_rows(mat_reverse_rows(matrix))
        words_in_mat_left_to_right(word_list, z_matrix, words_and_times_dic)
    if 'w' in directions:
        w_matrix = mat_diagonal_rows(mat_reverse_rows(mat_transpose(matrix)))
        words_in_mat_left_to_right(word_list, w_matrix, words_and_times_dic)
    if 'x' in directions:
        x_matrix = mat_reverse_rows(mat_diagonal_rows(matrix))
        words_in_mat_left_to_right(word_list, x_matrix, words_and_times_dic)
    words_and_times = dictionary_to_list(words_and_times_dic)
    return words_and_times


def write_output_file(results, output_filename):
    """This function get a list of tuples and a filename. if the file is
    already exist, it will delete the existing file and create a new one.
    Otherwise, it will create a new file with the given filename. This file
    will contain all the tuples as a string in a different row."""
    output_file = open(output_filename, "w+")
    for i in range(len(results)):
        word = str(results[i][WORD_IN_TUPLE])
        times = str(results[i][NUM_IN_TUPLE])
        output_file.write(word + COMMA + times + ENTER)
    output_file.close()
    return


def word_search(args):
    """This function get a list of 4 strings, check if the input is valid, if
    not it return an error message. If it is valid, the list contains the words
    list filename, the matrix filename, the output filename and the directions.
    The function will do the words search in the matrix and create a file of
    the output results."""
    args_check = check_input_args(args)
    if args_check is not None:
        return args_check
    else:
        word_list = read_wordlist_file(args[WORDS_IN_ARGS])
        matrix = read_matrix_file(args[MATRIX_IN_ARGS])
        output_filename = args[OUTPUT_IN_ARGS]
        directions = args[DIRECTIONS_IN_ARGS]
        results = find_words_in_matrix(word_list, matrix, directions)
        write_output_file(results, output_filename)
    return


if __name__ == "__main__":
    args = sys.argv[1:]
    word_search(args)
