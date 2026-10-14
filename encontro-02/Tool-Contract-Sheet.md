# Tool Contract Sheet · Equipe BEEFIM

**Encontro 2 · Entrega de 10%: esta planilha e o código** · Caso: Aurora Tecnologia

Uma linha por ferramenta do caso: as seis do hands-on e as que o ADR da equipe exigir. Equipe que trocou de domínio preenche com as ferramentas do próprio caso.

**A entrega é documento e código.** Cada linha descreve uma ferramenta que existe no fork da equipe, com contrato implementado. Linha sem código correspondente vai marcada como *planejada*.

---

## 1. Catálogo

**Antes de cada linha, respondam a coluna "Quem decide":** essa chamada precisa ser escolhida pelo modelo, ou pode ser um passo fixo do workflow? Toda linha com "Modelo" precisa justificar, na seção 2, por que o código não poderia decidir.

| Nome | Quem decide | Descrição | Entrada | Saída | Escopo | Criticidade | Reversível |
|---|---|---|---|---|---|---|---|
| `consultar_politica_rh` | Modelo | Busca nas políticas de RH da wiki (férias, trabalho remoto, licenças, jornada, guia de integração) | pergunta (texto, obrigatório, até 300), tema (enum, opcional) | id, titulo, atualizado_em, trecho | Qualquer colaborador; só páginas de RH da wiki | Baixa | Sim |
| `buscar_base_ti` | Modelo | Busca na base de conhecimento de TI antes de responder ou de abrir chamado | pergunta (texto, obrigatório, até 300) | id, titulo, atualizado_em, trecho | Qualquer colaborador; só páginas de TI da wiki | Baixa | Sim |
| `abrir_chamado_ti` | Modelo | Cria chamado quando o colaborador pede ou a base de TI indica; nunca duas vezes no mesmo atendimento | categoria (enum, obrigatório), descricao (texto, obrigatório, mínimo 15), urgencia (enum, opcional) | id, status, categoria, urgencia, prazo_atendimento, descricao | Colaborador autenticado; só o service desk de TI | Média | Com custo |
| `consultar_regra_beneficio` | Modelo | Devolve a página de regras de um benefício: valor, prazos, documentos | beneficio (enum, obrigatório), pergunta (texto, opcional, até 300) | id, titulo, atualizado_em, trecho | Qualquer colaborador; só páginas de benefícios da wiki | Baixa | Sim |
| `verificar_elegibilidade_beneficio` | Modelo | Lê o cadastro do colaborador e faz a pré-análise; não confirma direito, o caso segue para o RH | colaborador_id (texto, obrigatório), beneficio (enum, obrigatório) | colaborador_id, nome, regime, admissao, dependentes, beneficios_ativos, beneficio, pre_analise, criterios_verificados, aviso | Só o cadastro do próprio colaborador, com id informado por ele; CPF e salário não voltam ao modelo | Alta | Sim |
| `consultar_rede_credenciada` | Modelo | Lista até 5 prestadores ativos do plano de saúde em uma cidade | cidade (texto, obrigatório, até 60), tipo (enum, opcional), apenas_24h (booleano, opcional) | id, total_encontrados, aviso, prestador, tipo, especialidades, bairro, telefone, atende_24h | Qualquer colaborador; só prestadores ativos, sem valor negociado, observação interna nem código da operadora | Média | Sim |

**Como preencher cada coluna:**

- **Nome:** verbo + objeto, na linguagem do domínio.
- **Quem decide:** `Modelo` (o agente escolhe) ou `Código` (passo fixo do workflow).
- **Descrição:** resumida aqui. A versão completa vai na seção 3, com o **quando não usar**.
- **Entrada:** parâmetros, tipos e restrições (enum, obrigatório, limites).
- **Saída:** só os campos que voltam ao modelo.
- **Escopo:** quem pode chamar, em nome de quem, que dados alcança.
- **Criticidade:** Baixa, Média ou Alta. O que acontece se ela falhar ou for chamada errado?
- **Reversível:** `Sim` (nada muda no mundo), `Com custo` (desfaz, mas alguém já viu) ou `Não`.

## 2. Justificativas

Para cada ferramenta com **Quem decide = Modelo**: por que essa chamada depende do conteúdo da pergunta e não pode ser um passo fixo?

- `consultar_politica_rh`: a pergunta chega em texto livre e só o conteúdo dela diz se o assunto é RH, TI ou benefício, e qual tema de RH buscar.
- `buscar_base_ti`: mesma razão; palavras como "seguro", "ponto" e "trabalho remoto" aparecem em páginas de TI e de RH, então uma regra por palavra-chave erraria o contexto.
- `abrir_chamado_ti`: depende de o colaborador ter pedido um chamado e de a base de TI não resolver sozinha (c12 pergunta sobre chamado e não deve abrir nenhum). A categoria e a urgência também saem do relato.
- `consultar_regra_beneficio`: qual dos três benefícios consultar depende da pergunta.
- `verificar_elegibilidade_beneficio`: só faz sentido quando a pergunta é sobre a situação de uma pessoa e ela informou o id; para dúvida sobre a regra (c15) não deve ser chamada.
- `consultar_rede_credenciada`: cidade, tipo de prestador e necessidade de 24 horas vêm da pergunta.

