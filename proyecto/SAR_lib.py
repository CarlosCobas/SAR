import bisect
import json
from nltk.stem.snowball import SnowballStemmer
import os
import re


class SAR_Project:
    """
    Prototipo de la clase para realizar la indexacion y la recuperacion de noticias

        Preparada para todas las ampliaciones:
          parentesis + multiples indices + posicionales + stemming + permuterm + ranking de resultado

    Se deben completar los metodos que se indica.
    Se pueden añadir nuevas variables y nuevos metodos
    Los metodos que se añadan se deberan documentar en el codigo y explicar en la memoria
    """

    # lista de campos, el booleano indica si se debe tokenizar el campo
    # NECESARIO PARA LA AMPLIACION MULTIFIELD
    fields = [("title", True), ("date", False),
              ("keywords", True), ("article", True),
              ("summary", True)]

    # numero maximo de documento a mostrar cuando self.show_all es False
    SHOW_MAX = 10

    def __init__(self):
        """
        Constructor de la classe SAR_Indexer.
        NECESARIO PARA LA VERSION MINIMA

        Incluye todas las variables necesaria para todas las ampliaciones.
        Puedes añadir más variables si las necesitas

        """
        self.index = {}  # hash para el indice invertido de terminos --> clave: termino, valor: posting list.
        # Si se hace la implementacion multifield, se pude hacer un segundo nivel de hashing de tal forma que:
        # self.index['title'] seria el indice invertido del campo 'title'.
        self.sindex = {}  # hash para el indice invertido de stems --> clave: stem, valor: lista con los terminos que tienen ese stem
        self.ptindex = {}  # hash para el indice permuterm.
        self.docs = {}  # diccionario de terminos --> clave: entero(docid),  valor: ruta del fichero.
        self.weight = {}  # hash de terminos para el pesado, ranking de resultados. puede no utilizarse
        self.news = {}  # hash de noticias --> clave: entero (newid), valor: la info necesaria para diferencia la noticia dentro de su fichero
        self.tokenizer = re.compile("\W+")  # expresion regular para hacer la tokenizacion
        self.stemmer = SnowballStemmer('spanish')  # stemmer en castellano
        self.show_all = False  # valor por defecto, se cambia con self.set_showall()
        self.show_snippet = False  # valor por defecto, se cambia con self.set_snippet()
        self.use_stemming = False  # valor por defecto, se cambia con self.set_stemming()
        self.use_ranking = False  # valor por defecto, se cambia con self.set_ranking()

        self.doc_id = 0
        self.new_id = 0

    ###############################
    ###                         ###
    ###      CONFIGURACION      ###
    ###                         ###
    ###############################

    def set_showall(self, v):
        """

        Cambia el modo de mostrar los resultados.

        input: "v" booleano.

        UTIL PARA TODAS LAS VERSIONES

        si self.show_all es True se mostraran todos los resultados el lugar de un maximo de self.SHOW_MAX, no aplicable a la opcion -C

        """
        self.show_all = v

    def set_snippet(self, v):
        """

        Cambia el modo de mostrar snippet.

        input: "v" booleano.

        UTIL PARA TODAS LAS VERSIONES

        si self.show_snippet es True se mostrara un snippet de cada noticia, no aplicable a la opcion -C

        """
        self.show_snippet = v

    def set_stemming(self, v):
        """

        Cambia el modo de stemming por defecto.

        input: "v" booleano.

        UTIL PARA LA VERSION CON STEMMING

        si self.use_stemming es True las consultas se resolveran aplicando stemming por defecto.

        """
        self.use_stemming = v

    def set_ranking(self, v):
        """

        Cambia el modo de ranking por defecto.

        input: "v" booleano.

        UTIL PARA LA VERSION CON RANKING DE NOTICIAS

        si self.use_ranking es True las consultas se mostraran ordenadas, no aplicable a la opcion -C

        """
        self.use_ranking = v

    ###############################
    ###                         ###
    ###   PARTE 1: INDEXACION   ###
    ###                         ###
    ###############################

    def index_dir(self, root, **args):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Recorre recursivamente el directorio "root" e indexa su contenido
        los argumentos adicionales "**args" solo son necesarios para las funcionalidades ampliadas

        """

        self.multifield = args['multifield']
        self.positional = args['positional']
        self.stemming = args['stem']
        self.permuterm = args['permuterm']

        for dir, subdirs, files in os.walk(root):
            for filename in files:
                if filename.endswith('.json'):
                    fullname = os.path.join(dir, filename)

                    self.index_file(fullname)

        ##########################################
        ## COMPLETAR PARA FUNCIONALIDADES EXTRA ##
        ##########################################

    def index_file(self, filename):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Indexa el contenido de un fichero.

        Para tokenizar la noticia se debe llamar a "self.tokenize"

        Dependiendo del valor de "self.multifield" y "self.positional" se debe ampliar el indexado.
        En estos casos, se recomienda crear nuevos metodos para hacer mas sencilla la implementacion

        input: "filename" es el nombre de un fichero en formato JSON Arrays (https://www.w3schools.com/js/js_json_arrays.asp).
                Una vez parseado con json.load tendremos una lista de diccionarios, cada diccionario se corresponde a una noticia

        """

        with open(filename) as fh:
            news_list = json.load(fh)

        #
        # "news_list" es una lista con tantos elementos como noticias hay en el fichero,
        # cada noticia es un diccionario con los campos:
        #      "title", "date", "keywords", "article", "summary"
        #
        # En la version basica solo se debe indexar el contenido "article"
        #
        #
        #

        new_pos = 0

        for new in news_list:
            self.news[self.new_id] = (self.doc_id, new_pos)

            if self.multifield:
                for field, tokenize in SAR_Project.fields:
                    content = new[field]

                    if tokenize:
                        content = self.tokenize(content)

                        term_pos = 0

                        for term in content:
                            self.index_term(term, self.new_id, term_pos, field)

                            term_pos += 1

                    else:
                        self.index_term(content, self.new_id, 0, field)

            else:
                content = self.tokenize(new['article'])

                for term in content:
                    term_pos = 0

                    self.index_term(term, self.new_id, term_pos)

                    term_pos += 1

            self.new_id += 1

    def index_term(self, term, new_id, pos, field=None):
        index = self.index if field is None else self.index[field]

        news_dic = index.get(term, None)

        if news_dic is None:
            index[term] = {new_id: [pos]}

        else:
            if new_id in news_dic.keys():
                news_dic[new_id].append(pos)

            else:
                news_dic[new_id] = [pos]

            index[term] = news_dic

    def tokenize(self, text):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Tokeniza la cadena "texto" eliminando simbolos no alfanumericos y dividientola por espacios.
        Puedes utilizar la expresion regular 'self.tokenizer'.

        params: 'text': texto a tokenizar

        return: lista de tokens

        """
        return self.tokenizer.sub(' ', text.lower()).split()

    def make_stemming(self):  # TODO: Check if it works
        """
        NECESARIO PARA LA AMPLIACION DE STEMMING.

        Crea el indice de stemming (self.sindex) para los terminos de todos los indices.

        self.stemmer.stem(token) devuelve el stem del token

        """
        if self.multifield:
            for field in [f for f, t in SAR_Project.fields if t is True]:
                self.sindex[field] = {}

                inv_index = self.index[field]

                for term, _ in inv_index:
                    stem = self.stemmer.stem(term)

                    if stem not in self.sindex[field]:
                        self.sindex[field][stem] = []

                    else:
                        self.sindex[field][stem].append(term)

        else:
            self.sindex = {}

            for term, _ in self.index:
                stem = self.stemmer.stem(term)

                if stem not in self.sindex:
                    self.sindex[stem] = []

                else:
                    self.sindex[stem].append(term)

    def make_permuterm(self):  # TODO: Check if it works
        """
        NECESARIO PARA LA AMPLIACION DE PERMUTERM

        Crea el indice permuterm (self.ptindex) para los terminos de todos los indices.

        """
        if self.multifield:
            self.ptindex = {}

            for field in [f for f, t in SAR_Project.fields if t is True]:
                self.ptindex[field] = []

                inv_index = self.index[field]

                for term, _ in inv_index:
                    permuterms = self.get_permuterm(term)

                    for p in permuterms:
                        bisect.insort_left(self.ptindex[field], p)

        else:
            self.ptindex = []

            for term, _ in self.index:
                permuterms = self.get_permuterm(term)

                for p in permuterms:
                    bisect.insort_left(self.ptindex, p)

    def get_permuterm(self, term):
        term += '$'

        return [term[i:] + term[:i] for i in range(len(term))]

    def show_stats(self):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Muestra estadisticas de los indices

        """
        pass
        ########################################
        ## COMPLETAR PARA TODAS LAS VERSIONES ##
        ########################################

    ###################################
    ###                             ###
    ###   PARTE 2.1: RECUPERACION   ###
    ###                             ###
    ###################################

    def solve_query(self, query, prev={}):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Resuelve una query.
        Debe realizar el parsing de consulta que sera mas o menos complicado en funcion de la ampliacion que se implementen


        param:  "query": cadena con la query
                "prev": incluido por si se quiere hacer una version recursiva. No es necesario utilizarlo.


        return: posting list con el resultado de la query

        """

        if query is None or len(query) == 0:
            return []

        connections = ['AND', 'OR', 'NOT']
        query_as_list = query.split()
        postings_query_terms = {}

        # One word query
        if len(query_as_list) == 1 and query_as_list[0] not in connections:
            return self.get_posting(query_as_list[0])
        
        term_pos = 0
        for term in query_as_list:
            if term not in connections:
                pl = self.get_posting(term)
                postings_query_terms[term_pos] = pl

            term_pos += 1

        x = 0

        working_res = []

        while x < len(query_as_list) - 1:

            if query_as_list[x] == 'NOT':
                postings_query_terms[x+1] = self.reverse_posting(postings_query_terms.get(x+1))

            elif query_as_list[x] == 'AND':
                prev_term_posting = postings_query_terms.get(x-1)

                if query_as_list[x+1] == 'NOT':
                    second_term_posting = self.reverse_posting(postings_query_terms.get(x+2))
                    postings_query_terms[x+2] = self.and_posting(prev_term_posting, second_term_posting)
                    x += 1  # Avanzo para no repetir el NOT

                else:
                    postings_query_terms[x+1] = self.and_posting(prev_term_posting, postings_query_terms.get(x+1))

            elif query_as_list[x] == 'OR':
                prev_term_posting = postings_query_terms.get(x-1)

                if query_as_list[x+1] == 'NOT':
                    second_term_posting = self.reverse_posting(postings_query_terms.get(x+2))
                    postings_query_terms[x+2] = self.or_posting(prev_term_posting, second_term_posting)
                    x += 1  # Avanzo para no repetir el NOT

                else:
                    postings_query_terms[x+1] = self.or_posting(prev_term_posting, postings_query_terms.get(x+1))

            x += 1

        return postings_query_terms[len(query_as_list) - 1]

    def get_posting(self, term, field='article'):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Devuelve la posting list asociada a un termino.
        Dependiendo de las ampliaciones implementadas "get_posting" puede llamar a:
            - self.get_positionals: para la ampliacion de posicionales
            - self.get_permuterm: para la ampliacion de permuterms
            - self.get_stemming: para la amplaicion de stemming


        param:  "term": termino del que se debe recuperar la posting list.
                "field": campo sobre el que se debe recuperar la posting list, solo necesario se se hace la ampliacion de multiples indices

        return: posting list

        """
        res = list(self.index.get(term).keys())

        return res

    def get_positionals(self, terms, field='article'):
        """
        NECESARIO PARA LA AMPLIACION DE POSICIONALES

        Devuelve la posting list asociada a una secuencia de terminos consecutivos.

        param:  "terms": lista con los terminos consecutivos para recuperar la posting list.
                "field": campo sobre el que se debe recuperar la posting list, solo necesario se se hace la ampliacion de multiples indices

        return: posting list

        """
        pass
        ########################################################
        ## COMPLETAR PARA FUNCIONALIDAD EXTRA DE POSICIONALES ##
        ########################################################

    def get_stemming(self, term, field='article'):
        """
        NECESARIO PARA LA AMPLIACION DE STEMMING

        Devuelve la posting list asociada al stem de un termino.

        param:  "term": termino para recuperar la posting list de su stem.
                "field": campo sobre el que se debe recuperar la posting list, solo necesario se se hace la ampliacion de multiples indices

        return: posting list

        """

        stem = self.stemmer.stem(term)

        ####################################################
        ## COMPLETAR PARA FUNCIONALIDAD EXTRA DE STEMMING ##
        ####################################################

    def get_permuterm(self, term, field='article'):
        """
        NECESARIO PARA LA AMPLIACION DE PERMUTERM

        Devuelve la posting list asociada a un termino utilizando el indice permuterm.

        param:  "term": termino para recuperar la posting list, "term" incluye un comodin (* o ?).
                "field": campo sobre el que se debe recuperar la posting list, solo necesario se se hace la ampliacion de multiples indices

        return: posting list

        """

        ##################################################
        ## COMPLETAR PARA FUNCIONALIDAD EXTRA PERMUTERM ##
        ##################################################

    def reverse_posting(self, p):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Devuelve una posting list con todas las noticias excepto las contenidas en p.
        Util para resolver las queries con NOT.


        param:  "p": posting list


        return: posting list con todos los newid exceptos los contenidos en p

        """

        full_list = list(self.news.keys())
        res = []
        x = y = 0
        
        while x < len(full_list) and y < len(p):
            if full_list[x] == p[y]:
                x = x + 1
                y = y + 1

            else:
                res.append(full_list[x])
                x = x + 1

        while x < len(full_list):
            res.append(full_list[x])
            x = x + 1
        
        return res

    def and_posting(self, p1, p2):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Calcula el AND de dos posting list de forma EFICIENTE

        param:  "p1", "p2": posting lists sobre las que calcular


        return: posting list con los newid incluidos en p1 y p2

        """
        if len(p1) == 0 or len(p2) == 0:
            return []
        
        res = []
        x = y = 0

        while x < len(p1) and y < len(p2):
            if p1[x] == p2[y]:
                res.append(p1[x])
                x = x + 1
                y = y + 1

            else:
                if p1[x] < p2[y]:
                    x = x + 1

                else:
                    y = y + 1

        return res

    def or_posting(self, p1, p2):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Calcula el OR de dos posting list de forma EFICIENTE

        param:  "p1", "p2": posting lists sobre las que calcular


        return: posting list con los newid incluidos de p1 o p2

        """

        if len(p1) == 0 and len(p2) == 0:
            return []
        
        res = []
        x = y = 0

        while x < len(p1) and y < len(p2):
            if p1[x] == p2[y]:
                res.append(p1[x])
                x += 1
                y += 1

            else:
                if p1[x] > p2[y]:
                    res.append(p2[y])
                    y += 1

                else:
                    res.append(p1[x])
                    x += 1

        while x < len(p1):
            res.append(p1[x])
            x += 1
        
        while y < len(p2):
            res.append(p2[y])
            y += 1

        return res

    # TODO: revisar porque falla cuando lo uso (El and not queria hacerlo con este metodo pero falla)
    def minus_posting(self, p1, p2):
        """
        OPCIONAL PARA TODAS LAS VERSIONES

        Calcula el except de dos posting list de forma EFICIENTE.
        Esta funcion se propone por si os es util, no es necesario utilizarla.

        param:  "p1", "p2": posting lists sobre las que calcular


        return: posting list con los newid incluidos de p1 y no en p2

        """ 
        if len(p1) == 0:
            return []

        res = []
        x = y = 0

        while x < len(p1) and y < len(p2):
            if p1[x] == p2[y]:
                x += 1
                y += 1

            else:
                res.append(p1[x])
                x += 1

        while x < len(p1):
            res.append(p1[x])
            x += 1
        
        return res

    #####################################
    ###                               ###
    ### PARTE 2.2: MOSTRAR RESULTADOS ###
    ###                               ###
    #####################################

    def solve_and_count(self, query):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Resuelve una consulta y la muestra junto al numero de resultados

        param:  "query": query que se debe resolver.

        return: el numero de noticias recuperadas, para la opcion -T

        """
        result = self.solve_query(query)
        print("%s\t%d" % (query, len(result)))
        return len(result)  # para verificar los resultados (op: -T)

    def solve_and_show(self, query):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Resuelve una consulta y la muestra informacion de las noticias recuperadas.
        Consideraciones:

        - En funcion del valor de "self.show_snippet" se mostrara una informacion u otra.
        - Si se implementa la opcion de ranking y en funcion del valor de self.use_ranking debera llamar a self.rank_result

        param:  "query": query que se debe resolver.

        return: el numero de noticias recuperadas, para la opcion -T

        """
        result = self.solve_query(query)

        if self.use_ranking:
            result = self.rank_result(result, query)

        ########################################
        ## COMPLETAR PARA TODAS LAS VERSIONES ##
        ########################################

    def rank_result(self, result, query):
        """
        NECESARIO PARA LA AMPLIACION DE RANKING

        Ordena los resultados de una query.

        param:  "result": lista de resultados sin ordenar
                "query": query, puede ser la query original, la query procesada o una lista de terminos


        return: la lista de resultados ordenada

        """

        pass

        ###################################################
        ## COMPLETAR PARA FUNCIONALIDAD EXTRA DE RANKING ##
        ###################################################