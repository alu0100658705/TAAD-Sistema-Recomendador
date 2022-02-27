from copy import deepcopy
import sys
import re
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

pd.set_option("display.max_columns", None)

DICT_DOCS = []
COSINE_SIMILARITY = ''
DICT_DOCS_MASTER = ''
COSINE_SIMILARITY_MASTER = ''

#####################################
# TF-IDF: SKLEARN                   #
#####################################
def setup_tfidf(list_docs):
    count_vectorizer = CountVectorizer()
    count_X = count_vectorizer.fit_transform(list_docs)

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(list_docs)
    df_idf = pd.DataFrame(vectorizer.idf_, index=vectorizer.get_feature_names(),columns=["idf"]) # idf(t) = log[ (1+ N) / (1 + df(t)) ] + 1

    i = 0
    for doc in DICT_DOCS:
        for dict in doc.values():
            df_tf = pd.DataFrame(count_X[i].T.todense(), index=count_vectorizer.get_feature_names(),columns=["tf"]) # tf(i, j) = número de ocurrencias de i en j 
            df_tfidf = pd.DataFrame(X[i].T.todense(), index=vectorizer.get_feature_names(), columns=["tfidf"]) # resultado de tf*idf normalizado
            i += 1
            for key in dict.copy():
                if key in vectorizer.get_feature_names():
                    dict[key].append(df_tf.loc[key]['tf'])
                    dict[key].append(round(df_idf.loc[key]['idf'], 4))
                    dict[key].append(round(df_tfidf.loc[key]['tfidf'], 4))
                else:
                    del dict[key]

    cosine_sim(X, vectorizer)

def cosine_sim(X_, vectorizer_):
    global COSINE_SIMILARITY
    df = pd.DataFrame(X_.toarray(), columns=vectorizer_.get_feature_names())
    doc_names = [list(doc.keys())[0] for doc in DICT_DOCS]
    df.index = doc_names
    cosine_similarity_array = cosine_similarity(df)
    COSINE_SIMILARITY = pd.DataFrame(cosine_similarity_array, index=df.index, columns=df.index)

########################################
# TF-IDF: TRANSPARENCIAS DE CLASE      #
########################################
def setup_tfidf_master(list_docs):
    global COSINE_SIMILARITY_MASTER
    count_vectorizer = CountVectorizer()
    count_X = count_vectorizer.fit_transform(list_docs)
    tf = pd.DataFrame(count_X.toarray(), columns=count_vectorizer.get_feature_names())
    N = tf.shape[0]

    list_names = count_vectorizer.get_feature_names()
    index = [f'doc_{i+1}' for i in range(N)]
    df = pd.DataFrame(columns=list_names, index=index)

    i = 0
    for doc in DICT_DOCS_MASTER:
        for dict in doc.values():
            for key in dict.copy():
                if key in count_vectorizer.get_feature_names():
                    tf_value =tf.loc[i, key]/(tf.iloc[i, tf.columns!=key].max())
                    ni = len(tf.loc[tf[key] > 0])
                    idf_value  = np.log(N/ni)
                    tf_idf_value = tf_value * idf_value
                
                    df.loc[f'doc_{i+1}'][key] = tf_idf_value

                    dict[key].append(round(tf_value, 4))
                    dict[key].append(round(idf_value, 4))
                    dict[key].append(round(tf_idf_value, 4))
                else:
                    del dict[key]
        i += 1

    df = df.fillna(0)
    cosine_similarity_array = cosine_similarity(df)
    COSINE_SIMILARITY_MASTER = pd.DataFrame(cosine_similarity_array, index=df.index, columns=df.index)

#####################################
# ESCRIBIR RESULTADOS EN UN FICHERO #
#####################################
def write_file():
    with open('resultados.txt', 'w') as file:
        file.write("Resultados Sk-learn:\n")
        for doc in DICT_DOCS:
            for dict in doc.values():
                file.write(f'Documento: {list(doc.keys())[0]}\n')
                df_print = pd.DataFrame(data=dict, index=['Índice','TF', 'IDF', 'TF-IDF'])
                df_print_str = df_print.to_string(header=True, index=True)
                file.write(df_print_str)
                file.write("\n")
        file.write("Similitud del coseno entre cada documento:\n")
        df_cosine_str = COSINE_SIMILARITY.to_string()
        file.write(df_cosine_str)
        file.write("\n")
        file.write("\n")
        file.write("Resultados Clase:\n")
        for doc in DICT_DOCS_MASTER:
            for dict in doc.values():
                file.write(f'Documento: {list(doc.keys())[0]}\n')
                df_print = pd.DataFrame(data=dict, index=['Índice','TF', 'IDF', 'TF-IDF'])
                df_print_str = df_print.to_string(header=True, index=True)
                file.write(df_print_str)
                file.write("\n")
        file.write("Similitud del coseno entre cada documento:\n")
        df_cosine_str = COSINE_SIMILARITY_MASTER.to_string()
        file.write(df_cosine_str)

#############################
# IMPRIMIR LOS RESULTADOS   #
#############################
def menu_print():
    print("Opciones \n 1. Resultados: sklearn \n 2. Resultados: Asigantura \n 3. Salida a Fichero\n 4. Salir")
    opcion = input("Introduzca la opción: ")

    if opcion == '1':
        for doc in DICT_DOCS:
            for dict in doc.values():
                print(f'Documento: {list(doc.keys())[0]}')
                df_print = pd.DataFrame(data=dict, index=['Índice','TF', 'IDF', 'TF-IDF'])
                print(df_print)
                print("\n")
        print("Similitud del coseno entre cada documento:")
        print(COSINE_SIMILARITY)
        print("\n")
        menu_print()
    elif opcion == '2':
        for doc in DICT_DOCS_MASTER:
            for dict in doc.values():
                print(f'Documento: {list(doc.keys())[0]}')
                df_print = pd.DataFrame(data=dict, index=['Índice','TF', 'IDF', 'TF-IDF'])
                print(df_print)
                print("\n")
        print("Similitud del coseno entre cada documento:")
        print(COSINE_SIMILARITY_MASTER)
        print("\n")
        menu_print() 
    elif opcion == '3':
        write_file()
        print("\n")
        print("Generado archivo de salida.")
        menu_print()
    elif opcion == '4':
        print("Saliendo....")
    else:
        print("Opción no reconocida...\n")
        menu_print()

def read_file(doc):
    global DICT_DOCS
    global DICT_DOCS_MASTER
    with open(doc) as doc_file:
        lines = doc_file.readlines()

    clear_docs = [re.sub('^[0-9]+[.] ', '', line.rstrip()).replace('"', '').replace(".", "")
        .replace(",", "").replace("'", "").lower() for line in lines]
    for i in range(len(clear_docs)):
        name = f'doc_{i+1}'
        DICT_DOCS.append({name: {}})
        j = 1
        for w in clear_docs[i].split():
            if w in DICT_DOCS[i].get(name):
                DICT_DOCS[i].get(name)[w][0] += f' - {str(j)}'
            else:
                DICT_DOCS[i].get(name)[w] = [str(j)]
            j += 1
                
    DICT_DOCS_MASTER = deepcopy(DICT_DOCS)
    setup_tfidf(clear_docs)
    setup_tfidf_master(clear_docs)
    menu_print()
        
def main(argv):
    if len(argv) == 0:
        print("Error: No se ha especificado el fichero.\nusage: python recomender.py <documento.txt>")
        sys.exit()
    else:
        read_file(argv[0])

if __name__ == "__main__":
   main(sys.argv[1:])