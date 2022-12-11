import os
import re
import pickle

from tqdm import tqdm
from encode import encode_file
import random

import sys

class PatternRecognizer():

    def __init__(self, file, k=None, dict_cache=None):
        self.dict_cache_dir = './dict_cache'
        self.file = file
        self.lzwcompress = encode_file
        self.train_dictionary = dict()
        self.k = k
        self.test_data = []

    def train(self, train_split=90):
        #percorre todos as 40 pastas do dataset
        for path, _, files in tqdm(list(os.walk(self.file))[1:], colour='#FFFFFF'):
            #Comprime com o k atual e sem ler o cabeçalho da imagem
            compress = self.lzwcompress(self.k, operation="train")
            
            #determina os arquivos de teste aleatoriamente
            split_points = round(len(files)-(len(files)*(train_split/100)))
            tests_files = random.sample(files, split_points)
            
            #os arquivos que não foram escolhidos para teste são usados para treinar
            self.test_data.extend([os.path.join(path, file) for file in tests_files])
            training_data = list(set(files) - set(tests_files))
            
            #comprime os arquivos de treino
            for file in training_data:
                compress.file_dir = os.path.join(path, file)
                compress.encode_file(color=False)
            
            splited_path = path.split('orl_faces\\')[1]
            dict_cache_name = f'{splited_path}_{self.k}'

            #cria o cache
            with open(f'dict_cache\\{dict_cache_name}', 'wb') as dict_cache:
                pickle.dump(compress.dictionary, dict_cache)

            self.train_dictionary[dict_cache_name] = compress.dictionary

        return self.test_data

    def test(self):  
        best_compressed_data_len = sys.maxsize
        #percorre todos as 40 pastas
        for label, bytes_dict in self.train_dictionary.items():
            #armazenar k do dicionario
            self.kbit = int(label.split('_')[1])
            
            #comprime o arquivo de teste com todos os dicinarios em cache do mesmo k que o atual
            compress = self.lzwcompress(self.kbit, self.file, bytes_dict)
            compressed_data = compress.encode_file(color=False)

            #verifica qual pasta teve a melhor compressao de arquivo e salva ela como a melhor
            if len(compressed_data) < best_compressed_data_len:
                best_settings = label
                best_compression = compressed_data
                best_compressed_data_len = len(best_compression)

        
        compress.write_file(best_compression)

        #retorna a label do dicionario que teve o melhor resultado na compressão
        return best_settings    