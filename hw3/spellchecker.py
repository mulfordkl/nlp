import os, re, sys

# Get word list from file

def get_words_list():
    path = "/usr/share/dict/words"
    print(path)
    if os.path.exists(path):
        word_file = open(path, "r")
        content = word_file.read()
        return content.split("\n")
    else:
        print("Cannot find word list at /usr/share/dict/words.")
        return []

# Tokenize the lines. This basically assumes clitics are spelled correctly.

def tokenize_line(line: str):
    pattern = r"""(?x)                   
                       (?:[A-Z]\.)+           # abbreviations
                       |\d+(?:\.\d+)?%?       # percentages
                       |\w+(?:[']\w+)*       # words with apostrophes
                       |(?:[+/\-@&*,.;:!?$-])         # punctuation
                     """
    tokens = re.findall(pattern, line)
    return tokens

###############################################################################
#  Narrow down the list of candidate words by:
#   1. Only looking at words with length within 1 of the token
#   2. Only including words with the same first letter or with a different
#      letter if swapping that letter for the first letter of the token
#      results in a word on the list. For example - if the token is 'darge'
#      then words that start with "l" and "b" would be included because
#      "large" and "barge" are words but "k" would not ("karge").
#
###############################################################################

def organize_word_list_by_length(word_list):
    word_dict = {}
    for word in word_list:
        word_length = len(word)
        word_dict.setdefault(word_length,[]).append(word.lower())
    return word_dict

def organize_word_list_by_letter(word_list):
    word_dict = {}
    for word in word_list:
        start_letter = word[0]
        word_dict.setdefault(start_letter,[]).append(word)
    return word_dict

def get_word_list_by_length(word_dict, length):
    word_list = []

    if length in word_dict:
        word_list += word_dict[length]
    if length-1 in word_dict:
        word_list += word_dict[length-1]
    if length+1 in word_dict:
        word_list += word_dict[length+1]
    
    return word_list

def get_word_list_by_letter(word_dict, token):
    word_list = []
    for key in word_dict:
        new_token = key + token[1:]
        if new_token in word_dict[key] or token[0] == key:
            word_list += word_dict[key]
    return word_list

def narrow_word_list(word_list, token):
    word_list = get_word_list_by_length(organize_word_list_by_length(word_list), len(token))
    word_list = get_word_list_by_letter(organize_word_list_by_letter(word_list), token)
    return word_list

# Implement edit distance
# Takes two strings and three cost integers

def edit_distance(m: str, c: str, del_cost: int, ins_cost: int, sub_cost: int):
    # Set up rows and columns
    n_rows = len(m) + 1
    n_columns = len(c) + 1
    # Create matrix
    matrix = [[0 for column in range(n_columns)] for row in range(n_rows)]        
    for column in range(1, n_columns):
        # Set up the insertion costs for the empty string
        matrix[0][column] = column * ins_cost
        for row in range(1, n_rows):
            # Set up the deletion costs for the empty string
            matrix[row][0] = row * del_cost
            if m[row-1] == c[column-1]:
                s_cost = 0
            else:
                s_cost = sub_cost
            matrix[row][column] = min(matrix[row-1][column] + del_cost,
                                      matrix[row][column-1] + ins_cost,      
                                      matrix[row-1][column-1] + s_cost)
    # Grab the corner value. 
    dist = matrix[n_rows-1][n_columns-1]
    return dist

# Suggest words by retrieving the three closest words in edit distance

def suggest(ms_word: str, candidate_list: list):
    suggestions = {}
    for word in candidate_list:
        suggestions[word] = edit_distance(ms_word, word, 1, 1, 2)
    
    suggestions = sorted(suggestions.items(), key=lambda x: x[1])

    return suggestions[:3]

# Piece line back together with appropriate punctuation

def reconstruct_line(tokens: list):
    new_line = ' '.join(tokens)
    new_line = re.sub(r" - ", r"-", new_line)
    new_line = re.sub(r" \$ ", r" $", new_line)
    new_line = re.sub(r" ([,.;:!?]+)", r"\1", new_line)

    return new_line


def main():
    # Get corrected and uncorrected file and entire word list
    uncorrected_file = open(sys.argv[1])
    corrected_file = open("corrected_" + sys.argv[1], "w")
    word_list = get_words_list()
    
    line_num = 0
    for line in uncorrected_file:
        line_num += 1  
        tokens = tokenize_line(line)
        for index, token in enumerate(tokens):
            upper_flag = token[0].isupper() # Stash whether the token was capitalized
            token = token.lower()
            if token not in word_list and re.fullmatch("[a-zA-Z]+", token): # Only check misspellings for tokens with a-z letters
                word_candidates = narrow_word_list(word_list, token)
                suggestions = suggest(token, word_candidates)
                tokens[index] = suggestions[0][0]
                if upper_flag:
                    tokens[index] = tokens[index].capitalize()
                print("Misspelled token found in line {}: {}\nSuggested words: \n".format(line_num, token, suggestions))
                for index in suggestions:
                    print("\t{}".format(index[0]))
                print("\n")
        corrected_line = reconstruct_line(tokens) + "\n"
        corrected_file.write(corrected_line)

if __name__ == '__main__':
    main()