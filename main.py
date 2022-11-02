import sys
from encode import encode_file
# from decode import decode_file

# main.py -enc/-dec -k=9 -i=input.txt

def parse_args(args):
    error = None
    output = {}
    try:
        # operação a ser realizada (encode ou decode)
        op = [opArg for opArg in argV if opArg == '-enc' or opArg == '-dec'][0]
        output['op'] = op

        try:
            # arquivo de input
            input_file = [inputFile for inputFile in argV if inputFile.startswith('-i=')][0][3:]
            output['input_file'] = input_file

            if op == '-enc':
                try:
                    # valor de K
                    K = int([kArg for kArg in argV if kArg.startswith('-k=')][0][3:])
                    if not (9 <= K <= 16):
                        error = 'K value must be between 9 and 16 (included).'
                        return [error, output]
                    else:
                        output['K'] = K
                        return [error, output]
                except:
                    error = 'This script requires a value to be specified with the -k= flag for enconding.'
                    return [error, output]
        except:
            error = 'Input file not found.'
            return [error, output]
        
    except:
        error = 'This script requires an operation to be specified. Use -enc or -dec'
        return [error, output]


if __name__ == '__main__':
    argV = sys.argv[1:]
    print(parse_args(argV))
    error, args = parse_args(argV)
    if error:
        print(f'[ERROR]: {error}')
        exit()
    else:
        if (args['op'] == '-enc'):
            encode_file(args['K'], args['input_file'])
        else:
            decode_file(args['input_file'])

    
