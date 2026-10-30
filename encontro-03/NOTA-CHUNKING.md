# Nota de chunking · Equipe: BEEFIM

Caso: (x) Aurora  ( ) domínio próprio: ____________

## 1. O que adotamos

Estratégia de chunking: estrutura
Busca (vetor, BM25 ou híbrida): vetor
Tratamento de versões e de autoridade: considerando documentação vigentes e não oficiais
k (quantos trechos o agente recebe): 5

## 2. Por quê

| configuração | normal | excecao | conflito | termo-exato | autoridade | total |
|---|---|---|---|---|---|---|
| base: tamanho 400 · vetor | 7/7 (0) | 2/2 (1) | 2/3 (3) | 3/3 (1) | 1/1 (0) | 15/16 (5) |
| estrutura · vetor | 6/7 (0) | 2/2 (0) | 2/3 (3) | 3/3 (0) | 1/1 (0) | 14/16 (3) |
| estrutura · hibrida | 6/7 (0) | 2/2 (0) | 1/3 (3) | 3/3 (0) | 1/1 (0) | 13/16 (3) |
| estrutura · bm25 | 5/7 (0) | 2/2 (0) | 1/3 (3) | 3/3 (0) | 1/1 (0) | 12/16 (3) |
| estrutura - 400 - 0 - True - vetor - True - False | 6/7 (0) | 2/2 (0) | 3/3 (0) | 3/3 (0) | 1/1 (0) | 15/16 (0) |
| tamanho - 400 - 0 - True - vetor - True - False | 7/7 (0) | 2/2 (1) | 2/3 (0) | 3/3 (1) | 1/1 (0) | 15/16 (2) |
| tamanho - 400 - 0 - True - vetor - True - False - k = 5 | 7/7 (0) | 2/2 (1) | 3/3 (0) | 3/3 (1) | 1/1 (0) | 16/16 (2) |
| estrutura - 400 - 0 - True - vetor - True - False - k = 3 | 6/7 (0) | 2/2 (0) | 3/3 (0) | 3/3 (0) | 1/1 (0) | 15/16 (0) |
| estrutura - 400 - 0 - True - vetor - True - False - k = 5 | 7/7 (0) | 2/2 (0) | 3/3 (0) | 3/3 (0) | 1/1 (0) | 16/16 (0) |

A partir dos parâmetros adotados, foi possível obter 100% de acerto e zero de contaminações

## 3. O que ela não resolve

**Sem resposta (S1–S3).** Ex.: "A Aurora oferece previdência privada?" não tem
resposta na wiki, mas a busca devolve 5 trechos parecidos (similaridade ~0,86,
igual à de respostas certas). Nenhuma configuração de busca resolve. O agente é
quem precisa dizer "não sei" e encaminhar ao RH quando os trechos não respondem.

## 4. O que a ingestão precisa garantir

A ingestão precisa garantir que toda página tenha `politica`, `vigencia` e `autoridade`. O dono da página define a `politica` na criação, atualiza a `vigencia` a cada nova versão e marca a `autoridade` na publicação. Com algum desses campos errado, o agente pode responder com uma regra revogada, receber versões contraditórias ou tratar um FAQ informal como regra oficial, e por isso páginas sem esses campos devem ser rejeitadas.