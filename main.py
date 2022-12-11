import re
import sys
import timeit
import time
from encode import encode_file
from decode import decode_file
#from util import patternrecognizer
from patternrecognizer import PatternRecognizer
from tqdm import tqdm
import base64
from json import dump
from pathlib import Path

# main.py -enc/-dec -k=9 -i=input.txt
class lzw():
    def parse_args(args):
        error = None
        output = {}
        try:
            # operação a ser realizada (encode ou decode)
            op = [opArg for opArg in args if opArg == '-enc' or opArg == '-dec' or opArg == '-train' or opArg == '-test'][0]
            output['op'] = op

            try:
                # arquivo de input
                input_file = [inputFile for inputFile in args if inputFile.startswith('-i=')][0][3:]
                output['input_file'] = input_file

                if op == '-enc':
                    try:
                        # valor de K
                        K = int([kArg for kArg in args if kArg.startswith('-k=')][0][3:])
                        if not (9 <= K <= 16):
                            error = 'K value must be between 9 and 16 (included).'
                            return [error, output]
                        else:
                            output['K'] = K
                            return [error, output]
                    except:
                        error = 'This script requires a value to be specified with the -k= flag for enconding.'
                        return [error, output]
                else:
                    return [error, output]
            except:
                error = 'Input file not found.'
                return [error, output]
            
        except:
            error = 'This script requires an operation to be specified. Use -enc or -dec'
            return [error, output]

    def pattern_recognizer(input_file, k=None):
        #Array com os k's de 9 a 16
        bits_number_list = [k] if k else list(range(9, 17))
        best_compressions_by_kbit = {}
        accuracy_rates = {}
        times_by_kbit = {}

        #percorre todos os k's
        for index, kbit in enumerate(bits_number_list):
            begin_time = timeit.default_timer()

            pr = PatternRecognizer(input_file, kbit)
        
            print(f'\nCREATING TRAINING DATASET...\nK={kbit}, Dictionary_size={pow(2,kbit)}')
            #treina para o k atual
            pr.train()

            best_compressions = {}

            print('_'*152)
            print('Testing files...\n')

            #validação 
            for file in tqdm(sorted(pr.test_data)):
                pr.file = file
                img = file.split('orl_faces\\')[1]
                correct_img = re.sub('\\\\', '_', img)
                best_compressions[correct_img] = pr.test()
           
            best_compressions_by_kbit[f'{kbit} kbits'] = best_compressions

            sum_of_correct_imgs = 0

            #calcula a quantidade de acertos por k comparando a qual rosto pertencia o arquivo original e qual dicionario foi utilizado na compressão
            for img, best_img in best_compressions_by_kbit[f'{kbit} kbits'].items():
                person_img = img.split('_')[0]
                person_dict = best_img.split('_')[0]
                
                if person_img == person_dict:
                    sum_of_correct_imgs += 1
            
            end_time = timeit.default_timer()

            times_by_kbit[kbit] = end_time - begin_time
            #calcula a accuracia para cada k
            accuracy_rates[f's{kbit}'] = sum_of_correct_imgs/40.0
        #armazena os resultados de cada k
        Path("results").mkdir(parents=True, exist_ok=True)
        with open('results/best_results.json', 'w') as best_results_json:
            dump(best_compressions_by_kbit, best_results_json, indent=2, separators=(',', ': '))
        with open('results/accuracies.json', 'w') as accuracy_json:
            dump(accuracy_rates, accuracy_json, indent=2, separators=(',', ': '))

    if __name__ == '__main__':
        argV = sys.argv[1:]
        print(parse_args(argV))
        error, args = parse_args(argV)
        if error:
            print(f'[ERROR]: {error}')
            exit()
        else:
            if (args['op'] == '-enc'):
                compress = encode_file(args['K'], args['input_file'])
                compress.encode_file()
            elif (args['op'] == '-dec'):
                descompress = decode_file(args['input_file'])
                descompress.decode_file()
            elif (args['op'] == '-train'):
                pattern_recognizer(args['input_file'])


    
