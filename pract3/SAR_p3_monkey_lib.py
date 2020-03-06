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
        self.r1 = re.compile('[.;?!]|(\n\n)')
        self.r2 = re.compile('\W+')


    def index_sentence(self, sentence, tri):

        sentence = self.r2.sub(" ", sentence)
        sentence = sentence.lower()
        sentence = ['$'] + sentence.split() + ['$']

        for i in range(0, len(sentence) - 1):
                
            self.index['bi'][sentence[i]] = self.index['bi'].get(sentence[i], {})
            next_word = sentence[i+1]
            self.index['bi'][sentence[i]][next_word] = self.index['bi'][sentence[i]].get(next_word, 0) + 1

        if tri:

            for i in range(0, len(sentence) - 2):
                
                self.index['tri'][sentence[i]] = self.index['tri'].get(sentence[i], {})
                w1 = sentence[i+1]
                w2 = sentence[i+2]

                self.index['tri'][sentence[i]][(w1,w2)] = self.index['tri'][sentence[i]].get((w1,w2), 0) + 1
                


        
    


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

        raw_sentence = ""
        
        fh = open(filename)

        for line in fh:
            matches = self.r1.match(line)
            groups = matches.groups()

            for i in range(0, len(groups) - 1):
                self.index_sentence(groups[i], tri)
            
            raw_sentence += groups[len(groups) - 1]

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
        #############
        # COMPLETAR #
        #############
        pass


if __name__ == "__main__":
    print("Este fichero es una librería, no se puede ejecutar directamente")


