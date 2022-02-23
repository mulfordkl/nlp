import math
import sys
import os
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import brown

vocabulary_list = open("/usr/share/dict/web2", "r").read().split("\n")
vocabulary = {}
for line in vocabulary_list:
    vocabulary[line.strip().lower()] = None
vocabulary_length = len(vocabulary_list)
#print(vocabulary_length)
#vocabulary = {vocabulary_list[i].lower(): None for i in range(0, vocabulary_length)}

class NGramModel():
    def __init__(self, ngrams=2):
        self.ngrams = ngrams

    def train(self, sentences, smoothing = False):
        for sentence in sentences:
            for index, word in enumerate(sentence):
                print(word.lower())
                if word.lower() not in vocabulary:
                    sentence[index] = "<UNK>"
        print(sentence)

def main():
    author_list = open(sys.argv[1])
    for line in author_list:
        print("Now training for file: {}".format(line.strip()))
        author_file = os.path.join("corpora", line.strip())
        try:
            corpora = open(author_file, "r").read()
        except:
            print("Could not find the corpora file in corpora/{}. Is it there?".format(line))
        if corpora:
            sentences = [word_tokenize(t) for t in sent_tokenize(corpora)]
            print("Number of sentences: {}".format(len(sentences)))
            AustenModel = NGramModel()
            AustenModel.train(sentences[0:5])

    return 
        
if __name__ == '__main__':
    main()
