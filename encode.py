import struct

def encode_file(k, file):
    with open(file, 'rb') as f:
        data = f.read()
        message_size = len(data)
        
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
                    if index + i > message_size:
                        break
                    concatenated_words += data[index + i].to_bytes(1, 'big')

            # codificar a palavra atual 
            try:
                compressed_data.append(dictionary[c_byte])
                index += len(c_byte)
            except Exception as e:
                print(f'{index} {e}')

            # adicionar conjunto de caracteres ao dicionário (se der errado é <= ao invés de <)
            if(key <= dictionary_max_size):
                key += 1
                dictionary[concatenated_words] = key
                try:
                    c_byte = concatenated_words[-1]
                except:
                    c_byte = next_byte

        with open(f'./outputs/{file}.bin', 'wb') as f_output:
            compressed_file.write(struct.pack('h'*len(self.compressed_message), *self.compressed_message))