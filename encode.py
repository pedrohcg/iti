import struct
import timeit
from tqdm import tqdm
from pathlib import Path

encoding = 'latin-1'

class encode_file():

    def __init__(self, k, file_dir=None, dict_cache=None, operation=None):
        self.file_dir = file_dir
        self.k = k
        self.max_size = pow(2, k)
        self.key = 256
        self.dict_cache = dict_cache
        self.operation = operation
        self.dictionary = dict_cache if dict_cache else {i.to_bytes(1, 'big'): i for i in range(256)}

    def open_file(self):
        try:
            with open(f'{self.file_dir}', 'r', encoding=encoding) as f:
                data = f.read()[14:] if self.operation == "train" else f.read()
                return data
        except:
            print('[Error]: File not found')
            exit()

    def write_file(self, compressed_data):
        
        with open(f'./outputs/{self.file_dir}.bin', 'wb') as output:
            for data in compressed_data:
                output.write(struct.pack('>H', data))

    def encode_file(self, color):
        data = self.open_file()
        concatenated_words = ""
        compressed_data = []

        begin_time = timeit.default_timer()

        progress_bar = False if not color else tqdm(data)

        for character in data:

            if progress_bar:
                progress_bar.update(1)

            symbol = concatenated_words + character

            if symbol.encode(encoding) in self.dictionary:
                concatenated_words = symbol
            else:
                encoded_chr = concatenated_words.encode(encoding)
                compressed_data.append(self.dictionary[encoded_chr])

                if(len(self.dictionary) <= self.max_size) and not self.dict_cache:
                    self.dictionary[symbol.encode(encoding)] = self.key
                    self.key += 1
                
                concatenated_words = character
        
        if concatenated_words.encode(encoding) in self.dictionary:
            compressed_data.append(self.dictionary[concatenated_words.encode(encoding)])
        
        end_time = timeit.default_timer()

        if(self.operation != "train"):
            self.write_file(compressed_data)

        #print(f'{len(compressed_data) - 1} indices in LZW compression')

        #print(f'Compression time: {end_time - begin_time} seconds')

        return compressed_data
    