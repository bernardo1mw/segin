import nltk
import math
import random
import unicodedata
from collections import defaultdict

# ============================================
# ======== Preparação do Corpus ==============
# ============================================

try:
    nltk.data.find('corpora/floresta')
except LookupError:
    nltk.download('floresta')

from nltk.corpus import floresta

def remover_acentos(txt):
    return ''.join(c for c in unicodedata.normalize('NFD', txt)
                   if unicodedata.category(c) != 'Mn')

# Lista de palavras portuguesas
PALAVRAS_PT = set(
    remover_acentos(w.lower()) for w in floresta.words() if w.isalpha()
)

# Lista de padrões linguísticos (palavras e sufixos comuns)
PADROES = [
    'que', 'para', 'como', 'nao', 'uma', 'das', 'dos', 'mas', 'por', 'se',
    'ao', 'no', 'de', 'em', 'um', 'cao', 'nte', 'ura', 'ica', 'ista', 'ismo',
    'mento', 'dade', 'acao', 'aria', 'avel', 'ivel', 'eiro', 'osa', 'oso'
]

# Gerar modelo de bigramas e trigramas
def gerar_ngramas_corpus():
    texto = ' '.join(floresta.words())
    texto = remover_acentos(texto.lower())
    texto = ''.join(c for c in texto if c.isalpha())

    bigramas = defaultdict(lambda: 1e-8)
    trigramas = defaultdict(lambda: 1e-8)
    total_bi = 0
    total_tri = 0

    for i in range(len(texto) - 1):
        par = texto[i:i+2]
        bigramas[par] += 1
        total_bi += 1

    for i in range(len(texto) - 2):
        tri = texto[i:i+3]
        trigramas[tri] += 1
        total_tri += 1

    for k in bigramas:
        bigramas[k] /= total_bi
    for k in trigramas:
        trigramas[k] /= total_tri

    return bigramas, trigramas

print("Gerando modelo de n-gramas...")
bigramas_freq, trigramas_freq = gerar_ngramas_corpus()
print("Modelo gerado.")

# ============================================
# =============== Funções ====================
# ============================================

ALFABETO = 'abcdefghijklmnopqrstuvwxyz'

def aplicar_chave(texto, chave):
    tabela = str.maketrans(ALFABETO, chave)
    return texto.translate(tabela)

def score_ngramas(texto):
    score = 0.0
    for i in range(len(texto) - 1):
        score += math.log(bigramas_freq.get(texto[i:i+2], 1e-8))
    for i in range(len(texto) - 2):
        score += math.log(trigramas_freq.get(texto[i:i+3], 1e-8))
    return score

def score_palavras(texto):
    count = 0
    for i in range(len(texto) - 2):
        for j in range(3, min(10, len(texto) - i + 1)):
            if texto[i:i+j] in PALAVRAS_PT:
                count += 1
    return count

def score_padroes(texto):
    count = 0
    for padrao in PADROES:
        count += texto.count(padrao)
    return count

def score_total(texto, w_ngram=1.0, w_palavra=2.0, w_padrao=1.5):
    return (
        w_ngram * score_ngramas(texto) +
        w_palavra * score_palavras(texto) +
        w_padrao * score_padroes(texto)
    )

# ============================================
# ========= Algoritmo Genético ===============
# ============================================

def algoritmo_genetico(cipher_text, pop_size=100, geracoes=300, elite_size=5, taxa_mutacao=0.2):
    # Inicialização
    populacao = [''.join(random.sample(ALFABETO, len(ALFABETO))) for _ in range(pop_size)]

    melhor = None
    melhor_score = float('-inf')

    for geracao in range(geracoes):
        scores = []
        for chave in populacao:
            texto = aplicar_chave(cipher_text, chave)
            s = score_total(texto)
            scores.append((s, chave))

            if s > melhor_score:
                melhor = chave
                melhor_score = s

        scores.sort(reverse=True)

        nova_pop = [chave for (_, chave) in scores[:elite_size]]

        while len(nova_pop) < pop_size:
            pai1, pai2 = random.choices(scores[:50], k=2)
            filho = crossover(pai1[1], pai2[1])
            if random.random() < taxa_mutacao:
                filho = mutar(filho)
            nova_pop.append(filho)

        populacao = nova_pop

        if geracao % 20 == 0 or geracao == geracoes -1:
            print(f"[Geração {geracao}] Melhor score: {melhor_score}")

    return melhor


def crossover(p1, p2):
    corte = random.randint(5, 20)
    filho = list(p1[:corte])
    for c in p2:
        if c not in filho:
            filho.append(c)
    return ''.join(filho)

def mutar(chave):
    a, b = random.sample(range(len(chave)), 2)
    lst = list(chave)
    lst[a], lst[b] = lst[b], lst[a]
    return ''.join(lst)

# ============================================
# === Hill Climbing finalizador ============
# ============================================

def hill_climbing(cipher_text, chave_inicial, iteracoes=5000):
    chave = chave_inicial
    texto = aplicar_chave(cipher_text, chave)
    score = score_total(texto)

    for _ in range(iteracoes):
        candidato = mutar(chave)
        texto_cand = aplicar_chave(cipher_text, candidato)
        score_cand = score_total(texto_cand)

        if score_cand > score:
            chave = candidato
            texto = texto_cand
            score = score_cand

    return chave, texto, score

# ============================================
# ================ Execução ==================
# ============================================

cipher_text = "qjseqypdrhigdsgqqyhcjqvqcqmdqgmsibqmmqgliqmqidsgqquhrqdupliqticphdhdhsxpmmqdhxhwuqfqupifpehulipqyhwsuliqdhsliquphbupkhuq"
plain_text = "evocetinhaumnomeetalvezelesnemsoubessemqueseunomeerahenriquejuliananaodissenadapreferiuficarquietaporquenaoqueriabrigare"

print("\nIniciando ataque Premium+...")

chave_ag = algoritmo_genetico(cipher_text)
chave_final, texto_final, score_final = hill_climbing(cipher_text, chave_ag)

print("\n======= Resultado Final =======")
print(f"Chave: {chave_final}")
print(f"Texto decifrado: {texto_final}")
print(f"Score final: {score_final}")
print(f"\n=== Sucesso === \n{texto_final == plain_text}")
