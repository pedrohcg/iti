import struct

def encode_file(k, file):
    with open(file, 'rb') as f:
        data = f.read()
        message_size = len(data)-1

        if len(data) - 1 < 1:
            print("Arquivo vazio")
            return

        # inicializar o dicionário
        dictionary_max_size = pow(2, k)
        dictionary = {(i.to_bytes(1, 'big')): i for i in range(256)}
        compressed_data = []

        key, index = 255, 0
        c_byte = data[0].to_bytes(1, 'big')
        #print(dictionary)

        while not index + 1 > message_size + 1:
            try:
                next_byte = data[index + 1].to_bytes(1, 'big')
            except:
                next_byte = b''

            concatenated_words = data[index].to_bytes(1, 'big') + next_byte

            if concatenated_words in dictionary:
                # índice do próximo símbolo a ser concatenado
                i = 1
                while concatenated_words in dictionary:
                    i += 1
                    c_byte = concatenated_words
                    #para o while se não tiver prox caractere
                    if index + i > message_size:
                        break
                    concatenated_words += data[index + i].to_bytes(1, 'big')

            # codificar a palavra atual 
            compressed_data.append(dictionary[c_byte])
            index += len(c_byte)          
        
            # adicionar conjunto de caracteres ao dicionário (se der errado é <= ao invés de <)
            if(key <= dictionary_max_size):
                key += 1
                dictionary[concatenated_words] = key
                try:
                    c_byte = concatenated_words[-1:]
                except:
                    c_byte = next_byte
      
        with open(f'./outputs/compressed_result.bin', 'wb') as f_output:
            f_output.write(struct.pack('h'*len(compressed_data), *compressed_data))



