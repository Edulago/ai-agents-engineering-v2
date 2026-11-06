# Nota de avaliação · Encontro 5

**Equipe: BEEFIM**
**Integrantes:**

- 373155 EDUARDO LAGO
- 374640 BRUNA CARLA PEREIRA
- 369873 ELIAS MAX LOPES
- 373300 FELIPE HENRIQUE DE ALBUQUERQUE
- 375303 IGOR DA SILVA FERRAZ
- 375217 MATHEUS MENEZES MANFRIN

**Domínio:** caso Aurora

> Uma página. As tabelas das seções 1, 2 e 4 saem prontas do Passo 6 do notebook 02. O que vale nota é o
> raciocínio das seções 3, 4 e 5: números que aguentam o teste do ruído e uma decisão defendida.

## 1 · Golden set do grupo

8 perguntas do banco de produção, com o gabarito que o grupo escreveu a partir da wiki. O arquivo
`encontro-05/golden-equipe.json` está no fork.

## Golden set do grupo

| id | pergunta | desfecho | fontes | contém | não contém |
|---|---|---|---|---|---|
| B02 | Posso vender parte das minhas férias? Quantos dias? | responder | rh-ferias | 10 dias / dez dias |  |
| B04 | Qual a diária máxima de hotel numa viagem para uma capital? | responder | fin-viagens-e-reembolso | R$ 450 / 450 |  |
| B05 | Levei um cliente para jantar e pedimos vinho. A bebida é reembolsada? | responder | fin-viagens-e-reembolso | não são reembolsadas / não é reembolsadas |  |
| B13 | Meu filho nasceu há 40 dias. Ainda dá para incluir ele no plano de saúde sem carência? | responder | beneficios-plano-de-saude | novembro |  |
| B17 | Posso trabalhar duas semanas de Portugal? | responder | rh-trabalho-remoto | 30 dias / trinta dias |  |
| B19 | A empresa paga bônus de fim de ano? | nao_sei |  |  |  |
| B22 | Sou contratado como PJ. Tenho direito ao vale-refeição? | escalar |  |  |  |
| B23 | Valeu pela ajuda, até mais! | responder |  |  |  |

**Um gabarito difícil de decidir** (id, as duas leituras possíveis e por que o grupo escolheu esta):

## 2 · Placar

Golden set da turma (25 casos) mais o do grupo (8), 5 amostras de cada.

| versão | acerto (IC 90%) | pass^5 | instáveis | US$/acerto | p95 (s) | loops |
|---|---|---|---|---|---|---|
| v1 · produção | 70% (58%–81%) | 58% | 10/33 | 0.00081 | 9.3 | 12% |
| v2 · prompt enxuto (PR #42) | 73% (60%–84%) | 67% | 5/33 | 0.00043 | 5.4 | 0% |
| v3 · modelo mais barato | 98% (94%–100%) | 94% | 2/33 | 0.00022 | 4.4 | 0% |

## 3 · Regressão ou ruído

- ruído (teste A/A da v1): até 9% entre duas rodadas
- PR #42: +3% (IC 90%: -5% a +12%) · não dá para afirmar · pioraram: P1, R1, G5 · melhoraram: C2, B13, B22
...
| custo_por_acerto ≤ US$ 0.00050 | **FALHA** (US$ 0.00081) | passa (US$ 0.00043) | passa (US$ 0.00022) |
| p95_segundos ≤ 8.0s | **FALHA** (9.3s) | passa (5.4s) | passa (4.4s) |
| bateu_limite ≤ 2% | **FALHA** (12%) | passa (0%) | passa (0%) |
| aprovado_pelo_juiz ≥ 85% | passa (93%) | **FALHA** (85%) | passa (96%) |

**Os casos do grupo mudaram alguma conclusão?** (uma ou duas frases)

## 4 · SLOs e gate

| SLO | por que esse número (e quem na Aurora concordaria) |
|---|---|
| acerto ≥ 90% | Resposta errada sobre RH ou benefício gera reclamação e retrabalho; abaixo disso, compensa perguntar direto ao RH. (Diretoria de RH) |
| custo_por_acerto ≤ US$ 0,0005 | Precisa ficar abaixo do custo da v1 atual, porque o volume é alto. (Financeiro) |
| p95_segundos ≤ 8 s | Num chat, mais de 8 s de espera faz o colaborador desistir e abrir chamado. (Produto / TI) |
| bateu_limite ≤ 2% | Loop é custo jogado fora e colaborador sem resposta, como no B19. (Engenharia) |
| aprovado_pelo_juiz ≥ 85% | É o único SLI medível em produção, sem gabarito. (Engenharia, monitoramento) |

| SLO | v1 | v2 | v3 |
|---|---|---|---|
| acerto ≥ 90% | ✘ 70% | ✘ 73% | ✔ 98% |
| custo_por_acerto ≤ US$ 0,0005 | ✘ 0,00081 | ✔ 0,00043 | ✔ 0,00022 |
| p95 ≤ 8 s | ✘ 9,3 s | ✔ 5,4 s | ✔ 4,4 s |
| bateu_limite ≤ 2% | ✘ 12% | ✔ 0% | ✔ 0% |
| aprovado_pelo_juiz ≥ 85% | ✔ 93% | ✘ 85% | ✔ 96% |
| **pode ir para produção?** | NÃO | NÃO | SIM |

**A decisão:** que versão vai para produção, contra o quê, com que números, e o que faria o grupo mudar de ideia.

## 5 · Um atendimento por dentro

**Caso, versão e amostra:**  B19 ("A empresa paga bônus de fim de ano?"), v1, amostra 0.

**O que a cascata mostra** (passos, onde foi o tempo, o que a busca devolveu): 8 buscas sem achar nada (a wiki ñ fla de bônus), 7,4 s e 13 mil tokens

**Diagnóstico** (camada da pirâmide em que o problema aparece primeiro, e o que consertaria):  o erro está num passo do agente: depois da primeira busca vazia, ele deveria dizer "não sei". Conserto: regra no prompt "busca sem resultado = nao_sei".

---

*Opcional, para equipes que trocaram de domínio:* três perguntas da produção da empresa de vocês que
entrariam no golden set, e o SLO de qualidade que o negócio aceitaria.
