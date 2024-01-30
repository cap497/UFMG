# Organização de Computadores

## Hierarquia de Memória

Este trabalho envolve a criação de uma hierarquia de memória que inclui uma CPU, uma memória cache e uma memória de dados. A CPU realiza operações de leitura e escrita:

- Leitura: A CPU envia um endereço à cache. Se o dado estiver na cache (hit), ele é retornado. Caso contrário (miss), o dado é buscado na memória de dados.
- Escrita: A CPU fornece um endereço e um dado. O dado é atualizado na cache e marcado como "sujo". Se um bloco sujo precisa ser substituído na cache, os dados são primeiro escritos na memória de dados antes de atualizar a cache com o novo bloco.
