import struct
from tqdm import tqdm

encoding = 'latin-1'

def write_file(decompressed_data, fileName):
    with open(f'./outputs/decompressed_{fileName[:-4]}', 'w', encoding=encoding) as f_output:
        f_output.write(decompressed_data)


def decode_file(file):

    with open(f'./outputs/{file}', 'rb') as f:
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

        for i in tqdm(range(1, len(compressed_data))):
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

        write_file(''.join(descompressed_text), file)

