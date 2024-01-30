# Organização de Computadores

Este projeto envolve a implementação de uma hierarquia de memória simples. A hierarquia consiste em uma CPU que executa operações de leitura e escrita em um subsistema de memória. Este subsistema é composto por uma memória cache pequena e uma memória de dados.

## Funcionamento
Leitura: A CPU envia um endereço para ser acessado na memória. Este endereço é repassado para a cache, que retorna o dado se um "hit" ocorrer, ou busca o bloco na memória de dados em caso de "miss".

Escrita: Recebe-se um endereço e um dado. Primeiro, atualiza-se o bloco correspondente na cache e marca-se como "sujo". Se for necessário substituir um bloco "sujo" na cache por um novo bloco, atualiza-se primeiro a memória de dados com os dados do bloco "sujo", e depois a cache com os dados do novo bloco.

## Especificações
- A memória de dados pode armazenar 1024 palavras de 32 bits.
- A cache pode armazenar 64 blocos, cada um contendo 16 bytes, ou seja, 4 palavras de 32 bits (128 bits no total).
- Utiliza-se Mapeamento Direto para alocar blocos na cache.
- Para operações de escrita, utiliza-se a técnica de Write Back.
- Os endereços fornecidos pela CPU têm 32 bits.

## Teste do Sistema
O programa deve ler um arquivo onde cada linha representa uma requisição da CPU, contendo:

- Endereço N para acesso à memória (0 <= N <= 2^12).
- Tipo da operação: 0 para leitura, 1 para escrita.
- Dado para operação de escrita: um dado de 32 bits.

Exemplo de arquivo de entrada:

5 1 00000000000000000000000000000101

5 0

12 1 00000000000000000000000000010010

25 0

## Saída do Programa

READS: 2

WRITES: 2

HITS: 1

MISSES: 1

HIT RATE: 0.5

MISS RATE: 0.5

5 1 00000000000000000000000000000101 W

5 0 H

12 1 00000000000000000000000000010010 W

25 0 M
