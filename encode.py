import struct
from tqdm import tqdm

encoding = 'latin-1'

def open_file(file):
    try:
        with open(file, 'r', encoding=encoding) as f:
            data = f.read()
            return data
    except:
        print('[Error]: File not found')
        exit()

def write_file(compressed_data):
    with open('./outputs/compressed_result.bin', 'wb') as output:
        for data in compressed_data:
            output.write(struct.pack('>H', data))

def encode_file(k, file):

    data = open_file(file)
    dictionary = {i.to_bytes(1, 'big'): i for i in range(256)}
    dictionary_max_size = pow(2, k)
    key = 256
    concatenated_words = ""
    compressed_data = []

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

    write_file(compressed_data)
    
    


        # message_size = len(data)

        # if len(data) - 1 < 1:
        #     print("Arquivo vazio")
        #     return

        # # inicializar o dicionário
        # dictionary_max_size = pow(2, k)
        # dictionary = {(i.to_bytes(1, 'big')): i for i in range(256)}
        # compressed_data = []

        # key, index = 255, 0
        # c_byte = data[0].to_bytes(1, 'big')

        # while not index + 1 > message_size:
        #     try:
        #         next_byte = data[index + 1].to_bytes(1, 'big')
        #     except:
        #         next_byte = b''

        #     concatenated_words = data[index].to_bytes(1, 'big') + next_byte

        #     if concatenated_words in dictionary:
        #         # índice do próximo símbolo a ser concatenado
        #         i = 1
        #         while concatenated_words in dictionary:
        #             i += 1
        #             c_byte = concatenated_words
        #             #para o while se não tiver prox caractere
        #             if index + i > message_size:
        #                 break
        #             concatenated_words += data[index + i].to_bytes(1, 'big')

        #     # codificar a palavra atual 
        #     compressed_data.append(dictionary[c_byte])
        #     index += len(c_byte)          
        
        #     # adicionar conjunto de caracteres ao dicionário (se der errado é <= ao invés de <)
        #     if(key <= dictionary_max_size):
        #         key += 1
        #         dictionary[concatenated_words] = key
        #         try:
        #             c_byte = concatenated_words[-1:]
        #         except:
        #             c_byte = next_byte

        # with open(f'./outputs/compressed_result.bin', 'wb') as f_output:
        #     for i in compressed_data:
        #         try:
        #             f_output.write(struct.pack('>H', i))
        #         except:
        #             print(i)
        #             print(dictionary[i])