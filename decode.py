import struct
from tqdm import tqdm

encoding = 'latin-1'

class decode_file():

    def __init__(self, file_dir=str):
        self.file_dir = file_dir
        self.dictionary_size = 256
        self.dictionary = dict([(x, x.to_bytes(1, 'big')) for x in range(self.dictionary_size)])
        self.compressed_data = []

    def open_file(self):
        with open(f'./outputs/{self.file_dir}', 'rb') as f:
            while True:
                rec = f.read(2)
                if len(rec) != 2:
                    break
                (data, ) = struct.unpack('>H', rec)
                self.compressed_data.append(data)

    def write_file(self, decompressed_data=list):
        name = self.file_dir.split('.bin')
        with open(f'./outputs/decompressed_{name[0]}', 'wb') as f_output:
            for data in decompressed_data:
                f_output.write(data)
        
    def decode_file(self):

        self.open_file()

        symbol = ""
        decompressed_data = []

        for code in tqdm(self.compressed_data, colour='#FFFFFF'):
            if code not in self.dictionary:
                self.dictionary[code] = (symbol + symbol[0]).encode(encoding)
            
            decompressed_data.append(self.dictionary[code])

            if(not(len(symbol) == 0)):
                self.dictionary[self.dictionary_size] = (symbol + \
                    self.dictionary[code].decode(encoding)[0]).encode(encoding)
                self.dictionary_size += 1

            symbol = self.dictionary[code].decode(encoding)
        
        self.write_file(decompressed_data)