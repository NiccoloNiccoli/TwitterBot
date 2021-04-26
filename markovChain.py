import random
from scipy.sparse import dok_matrix
import os
import glob


class MarkovChain:
    training_list = {}
    k = 0
    lChain = 0
    distinct_words = {}
    k_words_idx_dict = {}
    next_after_k_words_matrix = {}

    def __init__(self, fileList, chainLength=30, nWords=3):
        self.training_list = fileList
        self.k = nWords
        self.lChain = chainLength

    def loadAnalyzeCorpus(self, encodingVersion='utf-16'):
        def __opendocument(files_list):
            _corpus = []
            for files in files_list:
                document = open('./src/'+files, encoding=encodingVersion).read()
                currentcorpus = document.replace('\n', ' ')
                currentcorpus = currentcorpus.replace('\t', ' ')
                currentcorpus = currentcorpus.replace('“', ' " ')
                currentcorpus = currentcorpus.replace('”', ' " ')
                currentcorpus = currentcorpus.replace('_', ' " ')
                for spaced in ['.', '-', ',', '!', '?', '(', '—', ')']:
                    currentcorpus = currentcorpus.replace(spaced, ' {0} '.format(spaced))
                currentcorpus = currentcorpus.replace('\ufeff', ' ')
                # print(len(corpus))
                currentcorpus_words = currentcorpus.split(' ')
                _corpus += currentcorpus_words

            return _corpus

        corpus_words = __opendocument(self.training_list)
        corpus_words = [word for word in corpus_words if word != '']
        # print(len(corpus_words))
        self.distinct_words = list(set(corpus_words))  # per avere una sola volta ogni parola
        # print(len(distinct_words))
        word_idx_dict = {word: i for i, word in enumerate(self.distinct_words)}  # associa ad ogni parola un numero
        distinct_words_count = len(self.distinct_words)
        # print('...')

        # numero di parole che formano le n-uple

        sets_of_k_words = [' '.join(corpus_words[i:i + self.k]) for i, _ in enumerate(corpus_words[:-self.k])]
        # print(sets_of_k_words) #crea delle n-uple di parole

        distinct_sets_ok_k_words = list(set(sets_of_k_words))
        sets_count = len(distinct_sets_ok_k_words)
        print(sets_count)
        self.next_after_k_words_matrix = dok_matrix((sets_count, distinct_words_count))
        self.k_words_idx_dict = {word: i for i, word, in enumerate(distinct_sets_ok_k_words)}
        # print(k_words_idx_dict)

        for i, word in enumerate(sets_of_k_words[:-self.k]):
            word_sequence_idx = self.k_words_idx_dict[word]
            next_word_idx = word_idx_dict[corpus_words[i + self.k]]
            self.next_after_k_words_matrix[word_sequence_idx, next_word_idx] += 1
        print('blip blop, corpus analyzed')

    def generateSentence(self, seedString=''):
        if not seedString:
            print(len(self.k_words_idx_dict))
            _seedString = random.choice(list(self.k_words_idx_dict.items()))
            seedString = _seedString[0]
            print(seedString)


        def sample_next_word_after_sequence(word_sequence, alpha=0.0):  # alpha è la possibilità che la rete tiri fuori un valore a caso
            # print(next_after_k_words_matrix[k_words_idx_dict[word_sequence]])
            # TODO: se non esiste la corrispondenza all'interno della matrice mettere un punto e ricominciare
            # TODO: un'altra frase.
            next_word_vector = self.next_after_k_words_matrix[self.k_words_idx_dict[word_sequence]] + alpha
            likelihoods = next_word_vector / next_word_vector.sum()  # viene calcolata la probabilità che ciascuno degli elementi esca data una certa parola
            # print(next_word_vector)
            # print('blip blop')
            # print(next_word_vector.sum())
            # print(str(likelihoods.toarray().size))
            # print('shape '+ str(likelihoods.toarray().shape))
            # print(len(distinct_words))
            likelihoods_array = likelihoods.T  # qui faccio la trasposizione del vettore
            # print(likelihoods_array.size)
            # print(len(likelihoods_array))
            # print('shape ' + str(likelihoods_array.shape))
            return random.choices(self.distinct_words, weights=(next_word_vector + alpha).T, k=1)

        def stochastic_chain(seed=seedString, chain_length=self.lChain, seed_length=self.k):
            current_words = seed.split(' ')
            if len(current_words) != seed_length:
                raise ValueError(f'wrong number of words in the seed, expected {seed_length}')
            sentence = seed

            for _ in range(chain_length):
                sentence += ' '
                # print(sentence)
                next_word = sample_next_word_after_sequence(' '.join(current_words), 0.0)
                # print(next_word)
                next_word = (''.join(next_word))
                sentence += next_word
                current_words = current_words[1:] + [next_word]
                # print(current_words)
            return sentence

        return stochastic_chain(seedString)
