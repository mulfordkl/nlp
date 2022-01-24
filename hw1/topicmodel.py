import sys
import re

def count_words(f, len_thresh):
    """
    This is a function that takes a file and outputs a dictionary
    of the counts of individual words, sorted by how often the word occurs.
    It also removes puncuation.
    """
    word_count = {}
    for line in f:
        # Remove puncutation
        line = re.sub(r'[^\w\s]', '', line)
        for word in line.split():
            # Only keep big words
            if len(word) > len_thresh:
                if word not in word_count:
                    word_count[word] = 1
                else:
                    word_count[word] += 1                
    return {k: v for k, v in sorted(word_count.items(), key=lambda item: item[1], reverse=True)}

def main():
    f = open(sys.argv[1])
    word_counts = count_words(f, 7)
    for ii in range(5):
        print(list(word_counts)[ii])
    f.close()

if __name__ == '__main__':
    main()