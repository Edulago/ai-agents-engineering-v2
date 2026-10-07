"""Arquitetura B — workflow determinístico.   (COMPLETE OS TODOs 1 e 2)

O fluxo está escrito no código. O modelo só faz duas tarefas pequenas:
classificar a pergunta e redigir a resposta.

    pergunta ──► classificar ──► tema?
                                   ├── "elegibilidade" ──► escalar (sem chamar o modelo)
                                   └── "rh" | "ti" | "beneficios"
                                          ──► buscar(tema, pergunta) ──► [ modelo + 3 documentos ] ──► resposta

Quem decide o próximo passo é o CÓDIGO, não o modelo.
"""
from comum import modelo
from comum.resultado import Resultado
from ferramentas import buscar, formatar
from politica_de_resposta import FORMATO_JSON, REGRAS

CATEGORIAS = ("rh", "ti", "beneficios", "elegibilidade")


# --------------------------------------------------------------------------
# TODO 1 — o classificador
#
# Escreva o prompt de sistema que faz o modelo responder com UMA das
# CATEGORIAS acima, e nada mais. Dicas:
#   - diga o que entra em cada categoria (ex.: "ti: notebook, senha, VPN...");
#   - "elegibilidade" é quando a pessoa pergunta se ELA tem direito a algo;
#   - peça a resposta em minúsculas, sem pontuação.
# --------------------------------------------------------------------------
PROMPT_CLASSIFICADOR = """
Responda com UMA única palavra, em minúsculas, sem pontuação, escolhida entre:

rh             -> férias, jornada, banco de horas, licenças, trabalho remoto, integração
ti             -> notebook, equipamentos, senha, acesso, VPN, instalação de software
beneficios     -> perguntas gerais sobre plano de saúde, vale-refeição, auxílio-creche
                  (como funciona, quanto vale, como usar)
elegibilidade  -> a pessoa pergunta se ELA MESMA tem direito a algum benefício
                  (ex.: "eu tenho direito ao auxílio-creche?")

Responda apenas com a palavra da categoria.
"""


def classificar(pergunta: str) -> str:
    resposta = modelo.chamar([modelo.mensagem_do_usuario(pergunta)],
                             sistema=PROMPT_CLASSIFICADOR, max_tokens=10)
    categoria = resposta.texto.strip().lower()

    # TODO 1 (continuação): e se o modelo responder algo fora de CATEGORIAS?
    # Decida um comportamento padrão e devolva sempre uma categoria válida.

    # Limpa acento e pontuacao
    categoria = categoria.strip(" .!\"'").replace("í", "i")

    if categoria in CATEGORIAS:
        return categoria
    # tenta achar uma categoria dentro do texto ("a categoria é ti")
    for c in CATEGORIAS:
        if c in categoria:
            return c
    return "rh"   # padrão: escolha sua e justifique no ADR


def resolver(pergunta: str) -> Resultado:
    categoria = classificar(pergunta)

    # ----------------------------------------------------------------------
    # TODO 2 — o roteamento
    #
    # a) Se a categoria for "elegibilidade", devolva direto:
    #        Resultado("escalar", [], "texto explicando que o RH vai analisar")
    #    (repare: esse caminho nem chama o modelo)
    #
    # b) Senão, busque os documentos do tema:   docs = buscar(categoria, pergunta)
    #    Se não vier nenhum documento, devolva Resultado("nao_sei", [], "...").
    #
    # c) Monte o prompt de sistema com REGRAS, FORMATO_JSON e os documentos
    #    (veja como a arquitetura_a.py faz com formatar), chame o modelo
    #    e devolva Resultado.de_json(resposta.texto).
    # ----------------------------------------------------------------------

    # a) elegibilidade vai direto para o RH, sem chamar o modelo
    if categoria == "elegibilidade":
        return Resultado("escalar", [],
                         "A análise de elegibilidade é feita pelo RH. Sua solicitação foi encaminhada.")

    # b) busca os documentos só do tema classificado
    docs = buscar(categoria, pergunta)
    if not docs:
        return Resultado("nao_sei", [], "Não encontrei essa informação nos documentos.")

    # c) igual à arquitetura A, mas só com os documentos encontrados
    documentos = "\n\n".join(formatar(doc) for doc in docs)
    sistema = f"{REGRAS}\n\n{FORMATO_JSON}\n\nDocumentos disponíveis:\n\n{documentos}"

    resposta = modelo.chamar([modelo.mensagem_do_usuario(pergunta)], sistema=sistema)
    return Resultado.de_json(resposta.texto)
