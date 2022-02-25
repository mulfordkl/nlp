from json import load
import math
import random
import sys
import os
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import brown
from collections import Counter
import string
import argparse


def load_vocabulary(vocab = "american-english") -> dict:
    if vocab == "brown":
        vocabulary_list = brown.words()
        vocabulary_length = len(vocabulary_list)
        vocabulary = {vocabulary_list[i].lower(): None for i in range(0, vocabulary_length)}
    if vocab == "american-english" or vocab == "web2":
        vocabulary_list = open("/usr/share/dict/{}".format(vocab), "r").read().split("\n")
        vocabulary = {}
        for line in vocabulary_list:
            vocabulary[line.strip().lower()] = None

    # Add our placeholder tokens
    vocabulary["<s>"] = None
    vocabulary["</s>"] = None
    vocabulary["<UNK>"] = None

    return vocabulary

def preprocess_sentence(sentence, vocabulary, trigram = False):
    sentence = list(filter(lambda x: x not in string.punctuation, sentence))
    for index, word in enumerate(sentence):
        sentence[index] = word.lower()
        if sentence[index] not in vocabulary:
            sentence[index] = "<UNK>"
    sentence.insert(0, "<s>")
    sentence.append("</s>")
    if trigram:
        sentence.insert(0, "<s>")
        sentence.append("</s>")
    return sentence
    

class NGramModel():
    def train(self, vocabulary, sentences, trigram = False):

        if not trigram:
            bigram_counts = {}
            unigram_counts = {}
            for sentence in sentences:
                sentence = preprocess_sentence(sentence, vocabulary, trigram = False)
                for index, word in enumerate(sentence):
                    if index == 0:
                        unigram_counts["<s>"] = unigram_counts.get("<s>", 0) + 1
                    else:
                        bigram = (sentence[index-1], word)
                        unigram = sentence[index-1]
                        bigram_counts[bigram] = bigram_counts.get(bigram, 0) + 1
                        unigram_counts[unigram] = unigram_counts.get(unigram, 0) + 1

            bigram_count_of_counts = Counter(bigram_counts.values())
            bigram_count_of_counts[0] = len(bigram_counts)**2 - sum(bigram_count_of_counts.values())

            unigram_count_of_counts = Counter(unigram_counts.values())
            unigram_count_of_counts[0] = len(vocabulary)**2 - sum(unigram_count_of_counts.values())
            
            return bigram_counts, unigram_counts, bigram_count_of_counts, unigram_count_of_counts

        else:
            trigram_counts = {}
            bigram_counts = {}
            for sentence in sentences:
                sentence = preprocess_sentence(sentence, vocabulary, trigram = True)
                for index, word in enumerate(sentence):
                    if index == 0:
                        continue
                    if index == 1:
                        bigram_counts[("<s>", "<s>")] = bigram_counts.get(("<s>", "<s>"), 0) + 1
                    else:
                        n_gram = (sentence[index-2], sentence[index-1], word)
                        n_1_gram = (sentence[index-2], sentence[index-1])
                        trigram_counts[n_gram] = trigram_counts.get(n_gram, 0) + 1
                        bigram_counts[n_1_gram] = bigram_counts.get(n_1_gram, 0) + 1

            trigram_count_of_counts = Counter(trigram_counts.values())
            trigram_count_of_counts[0] = len(trigram_counts)**2 - sum(trigram_count_of_counts.values())

            bigram_count_of_counts = Counter(bigram_counts.values())
            bigram_count_of_counts[0] = len(bigram_counts)**2 - sum(bigram_count_of_counts.values())
            
            return trigram_counts, bigram_counts, trigram_count_of_counts, bigram_count_of_counts



