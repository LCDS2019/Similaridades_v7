from owlready2 import *
import pandas as pd
import pickle
import os
from os import walk
import shutil
###################################################################
# Encontrar arquivos no diretório de dados

def encontrar_arq():
    path = './data_in/'

    for path, diretorios, arquivos in walk(path) :
        for arq in arquivos:
            nome_arq=os.path.splitext(arq)[0]
            #print(nome_arq)

            if arq.endswith(".owl") or arq.endswith(".rdf"):
                onto = get_ontology(path+str(arq)).load()

                class root(Thing):
                    namespace = onto

                #Apresentação das classes
                classes=list(onto.classes())
                #print(classes)

                #print(nome_arq)
                #print('Quantidade de conceitos: '+str(len(classes)))
                #print('')

                x=[]
                s = 0
                for i in classes:
                    for l in range(len(onto.get_children_of(i))):
                        #print(i,i.is_a[0])
                        b = (i.is_a[0],i)
                        x.append(b)
                        s = s + 1
                        #print(s)

                s = 0
                for i in classes:
                    for l in range(len(onto.get_children_of(i))):
                        # print(i,'|',onto.get_children_of(i)[l])
                        b = (i, onto.get_children_of(i)[l])
                        x.append(b)
                        s = s + 1
                        #print(s)

                df = pd.DataFrame(x)
                df.columns = ['n1', 'n2']
                #print(df)
                df['prop'] = 'is-a'
                df = df.drop_duplicates()
                #print(df)

                df.to_csv('./data_in/'+nome_arq+'_adj.csv', index = False, sep='|')
                #print(df.head(3))

    #print('')
    #print('Import ok!')
    #print('************************************************')
    #print('')

    return()

###################################################################
# Menu de arquivos de avaliação

def encontrar_arq_avaliacao():
    path = './data_in/'

    for path, diretorios, arquivos in walk(path) :
        for arq in arquivos:
            if arq.startswith("avalia_conceitos"):
                base_avaliacao = os.path.splitext(arq)[0]
                #print(base_avaliacao)
    return()

###################################################################
# Menu de arquivos

def criar_menu_arq():
    path = './data_in/'

    arr = os.listdir(path)

    lista = [arq for arq in arr if
             (arq.endswith("_adj.csv"))]

    menu_list = []
    n = 0
    for i in lista:
        print(n, i)
        menu_list.append((n,i))
        n = n + 1

    dic=dict(menu_list)
    dic = sorted(dic.values())
    #print(dict(menu_list))
    return dic

###################################################################
# Menu de arquivos de avaliação

def criar_menu_arq_avaliacao():
    path = './data_in/'

    arr_avaliacao = os.listdir(path)

    lista = [arq for arq in arr_avaliacao if
             (arq.startswith("avalia_conceitos"))]

    menu_avalia_list = []
    n = 0
    for i in lista:
        print(n, i)
        menu_avalia_list.append((n,i))
        n = n + 1

    dic_avalia=dict(menu_avalia_list)
    #print(dict(menu_avalia_list))
    return dic_avalia

###################################################################
# Menu de arquivos
def carga_de_ontologia(base):
    print('')
    #print('./data_in/'+str(base))
    print('Layout do arquivo base: ontologia:')
    df=pd.read_csv('./data_in/'+str(base),decimal=".",delimiter='|')
    print(df.head(3))
    return df


def carga_de_avaliacao(avaliacao):
    print('')
    #print('./data_in/'+str(base))
    print('Layout do arquivo de avaliação')
    df_avaliacao=pd.read_csv('./data_in/'+str(avaliacao),decimal=".",delimiter=',')
    print(df_avaliacao.head(3))
    return df_avaliacao