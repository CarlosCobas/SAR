#!/usr/bin/env python
#! -*- encoding: utf8 -*-

# 1.- Pig Latin

import sys
import re


class Translator():

    def __init__(self, punt=None):
        """
        Constructor de la clase Translator

        :param punt(opcional): una cadena con los signos de puntuación
                                que se deben respetar
        :return: el objeto de tipo Translator
        """
        if punt is None:
            self.re = re.compile("(\w+)([.,;?!]*)")
        else:
            self.re = re.compile("(\w+)(["+punt+"]*)")

    def translate_word(self, word):
        """
        Este método recibe una palabra en inglés y la traduce a Pig Latin

        :param word: la palabra que se debe pasar a Pig Latin
        :return: la palabra traducida
        """

        rexp = re.compile("(\w+)([.,;?!]*)")

        new_word = ''

        m = rexp.match(word)
        gp = m.groups()

        parsedWord = gp[0]
        signs = gp[1]

        full_upper = word.isupper()
        first_upper = word[0].isupper() 
        
        parsedWord = parsedWord.lower()

        if parsedWord[0] not in '1234567890,;?!' :
            if parsedWord[0] in 'aeiouyAEIOUY':
                new_word = parsedWord + 'yay'
            else: 
                for letter in parsedWord:
                    if letter in 'aeiouyAEIOUY':
                        separated_word = parsedWord.split(letter, 1)
                        separated_word.reverse()

                        new_word = letter + "".join(separated_word) + "ay" 
                        break
        else :
            new_word = word
        

        if full_upper:
            new_word = new_word.upper()
        elif first_upper:
                first_upper_letter = new_word[0].upper()
                new_word = first_upper_letter + new_word[1:]

        return new_word + signs + " "

    def translate_sentence(self, sentence):
        """
        Este método recibe una frase en inglés y la traduce a Pig Latin

        :param sentence: la frase que se debe pasar a Pig Latin
        :return: la frase traducida
        """

        # sustituir
        line = sentence.split()
        new_sentence = ''

        for word in line:
            new_word = self.translate_word(word)
            new_sentence = new_sentence + new_word

        return new_sentence.strip()

    def translate_file(self, filename):
        """
        Este método recibe un fichero y crea otro con su tradución a Pig Latin

        :param filename: el nombre del fichero que se debe traducir
        :return: True / False 
        """
        fh = open(filename)

        new_file_name = ''
        
        s = filename.split('.')
        
        if len(s) > 1:
            new_file_name = s[0] + 'latin' + '.' + s[1]
        else: 
            new_file_name = s[0] + 'latin'
            
        newFh = open(new_file_name, 'w')

        for line in fh:
            newline = self.translate_sentence(line)
            newFh.write(newline + '\n')

        newFh.close()
        fh.close()

        

if __name__ == "__main__":
    if len(sys.argv) > 2:
        print('Syntax: python %s [filename]' % sys.argv[0])
        exit
    else:
        t = Translator()
        if len(sys.argv) == 2:
            t.translate_file(sys.argv[1])
        else:
            while True:
                sentence = input("ENGLISH: ")
                if len(sentence) < 2:
                    break
                print("PIG LATIN:", t.translate_sentence(sentence))
