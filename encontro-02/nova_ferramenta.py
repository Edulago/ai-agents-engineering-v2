"""TODO 4 — Construir do zero: consultar_rede_credenciada.     (CONTRATO E IMPLEMENTAÇÃO)

Nas ferramentas 1 a 5, a implementação veio pronta e vocês escreveram o contrato.
Aqui não tem nada pronto: vocês escrevem as duas coisas.

O pedido do time de Benefícios
------------------------------
"Todo dia alguém pergunta se tal hospital ou laboratório atende pelo plano. A resposta
está na nossa planilha da rede credenciada, no Google Sheets. Queremos que o assistente
consulte a planilha."

O sistema: a planilha
---------------------
    SHEETS.ler("planilha-rede-credenciada", "prestadores")

devolve o mesmo formato da API do Google Sheets (spreadsheets.values.get):

    {"spreadsheetId": "planilha-rede-credenciada",
     "range": "prestadores!A1:L31",
     "majorDimension": "ROWS",
     "values": [
        ["prestador", "tipo", "especialidades", "cidade", "uf", "bairro", "telefone",
         "atende_24h", "situacao", "codigo_operadora", "valor_negociado_consulta",
         "observacao_interna"],                                            <- cabeçalho
        ["Hospital Jacarandá Paulista", "Hospital", "clínica geral; ...", "São Paulo", ...],
        ...
     ]}

Tudo vem como texto, e a planilha é mantida à mão desde 2021. Olhem os dados antes
de escrever qualquer linha:

    python encontro-02/nova_ferramenta.py          (a partir da raiz: imprime a planilha inteira)

Passo a passo
-------------
  4a. IMPLEMENTAÇÃO: escrevam consultar_rede_credenciada(). Decidam os parâmetros.
      Devolvam um dicionário com a lista de prestadores em "resultados" (um dicionário
      por prestador). Chaves fora de "resultados" também podem voltar ao modelo,
      se o contrato declarar (ex.: a fonte).
  4b. CONTRATO: preencham CONTRATO (descrição, schema, saída), como nos TODOs 1 a 3.
      Os parâmetros do schema precisam bater com os da função.
  4c. TESTE: assim que CONTRATO["parametros"] deixar de ser None, a ferramenta entra
      no catálogo do agente sozinha. Os casos c16 e c17 dependem dela:

          python encontro-02/rodar.py --casos c16 c17 --detalhe

Perguntas para decidir
----------------------
  - Que parâmetros o modelo precisa para chegar ao prestador certo? Quais valores aceitar?
  - "Campinas", "campinas" e "CAMPINAS " são a mesma cidade. Quem resolve isso: o modelo
    ou o código?
  - A planilha tem prestadores descredenciados e em negociação. O modelo deveria vê-los?
  - São Paulo tem mais de dez prestadores. Quantos voltam para o contexto?
  - Quais colunas nunca deveriam entrar no contexto? (O placar tem uma coluna para isso.)
  - Como o agente cita a planilha como fonte?
  - E erros: cidade sem prestador? Tipo que não existe?
"""
import unicodedata

from ferramentas import ErroDeFerramenta   # para devolver erros legíveis ao modelo (veja ferramentas.py)
from sistemas import PlanilhaGoogle

SHEETS = PlanilhaGoogle()
PLANILHA_ID = "planilha-rede-credenciada"
ABA = "prestadores"


def normalizar(texto: str) -> str:
    """'  São Paulo ' -> 'sao paulo'. Minúsculas, sem acento, sem espaço nas pontas."""
    sem_acento = unicodedata.normalize("NFKD", str(texto)).encode("ascii", "ignore").decode()
    return " ".join(sem_acento.lower().split())


# ======================================================================
# TODO 4a — a implementação
#
# Troquem a assinatura pelos parâmetros que vocês decidirem (com tipos e valores
# padrão) e escrevam o corpo. Esqueleto sugerido:
#   1. ler a planilha com SHEETS.ler(PLANILHA_ID, ABA)
#   2. transformar cada linha num dicionário (cabeçalho -> valor)
#   3. filtrar (normalizar() ajuda)
#   4. devolver {"resultados": [...], ...}
# ======================================================================
MAX_RESULTADOS = 5


