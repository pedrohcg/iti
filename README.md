# Projeto final de ITI - LZW

O projeto consiste em implementar um compressor e descompressor utilizando o algoritmo LZW
com possibilidade para arquivo de texto e arquivo binário de vídeo. As mensagens descomprimidas são
geradas por fontes com alfabeto A = {0, 1, ..., 255}.

## Requisitos

Este projeto foi todo implementado em Python 3.10.8, biblioteca necessária:

TQDM:

```
pip3 install tqdm
```

## Execução

Este projeto aceita como formato para a compressão txt e mp4. No diretório raiz do projeto:

- Compressão:

```
python3 main.py -enc -k="[9-16]" -i="nome_do_arquivo_para_comprimir"
```

- Decompressão:

```
python3 main.py -dec -i="nome_do_arquivo_para_descomprimir"
```
