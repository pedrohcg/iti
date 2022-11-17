import struct
import timeit
from tqdm import tqdm

encoding = 'latin-1'

def open_file(fileName):
    try:
        with open(f'./tests/{fileName}', 'r', encoding=encoding) as f:
            data = f.read()
            return data
    except:
        print('[Error]: File not found')
        exit()

def write_file(compressed_data, fileName):
    with open(f'./outputs/{fileName}.bin', 'wb') as output:
        for data in compressed_data:
            output.write(struct.pack('>H', data))

def encode_file(k, file):

    data = open_file(file)
    dictionary = {i.to_bytes(1, 'big'): i for i in range(256)}
    dictionary_max_size = pow(2, k)
    key = 256
    concatenated_words = ""
    compressed_data = []

    begin_time = timeit.default_timer()
    for character in tqdm(data, colour='#FFFFFF'):
        symbol = concatenated_words + character

        if symbol.encode(encoding) in dictionary:
            concatenated_words = symbol
        else:
            encoded_char = concatenated_words.encode(encoding)
            compressed_data.append(dictionary[encoded_char])

            if len(dictionary) < dictionary_max_size:
                dictionary[symbol.encode(encoding)] = key
                key += 1
            
            concatenated_words = character
    
    if concatenated_words.encode(encoding) in dictionary:
        compressed_data.append(dictionary[concatenated_words.encode(encoding)])

    end_time = timeit.default_timer()
    print(f'{len(compressed_data) - 1} indices in LZW compression')

    print(f'Compression time: {end_time - begin_time} seconds')
    write_file(compressed_data, file)