## 3. Contratos completos

- `encontro-02/contratos.py`: `consultar_politica_rh`, `buscar_base_ti`, `abrir_chamado_ti`, `consultar_regra_beneficio`, `verificar_elegibilidade_beneficio`.
- `encontro-02/nova_ferramenta.py`: `consultar_rede_credenciada` (contrato e implementação).

## 4. Evidência do hands-on

**A quebra da dupla** (2 · Texto livre no lugar de enum):

| Versão | Acertos | Tool errada | Args inválidos | Chamados a mais | Dado sensível | Tokens/caso |
|---|---|---|---|---|---|---|
| Contrato da dupla | 11/17 | 0 | 0 | 0 | 0 | 8.189 |
| Quebra 2 | 10/17 | 3 | 16 | 0 | 0 | 10.799 |

CSV: `encontro-02/resultados/execucao_20261013_230250_q2.csv`

O acerto quase não mudou (11 → 10), mas o custo subiu: sem enum, o modelo passou `tema` (7 vezes), `beneficio` (6), `categoria` (2) e `urgencia` (1) em texto livre, o sistema recusou as 16 chamadas e cada recusa virou uma nova tentativa. Foram 32% mais tokens por caso, e o custo por acerto passou de US$ 0,0150 para US$ 0,0216. Olhando só para acertos, quase ninguém perceberia.

Essa rodada já é com o contrato final, depois dos ajustes descritos abaixo. Uma rodada anterior, com o contrato das 22:01 (`execucao_20261013_220142_q2.csv`), tinha dado 9 → 9 acertos, 15 args inválidos e 7.831 → 9.207 tokens por caso: o mesmo padrão.

**A ferramenta construída** (`consultar_rede_credenciada`): c16 falhou e c17 falhou na primeira versão. O que precisou mudar até passar: o contrato, não o filtro. Desde a primeira versão a ferramenta devolveu os prestadores certos e nenhum descredenciado; as falhas eram o modelo responder em texto livre, sem encerrar pela ferramenta `responder` e sem citar a fonte. Os dois casos passaram juntos depois de dois ajustes: o campo da fonte passou de `fonte` para `id`, igual às outras ferramentas, e a descrição passou a mandar encerrar pela ferramenta `responder` com esse id em fontes.

| Rodada (13/10) | Versão da ferramenta | c16 | c17 |
|---|---|---|---|
| 21:57 | Primeira versão | falhou | falhou |
| 21:58 | Primeira versão | passou | falhou |
| 22:01 | Primeira versão | falhou | falhou |
| 22:48 | Com `total_encontrados` e `aviso` de lista cortada | falhou | falhou |
| 22:50 | Campo `fonte` renomeado para `id` | passou | falhou |
| 22:54 | Descrição manda encerrar pela ferramenta `responder` | passou | passou |
| 23:02 | A mesma (rodada da quebra, coluna Contrato da dupla) | passou | passou |

CSV da primeira rodada em que os dois passaram: `encontro-02/resultados/execucao_20261013_225437_contrato.csv`. Cada linha da tabela é uma rodada só, sem repetições.

**O que isso mudou no nosso contrato:**

- Mantivemos enum em todo parâmetro que o sistema valida, porque é o que evita a tentativa recusada.
- `consultar_rede_credenciada` passou a devolver `total_encontrados` e um `aviso` quando a lista é cortada em 5, para o corte não ser invisível para o modelo (São Paulo tem 10 prestadores ativos).
- As seis descrições passaram a dizer como encerrar o atendimento: pela ferramenta `responder`, com o id em fontes, ou por `escalar_para_rh` no caso da elegibilidade.
- `verificar_elegibilidade_beneficio` ganhou o "quando não usar" e a instrução de encaminhar o caso ao RH em vez de afirmar o direito.
- A instrução de encerramento não resolveu tudo: na rodada das 23:02, c04, c09, c11 e c13 ainda terminaram em texto livre, e c11 e c13 falharam assim em todas as rodadas.
- Ficou identificado, sem correção ainda, que a descrição de `consultar_politica_rh` invade benefícios: na rodada das 22:01, no c15, o agente a chamou depois da regra do benefício e terminou em "não sei".

## 5. A ação irreversível do ADR

A ação irreversível definida no ADR do Encontro 1 é: confirmar a um colaborador que ele é elegível a um benefício (ou negar).

- Ela **não** é executada por nenhuma ferramenta do sistema, porque `verificar_elegibilidade_beneficio` faz só a pré-análise e o contrato manda encaminhar o caso ao RH, que é quem confirma (c14 termina em escalar).

> No Encontro 6, a coluna Reversível vira o eixo de impacto da matriz autonomia × impacto.