def consultar_rede_credenciada(cidade: str, tipo: str | None = None, apenas_24h: bool = False) -> dict:
    cabecalho, *linhas = SHEETS.ler(PLANILHA_ID, ABA)["values"]
    prestadores = [dict(zip(cabecalho, linha)) for linha in linhas]

    resultados = []
    for p in prestadores:
        if normalizar(p["situacao"]) != "ativo":   # descredenciado e em negociação não saem daqui
            continue
        if normalizar(p["cidade"]) != normalizar(cidade):
            continue
        if tipo and normalizar(p["tipo"]) != normalizar(tipo):
            continue
        atende_24h = normalizar(p["atende_24h"]) == "sim"
        if apenas_24h and not atende_24h:
            continue
        # só o que o colaborador pode ver: valor negociado, observação interna e código ficam de fora
        resultados.append({
            "prestador": p["prestador"],
            "tipo": p["tipo"],
            "especialidades": p["especialidades"],
            "bairro": p["bairro"],
            "telefone": p["telefone"],
            "atende_24h": atende_24h,
        })

    saida = {"id": PLANILHA_ID, "total_encontrados": len(resultados),
             "resultados": resultados[:MAX_RESULTADOS]}
    if len(resultados) > MAX_RESULTADOS:   # o corte não pode ser invisível para o modelo
        saida["aviso"] = (f"Mostrando {MAX_RESULTADOS} de {len(resultados)} prestadores. "
                          "Para ver os demais, refine a busca por tipo ou por apenas_24h.")
    return saida



# ======================================================================
# TODO 4b — o contrato (mesmo formato de contratos.py)
# ======================================================================
CONTRATO = {
    "descricao": (
        "Consulta a planilha da rede credenciada do plano de saúde da Aurora e devolve até 5 prestadores "
        "ativos de uma cidade: nome, tipo, especialidades, bairro, telefone e se atende 24 horas. "
        "Use quando o colaborador perguntar qual hospital, laboratório, clínica ou pronto-socorro atende "
        "pelo plano. Prestadores descredenciados ou em negociação não aparecem: indique só os que voltarem. "
        "Quando tiver o que precisa, encerre o atendimento pela ferramenta responder, com o valor do "
        "campo 'id' em fontes; nunca responda em texto livre. "
        "O campo 'total_encontrados' diz quantos prestadores atendem ao filtro; se vier um 'aviso' de "
        "lista cortada, refine por tipo ou por apenas_24h antes de dizer que não há outras opções. "
        "Não use para regras do plano de saúde (carência, inclusão de dependentes, coparticipação, valores): "
        "isso é consultar_regra_beneficio."
    ),
    "parametros": {
        "type": "object",
        "properties": {
            "cidade": {"type": "string", "maxLength": 60,
                       "description": "Cidade onde o colaborador quer ser atendido. Ex.: 'Campinas'."},
            "tipo": {"type": "string", "enum": ["hospital", "laboratorio", "clinica", "pronto-socorro"],
                     "description": "Tipo de prestador. Omita para trazer todos os tipos da cidade."},
            "apenas_24h": {"type": "boolean",
                           "description": "true para trazer só prestadores que atendem 24 horas."},
        },
        "required": ["cidade"],
        "additionalProperties": False,
    },
    "saida": ["id", "total_encontrados", "aviso", "prestador", "tipo", "especialidades", "bairro", "telefone", "atende_24h"],
}


NOME = "consultar_rede_credenciada"


if __name__ == "__main__":   # olhar os dados antes de escrever a ferramenta
    # for linha in SHEETS.ler(PLANILHA_ID, ABA)["values"]:
        # print(linha)

    print(consultar_rede_credenciada("São Paulo"))