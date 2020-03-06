#!/usr/bin/env python
#! -*- encoding: utf8 -*-
# 3.- Mono Library

import pickle
import random
import re
import sys

## Nombres: 

########################################################################
########################################################################
###                                                                  ###
###  Todos los métodos y funciones que se añadan deben documentarse  ###
###                                                                  ###
########################################################################
########################################################################



def sort_index(d):
    for k in d:
        l = sorted(((y, x) for x, y in d[k].items()), reverse=True)
        d[k] = (sum(x for x, _ in l), l)


class Monkey():

    def __init__(self):
        self.r1 = re.compile('[.;?!]')
        self.r2 = re.compile('\W+')


    def index_sentence(self, sentence, tri):

        """
        Este método tokeniza la frase proporcionada y saca las estadisticas
            

        :param 
            sentence: frase a tokenizar.
            tri: bool si incluir trigramas

        :return: None
        """

        sentence = self.r2.sub(" ", sentence)
        sentence = sentence.lower()
        sentence = ['$'] + sentence.split() + ['$']

        for i in range(0, len(sentence) - 1):
                
            self.index['bi'][sentence[i]] = self.index['bi'].get(sentence[i], {})
            next_word = sentence[i+1]
            self.index['bi'][sentence[i]][next_word] = self.index['bi'][sentence[i]].get(next_word, 0) + 1

        if tri:

            for i in range(0, len(sentence) - 2):      

                bigram = (sentence[i], sentence[i+1])
                self.index['tri'][bigram] = self.index['tri'].get(bigram, {})
                w = sentence[i+2]
                self.index['tri'][bigram][w] = self.index['tri'][bigram].get(w, 0) + 1
                


    def compute_index(self, filename, tri):
        """
        Este método separa el fichero en frases para procesar y generar indices
            

        :param 
            filename: el nombre del fichero.
            tri: bool si incluir trigramas

        :return: None
        """
        self.index = {'name': filename, "bi": {}}
        
        if tri:
            self.index["tri"] = {}

        
        
        fh = open(filename)

        file = fh.read()
        file.replace('\n\n', '.')
        splitted_file = self.r1.split(file)

        for line in splitted_file:
            self.index_sentence(line, tri)

        fh.close()


        sort_index(self.index['bi'])
        if tri:
            sort_index(self.index['tri'])
        

    def load_index(self, filename):
        with open(filename, "rb") as fh:
            self.index = pickle.load(fh)


    def save_index(self, filename):
        with open(filename, "wb") as fh:
            pickle.dump(self.index, fh)


    def save_info(self, filename):
        with open(filename, "w") as fh:
            print("#" * 20, file=fh)
            print("#" + "INFO".center(18) + "#", file=fh)
            print("#" * 20, file=fh)
            print("filename: '%s'\n" % self.index['name'], file=fh)
            print("#" * 20, file=fh)
            print("#" + "BIGRAMS".center(18) + "#", file=fh)
            print("#" * 20, file=fh)
            for word in sorted(self.index['bi'].keys()):
                wl = self.index['bi'][word]
                print("%s\t=>\t%d\t=>\t%s" % (word, wl[0], ' '.join(["%s:%s" % (x[1], x[0]) for x in wl[1]])), file=fh)
            if 'tri' in self.index:
                print(file=fh)
                print("#" * 20, file=fh)
                print("#" + "TRIGRAMS".center(18) + "#", file=fh)
                print("#" * 20, file=fh)
                for word in sorted(self.index['tri'].keys()):
                    wl = self.index['tri'][word]
                    print("%s\t=>\t%d\t=>\t%s" % (word, wl[0], ' '.join(["%s:%s" % (x[1], x[0]) for x in wl[1]])), file=fh)


    def generate_sentences(self, n=10):

        for i in range(0, n):

            sentence = ''
            generated_word = ''
            

            if(self.index.get('tri', False)):

                list_of_posible_starts = self.index['bi']['$']

                sentence_as_list = []

                generated_word = self.get_random_word(list_of_posible_starts)

                sentence_as_list.append(generated_word)

                generated_word = self.get_random_word(self.index['bi'][generated_word])

                sentence_as_list.append(generated_word)

                for j in range(1, 25):

                    list_of_posible_words = self.index['tri'][(sentence_as_list[j - 1], sentence_as_list[j])]
                    generated_word = self.get_random_word(list_of_posible_words)

                    if(generated_word == '$'):
                        break
                    else:
                         sentence_as_list.append(generated_word)

                sentence = " ".join(sentence_as_list)

            else:
                list_of_posible_starts = self.index['bi']['$']

                generated_word = self.get_random_word(list_of_posible_starts)
                
                sentence += generated_word

                for j in range(0, 25):

                    list_of_posible_words = self.index['bi'][generated_word]
                    generated_word = self.get_random_word(list_of_posible_words)

                    if(generated_word == '$'):
                        break
                    else:
                        sentence += ' ' + generated_word

            print(sentence)
            print('--------')




    def get_random_word(self, posible_words):
        
        words_list = []
        
        posible_words_list = posible_words[1]
        ## Append elemnts repeated by frecuency to list
        for posible_word in posible_words_list:
            for i in range(0, posible_word[0]):
                words_list.append(posible_word[1]);

        random_number = random.randint(0, posible_words[0] - 1)
        return words_list[random_number]


if __name__ == "__main__":
    print("Este fichero es una librería, no se puede ejecutar directamente")


