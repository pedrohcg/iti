import struct
from tqdm import tqdm

encoding = 'latin-1'

def open_file(file):
    with open(file, 'rb') as f:
        compressed_data = []

        while True:
            rec = f.read(2)
            if len(rec) != 4:
                break
            (data, ) = struct.unpack('>H', rec)
            compressed_data.append(data)
        
        return compressed_data

def write_file(decompressed_data):
    with open(f'./outputs/result.txt', 'wb') as result:
        for data in decompressed_data:
            result.write(data)


def decode_file(file):
    #compressed_data = open_file(file)

    #concatenated_words = ""
    #decompressed_data = []
    #dictionary_size = 256
    #dictionary = dict([(x, f'{x}'.encode(encoding)) for x in range(dictionary_size)])

    #for code in tqdm(compressed_data, colour='#FFFFFF'):
    #    if not code in dictionary:
    #        dictionary[code] = (concatenated_words + concatenated_words[0]).encode(encoding)
        
    #    decompressed_data.append(dictionary[code])

    #    if not(len(compressed_data) == 0):
    #        dictionary[dictionary_size] = (concatenated_words + dictionary[code].decode(encoding)[0]).encode(encoding)
    #        dictionary_size += 1

    #    concatenated_words = dictionary[code].decode(encoding)

    #    write_file(decompressed_data)

    with open(file, 'rb') as f:
        compressed_data = []

        while True:
            rec = f.read(2)
            if len(rec) != 2:
                break
            (data, ) = struct.unpack('>H', rec)
            compressed_data.append(data)
    
        if len(compressed_data) - 1 < 1:
            print("Arquivo vazio")
            return

        #inicializar dicionário de decodificação
        dictionary = {f'{i}': (i.to_bytes(1, 'big')) for i in range(256)}
        descompressed_text, index = [], "256"

        first_letter = dictionary[str(compressed_data[0])]
        descompressed_text.append(first_letter.decode('latin-1'))

        dictionary[index] = first_letter
    
        for i in range(1, len(compressed_data)):
            code = str(compressed_data[i])
            decoded_symbol = dictionary[code].decode('latin-1')

            if len(decoded_symbol):
                symbol = decoded_symbol[0]
            else:
                symbol = decoded_symbol
        
            dictionary[index] = dictionary[index] + \
                symbol.encode('latin-1')
        

            index = str(int(index) + 1)

            dictionary[index] = dictionary[code]
        
            descompressed_text.append(dictionary[code].decode('latin-1'))
    
        return "".join(descompressed_text)