def test_model(models, vocabulary, sentences, true_author=None, trigram=False, test=False, interpolation=False):
    model_prob = {}
    total = 0
    correct = 0
    for sentence in sentences:
        if trigram:
            sentence = preprocess_sentence(sentence, vocabulary, trigram=True) 
        else:           
            sentence = preprocess_sentence(sentence, vocabulary)
        for model in models:
            n_grams = models[model]['n_gram_counts']
            n_1_grams = models[model]['n_1_gram_counts']
            n_gram_count_of_counts = models[model]['n_gram_count_counts']
            n_1_gram_count_of_counts = models[model]['n_1_gram_count_counts']

            cum_prob = 0
            for index, word in enumerate(sentence):
                #if word not in vocabulary and vocabulary.get(word,None):
                #    sentence[index] = '<UNK>'
                if trigram:
                    if index in [0, 1]:
                        continue
                    else:
                        n_gram = (sentence[index-2], sentence[index-1], word)
                        n_1_gram = (sentence[index-2], sentence[index-1])
                else:
                    if index == 0:
                        continue
                    else:
                        n_gram = (sentence[index-1], word)
                        n_1_gram = sentence[index-1]
                
                prob_num = n_grams.get(n_gram, 0.0)
                prob_denom = n_1_grams.get(n_1_gram, 0.0)

                if prob_num < 6:
                    prob_num = good_turing_smooth(prob_num, n_gram_count_of_counts)
                if prob_denom < 6:
                    prob_denom = good_turing_smooth(prob_denom, n_gram_count_of_counts)

                if interpolation:
                    cum_prob += math.log(0.2*prob_denom + 0.8*(prob_num / prob_denom))

                cum_prob += ( math.log(prob_num / prob_denom) )
            model_prob[model] = cum_prob
        max_model = max(model_prob, key=model_prob.get)
        if test:
            print(max_model)         
        else:
            if max_model == true_author:
                correct += 1
            total += 1
    if not test:
        print("Correct on {} dev set:\t{}/{}\t\t{}%".format(true_author, correct, total, round((correct/total)*100,1)))

def good_turing_smooth(counts, count_of_counts):
    smoothed_counts = (counts + 1) * ( count_of_counts[counts + 1] / count_of_counts[counts] )
    return smoothed_counts

def main():
    parser = argparse.ArgumentParser(description="Trains and tests an N-gram language model")
    parser.add_argument("author_list")
    parser.add_argument("-test")
    parser.add_argument("-trigram", action="store_true")
    parser.add_argument("-interpolation", action="store_true")
    args = parser.parse_args()

    print(args)

    vocabulary = load_vocabulary('brown')
    dev_sets = {}
    models = {}
    trigram = True if args.trigram else False
    interpolation = True if args.interpolation else False

    author_list = open(args.author_list)

    for line in author_list:
        print("Now training for file: {}".format(line.strip()))
        author_file = os.path.join("corpora", line.strip())
        author = line.strip()[:-9]

        models[author] = {}

        try:
            corpora = open(author_file, "r", encoding="utf-8").read()
        except:
            print("Could not find the corpora file in corpora/{}. Is it there?".format(line))
        if corpora:
            sentences = [word_tokenize(t) for t in sent_tokenize(corpora)]

            if args.test:
                training = sentences
            else:
                random.shuffle(sentences)
                dev_index = int(0.8 * len(sentences))
                dev_sets[author] = sentences[dev_index:]
                training = sentences[:dev_index]


            Model = NGramModel()
            n_gram, n_1_gram, n_gram_count_counts, n_1_gram_count_counts = Model.train(vocabulary, training, trigram)

            models[author]["n_gram_counts"] = n_gram
            models[author]["n_1_gram_counts"] = n_1_gram
            models[author]["n_gram_count_counts"] = n_gram_count_counts
            models[author]["n_1_gram_count_counts"] = n_1_gram_count_counts

    if args.test:
        try:
            test_sentences = open(args.test, "r", encoding="utf-8").read().split("\n")
            test_sentences = [word_tokenize(t) for t in test_sentences]
            test_model(models, vocabulary, test_sentences, trigram, test=True)
        except:
            print("Could not open test file, is the path correct?")        
    else:
        test_model(models, vocabulary, dev_sets["austen"], "austen", trigram, args.test, interpolation)
        test_model(models, vocabulary, dev_sets["dickens"], "dickens", trigram, args.test, interpolation)
        test_model(models, vocabulary, dev_sets["tolstoy"], "tolstoy", trigram, args.test, interpolation)
        test_model(models, vocabulary, dev_sets["wilde"], "wilde", trigram, args.test, interpolation)

    return 
        
if __name__ == '__main__':
    main()
