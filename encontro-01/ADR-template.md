# Agent Decision Record — Grupo 6

**Caso:** [Dúvidas Internas do Colaborador, ou o domínio da equipe, se aprovado]
**Data:** [data] · **Integrantes:** [nomes]
**Status:** proposta

## 1. Contexto

A Aurora Tecnologia quer um assistente que responda dúvidas internas dos colaboradores sobre RH, TI e Benefícios, com base em 12 documentos de política interna (5 de RH, 4 de TI, 3 de Benefícios).
As respostas devem usar **somente** esses documentos e citar a fonte de cada informação.
Quando a informação não existe ou os documentos se contradizem, o assistente deve dizer que não sabe, em vez de escolher uma versão.
Perguntas sobre a elegibilidade do próprio colaborador a um benefício não podem ser respondidas pelo assistente: vão para análise do RH.
O volume é de perguntas curtas e frequentes, então custo por resposta e tempo de resposta importam tanto quanto o acerto.

**Ação irreversível do caso:** confirmar a um colaborador que ele é elegível a um benefício (ou negar). A resposta cria uma expectativa, ou leva a pessoa a abrir mão de um direito, que não se desfaz depois, mesmo que o RH corrija; por isso a elegibilidade é sempre escalada para análise humana.

## 2. Alternativas consideradas

Números do Hands-on 1 (mesmos 10 casos):

| Arquitetura | Acertos | Custo total | p50 | p95 | Custo por acerto | Variou entre execuções? |
|---|---|---|---|---|---|---|
| A · Prompt único | 9.0/10 | US$ 0.03941  | 1.98  s | 3.33 s | US$ 0.00438 | — |
| B · Workflow | 8.0/10 | US$ 0.01612 | 1.91 s | 2.52 s | US$ 0.00201 | — |
| C · Agente em loop | 9.0/10 | US$ 0.06321 | 3.95 s | 7.61 s | US$ 0.00702 | 0 de 10 casos |

**Onde cada uma errou, e por quê:** [2 a 4 linhas. Ex.: "B errou c07 porque o documento conflitante está em outro tema."]

c07: conflito entre documentos (as três erraram)

A pergunta é "Qual é o valor do vale-refeição por dia?". Dois documentos discordam:
- beneficios-vale-refeicao diz R$ 45,00;
- rh-guia-de-integracao diz R$ 42,00.

O certo era nao_sei, citando os dois. As três responderam "R$ 45,00", citando só o documento de benefícios, mas cada uma errou por um motivo diferente:

- A: tinha os 12 documentos no contexto, inclusive os dois em conflito, e mesmo assim não percebeu. O valor de R$ 42 aparece de passagem no meio do guia de integração, e o modelo ficou com o documento que trata do assunto e ignorou a regra 3 da política (conflito vira nao_sei). Ou seja, é um erro do modelo: a informação estava lá.
- B: o classificador mandou a pergunta para o tema beneficios, e a busca só olhou esse tema. O guia de integração é de RH, então o modelo nunca viu o R$ 42. É um erro da arquitetura: o workflow buscou num tema só.
- C: foram 2 chamadas ao modelo, uma busca e a resposta, e o agente não procurou mais. O CSV não guarda o tema que ele usou na busca, então não sei se foi beneficios ou todos. De qualquer forma, ele achou o documento de benefícios e parou: não tinha motivo para desconfiar de que existia outra versão em outro documento. Por isso errou nas 3 repetições.

c10: multi-passo (só o B errou)

A pergunta junta licença-paternidade (RH) e inclusão do bebê no plano de saúde (Benefícios).
- B: o classificador escolhe um tema, que foi RH. O workflow buscou só em RH e chegou a responder "essa informação não está nos documentos" sobre o plano de saúde. Faltou citar beneficios-plano-de-saude.
- A acertou porque tinha todos os documentos no contexto.
- C acertou porque o agente pode fazer mais de uma busca.

## 3. Decisão

Adotar a **Arquitetura A · Prompt único**: uma chamada ao modelo com todos os documentos no contexto.

**Escopo de autonomia:** o modelo só redige a resposta e escolhe o desfecho (`responder`, `escalar` ou `nao_sei`) com base nos documentos. Não executa ações nem decide elegibilidade: isso é sempre escalado ao RH.

**Critério de parada:** não se aplica. É sempre 1 chamada por pergunta, sem loop.

## 4. Trade-offs assumidos

- **Custo:** cerca de 2x mais caro por acerto que o workflow (US$ 0,0044 × US$ 0,0020), porque todos os documentos vão em toda pergunta.
- **Escala:** só funciona com corpus pequeno; com milhares de documentos fica inviável.
- **Explicabilidade:** não há registro de buscas ou passos, só a resposta com as fontes.
- **Risco:** conflitos entre documentos podem passar despercebidos (c07), erro que B e C também cometeram.

## 5. Critério de reversão

- Voltar para o **workflow (B)** se os tokens de entrada por pergunta passarem de 15.000 (hoje ~3.200) ou o custo por acerto passar de US$ 0,006 (hoje US$ 0,0044).
- Mudar para o **agente (C)** se ele superar o prompt único em 2 ou mais acertos a cada 10 casos de teste.
