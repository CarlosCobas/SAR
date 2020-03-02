#! -*- encoding: utf8 -*-

##NOTA: Se ha implementado la ampliación del cálculo de bigramas

## Nombres: Carlos Enrique Pérez Cobas
##          Steven Alejandro Valencia Bonilla


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
import operator


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
            fh.write("Lines: " + str(stats['nlines']) + "\n")
            if not use_stopwords:
                fh.write("Number words (including stopwords): " + str(stats['nwords']) + "\n")
            else:
                fh.write("Number words (including stopwords): " + str(stats['total_words']) + "\n")
                fh.write("Number words (without stopwords): " + str(stats['nwords']) + "\n")
            fh.write("Vocabulary size: " + str(stats['unique_words']) + "\n")
            fh.write("Number of symbols: " + str(stats['nsymbols']) + "\n")
            fh.write("Number of different symbols: " + str(stats['unique_symbols']) + "\n")
            fh.write("Words (alphabetical order): \n")
            
            if full:
                for key in sorted(stats['word'].keys()):
                    fh.write("\t" + key + ": " + str(stats['word'][key]) + "\n")
                pass
                fh.write("Words (by frequency):\n")
                for key, value in sort_dic_by_values(stats['word']):
                    fh.write("\t" + key + ": " + str(value) + "\n")
                pass
                fh.write("Symbols (alphabetical order):\n")
                for key in sorted(stats['symbol'].keys()):
                    fh.write("\t" + key + ": " + str(stats['symbol'][key]) + "\n")            
                pass
                fh.write("Symbols (by frequency):\n")
                for key, value in sort_dic_by_values(stats['symbol']):
                    fh.write("\t" + key + ": " + str(value) + "\n")
                pass

                #Bigrams and bisymbols
                fh.write("Word pairs (alphabetical order):\n")
                for (key) in sorted(stats['biword']):
                    if (key[0] is "$" and key[1] is "$"):
                        pass
                    else:
                        fh.write("\t" + key[0] +" " + key[1]  + ": " + str(stats['biword'][key])+ "\n")            
                pass
                fh.write("Word pairs (by frequency):\n")
                for (key),value in sort_dic_by_values(stats['biword']):
                    fh.write("\t" + key[0] +" " + key[1]  + ": " + str(stats['biword'][key])+ "\n")            
                pass
                fh.write("Symbol pairs (alphabetical order):\n")
                for (key) in sorted(stats['bisymbol']):
                    klist = list(key)
                    if "$" not in klist:
                        fh.write("\t" + str(klist[0]) +  str(klist[1])  + ": " + str(stats['bisymbol'][key]) + "\n")
                pass
                fh.write("Symbol pairs (by frequency):\n")
                for (key) in sort_dic_by_values(stats['bisymbol']):
                    klist = list(key[0])
                    if "$" not in klist:
                        fh.write("\t" + str(klist[0]) +  str(klist[1])  + ": " + str(key[1]) + "\n")
                pass
            
            else:
                i = 0
                for key in sorted(stats['word'].keys()):
                    fh.write("\t" + key + ": " + str(stats['word'][key]) + "\n")
                    i += 1
                    if i == 20:
                        break 
                pass

                fh.write("Words (by frequency):\n")
                i = 0
                for key,value in sort_dic_by_values(stats['word']):
                    fh.write("\t" + key + ": " + str(value) + "\n")
                    i += 1
                    if i == 20:
                        break    
                pass

                fh.write("Symbols (alphabetical order):\n")
                i = 0
                for key in sorted(stats['symbol'].keys()):
                    fh.write("\t" + key + ": " + str(stats['symbol'][key]) + "\n")
                    i += 1
                    if i == 20:
                        i = 0
                        break            
                pass

                fh.write("Symbols (by frequency):\n")
                for key, value in sort_dic_by_values(stats['symbol']):
                    fh.write("\t" + key + ": " + str(value) + "\n")
                    i += 1
                    if i == 20:
                        i = 0
                        break
                pass

                #Bigrams and bisymbols
                fh.write("Word pairs (alphabetical order):\n")
                for (key) in sorted(stats['biword']):
                    if key[0] =="$" and key[1] =="$":
                        pass
                    else:
                        fh.write("\t" + key[0] +" " + key[1]  + ": " + str(stats['biword'][key])+ "\n")
                        i += 1
                        if i == 20:
                            i = 0
                            break            
                pass

                fh.write("Word pairs (by frequency):\n")
                for (key),value in sort_dic_by_values(stats['biword']):
                    if (key[0] =="$" and key[1] =="$"):
                        pass
                    else:
                        fh.write("\t" + key[0] +" " + key[1]  + ": " + str(stats['biword'][key])+ "\n")
                        i += 1
                        if i == 20:
                            i = 0
                            break            
                pass

                fh.write("Symbol pairs (alphabetical order):\n")
                for (key) in sorted(stats['bisymbol']):
                    klist = list(key)
                    if "$" not in klist:
                        fh.write("\t" + str(klist[0]) +  str(klist[1])  + ": " + str(stats['bisymbol'][key]) + "\n")
                        i += 1
                        if i == 20:
                            i = 0
                            break
                pass
                fh.write("Symbol pairs (by frequency):\n")
                for (key) in sort_dic_by_values(stats['bisymbol']):
                    klist = list(key[0])
                    if "$" not in klist:
                        fh.write("\t" + str(klist[0]) +  str(klist[1])  + ": " + str(key[1]) + "\n")
                        i += 1
                        if i == 20:
                            i = 0
                            break
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

        sts = {
                'nwords': 0,
                'nlines': 0,
                'word': {},
                'symbol': {},
                }

        if bigrams:
            sts['biword'] = {}
            sts['bisymbol'] = {}

        words = {}
        symbols = {}
        bigrams_words = {}
        bigrams_symbols = {}
        
        bigrams_word = {}
        bigrams_list = {}

        io_file = open(filename)
        line_count = 0 
        words_count = 0
        words_in_stopwords = 0
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
                        bigrams_word = str('$') + word + str('$')
                        for i in range(len(bigrams_word) - 1):
                            w1, w2 = bigrams_word[i : i + 2]
                            bigrams_symbols[(w1,w2)] = bigrams_symbols.get((w1,w2), 0) + 1
                else:
                    words_in_stopwords += 1

            if bigrams:
                bigrams_list = '$ ' + " ".join(clean_line_list) + ' $'
                #bigrams_list = str('$')+ clean_line_list + str('$')
                bigrams_list = bigrams_list.split()
                
                for i in range(len(bigrams_list) - 1):  
                    (w1, w2) = bigrams_list[i : i + 2]
                    if w1 in stopwords:
                        pass
                    elif w2 in stopwords:
                        pass
                    else:
                        bigrams_words[(w1,w2)] = bigrams_words.get((w1,w2), 0) + 1
                

        sts['nlines'] = line_count
        sts['nwords'] = words_count
        sts['total_words'] = words_count + words_in_stopwords
        sts['nsymbols'] = symbols_count
        sts['word'] = words
        sts['symbol'] = symbols
        sts['biword'] = bigrams_words
        sts['bisymbol'] = bigrams_symbols
        sts['unique_words'] = len(words)
        sts['unique_symbols'] = len(symbols)

        #Output filename treatment
        new_filename = "" 
        s = filename.split('.')
        if len(s) > 1:
            new_filename = s[0] + '_stats' + '.' + s[1]
        else: 
            new_filename = s[0] + '_stats'
        
        if lower:
            s = new_filename.split('_')
            new_filename = s[0] + '_l_' + s[1]

        if stopwordsfile:
            s = new_filename.split('_')
            if len(s) > 2:
                new_filename = s[0] + '_'+ s[1] + 's_' + s[2]
            else:
                new_filename = s[0] + '_s_'+ s[1]

        if bigrams:
            s = new_filename.split('_')
            if len(s) > 2:
                new_filename = s[0] + '_'+ s[1] + 'b_' + s[2]
            else:
                new_filename = s[0] + '_b_'+ s[1]
        if full:
            s = new_filename.split('_')
            if len(s) > 2:
                new_filename = s[0] + '_'+ s[1] + 'f_' + s[2]
            else:
                new_filename = s[0] + '_f_'+ s[1]

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