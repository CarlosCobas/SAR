#! -*- encoding: utf8 -*-



## Nombres: Carlos Enrique Pérez Cobas

########################################################################
########################################################################
###                                                                  ###
###  Todos los métodos y funciones que se añadan deben documentarse  ###
###                                                                  ###
########################################################################
########################################################################

import argparse
import re
import sys


def sort_dic_by_values(d, asc=True):
    return sorted(d.items(), key=lambda a: (-a[1], a[0]))

class WordCounter:

    def __init__(self):
        """
           Constructor de la clase WordCounter
        """
        self.clean_re = re.compile('\W+')

    def write_stats(self, filename, stats, use_stopwords, full):
        """
        Este método escribe en fichero las estadísticas de un texto
            

        :param 
            filename: el nombre del fichero destino.
            stats: las estadísticas del texto.
            use_stopwords: bclean_reooleano, si se han utilizado stopwords
            full: boolean, si se deben mostrar las stats completas

        :return: None
        """
        with open(filename, 'w') as fh:
            fh.write("N words " + str(stats['nwords']) + "\n")
            fh.write("N lines " + str(stats['nlines']) + "\n")
            fh.write("Words (alphabetical order):\n")
            for key in sorted(stats['word'].keys()):
                fh.write("\t" + key + " : " + str(stats['word'][key]) + "\n")            
            pass
        


    def file_stats(self, filename, lower, stopwordsfile, bigrams, full):
        """
        Este método calcula las estadísticas de un fichero de texto
            

        :param 
            filename: el nombre del fichero.
            lower: booleano, se debe pasar todo a minúsculas?
            stopwordsfile: nombre del fichero con las stopwords o None si no se aplican
            bigram: booleano, se deben calcular bigramas?
            full: booleano, se deben montrar la estadísticas completas?

        :return: None
        """

        stopwords = [] if stopwordsfile is None else open(stopwordsfile).read().split()

        # variables for results

        sts = {
                'nwords': 0,
                'nlines': 0,
                'word': {},
                'symbol': {}
                }

        if bigrams:
            sts['biword'] = {}
            sts['bisymbol'] = {}

        words = {}
        symbols = {}
        bigrams_words = {}
        bigrams_symbols = {}


        io_file = open(filename)
        line_count = 0 
        words_count = 0
        symbols_count = 0

        for line in io_file:
            line_count += 1
            
            #Cleaning the input line from non alphanumeric values
            clean_line = self.clean_re.sub(" ", line)

            #Check if user wants lowercase only    
            if lower:
                clean_line = clean_line.lower()

            #breaking line to list of words 
            clean_line_list = clean_line.split()


            for word in clean_line_list:
                if word not in stopwords:

                    words_count += 1
                    words[word] = words.get(word, 0) + 1

                    for symbol in word:
                        symbols_count += 1
                        symbols[symbol] = symbols.get(symbol, 0) + 1
                    
                    if bigrams:
                        bigrams_word = ['$'] + word + ['$']
                        for i in range(len(bigrams_word)):
                            w1, w2 = bigrams_list[i : i + 2]
                            bigrams_symbols[(w1,w2)] = bigrams_symbols.get((w1,w2), 0) + 1



            if bigrams:
                bigrams_list = ['$'] + clean_line_list + ['$']
                for i in range(len(bigrams_list)):
                    w1, w2 = bigrams_list[i : i + 2]
                    bigrams_words[(w1,w2)] = bigrams_words.get((w1,w2), 0) + 1


        sts['nlines'] = line_count
        sts['nwords'] = words_count
        sts['word'] = words
        sts['symbol'] = symbols
        sts['biword'] = bigrams_words
        sts['bisymbol'] = bigrams_symbols
        sts['unique_words'] = len(words)
        sts['unique_symbols'] = len(symbols)


        new_filename = "" 
        s = filename.split('.')
        if len(s) > 1:
            new_filename = s[0] + '_stats' + '.' + s[1]
        else: 
            new_filename = s[0] + '_stats'

        self.write_stats(new_filename, sts, stopwordsfile is not None, full)


    def compute_files(self, filenames, **args):
        """
        Este método calcula las estadísticas de una lista de ficheros de texto
            

        :param 
            filenames: lista con los nombre de los ficheros.
            args: argumentos que se pasan a "file_stats".

        :return: None
        """

        for filename in filenames:
            self.file_stats(filename, **args)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Compute some statistics from text files.')
    parser.add_argument('file', metavar='file', type=str, nargs='+',
                        help='text file.')

    parser.add_argument('-l', '--lower', dest='lower', action='store_true', default=False, 
                    help='lowercase all words before computing stats.')

    parser.add_argument('-s', '--stop', dest='stopwords', action='store',
                    help='filename with the stopwords.')

    parser.add_argument('-b', '--bigram', dest='bigram', action='store_true', default=False, 
                    help='compute bigram stats.')

    parser.add_argument('-f', '--full', dest='full', action='store_true', default=False, 
                    help='show full stats.')

    args = parser.parse_args()
    wc = WordCounter()
    wc.compute_files(args.file, lower=args.lower, stopwordsfile=args.stopwords, bigrams=args.bigram, full=args.full)