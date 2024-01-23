O dado é retornado na operação read para verificar sua corretude.

Código usado para teste:

317 1 00000000000000000000000010100101 W	Escreve um dado na cache
317 1 00000000011000000111000000000101 W	Escreve o dado da cache na memoria e
							atualiza a cache	
317 0 00000000011000000111000000000101 H	Lê o dado da cache
919 0 M						Não retorna nada porque as posições nas duas memórias estão zeradas
919 1 00000000000001111111111111100000 W	Escreve um dado na cache
919 1 00000011111110000000011111100000 W	Escreve o dado da cache na memória e
							atualiza a cache
919 0 00000011111110000000011111100000 H	Lê o dado da cache
919 1 00000000000000000000000000000000 W	Zera a posição da cache
919 0 00000000000001111111111111100000 M	Como esta posição está vazia na cache (M),
							retorna o dado da memória principal
523 1 00000000000000000000000000010010 W	
956 1 00000000000000101001111100000100 W	Escreve um dado na cache
956 1 00000111000110101001100100000100 W	Escreve o dado da cache na memória e
							atualiza a cache
956 0 00000111000110101001100100000100 H	Lê o dado da cache
956 1 00000000000000000000000000000000 W	Zera a posição da cache
956 0 00000000000000101001111100000100 M	Como esta posição está vazia na cache (M),
							retorna o dado da memória principal
956 1 00000000000000000000000000000000 W	Como a posição na cache já está zerada,
							agora zera a posição na memória principal
956 0 M						Não retorna nada porque as posições nas duas memórias estão zeradas
538 1 00000000000000111111100000000001 W	
1 1 00000000000111100001111100010101 W