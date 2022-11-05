import struct

def decode_file(file):
    with open(file, 'rb') as f:
        compressed_file = f.read()

        data = struct.unpack(
                'h'*(round(len(compressed_file)/2)), compressed_file)
       
        if len(data) - 1 < 1:
            print("Arquivo vazio")
            return

        #inicializar dicionário de decodificação
        dictionary = {f'{i}': (i.to_bytes(1, 'big')) for i in range(256)}
        descompressed_text, index = [], "256"

        first_letter = dictionary[str(data[0])]
        descompressed_text.append(first_letter.decode('latin-1'))

        dictionary[index] = first_letter
        
        for i in range(1, len(data)):
            code = str(data[i])
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
    
