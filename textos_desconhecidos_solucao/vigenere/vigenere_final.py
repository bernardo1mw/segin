import numpy as np
import unicodedata
import nltk
import random

# Dependências: nltk, numpy
try:
    nltk.data.find('corpora/floresta')
except LookupError:
    nltk.download('floresta')
from nltk.corpus import floresta

# Remover acentos
def remover_acentos(palavra):
    return ''.join(ch for ch in unicodedata.normalize('NFD', palavra)
                   if unicodedata.category(ch) != 'Mn')

# Palavras válidas
fl_palavras = [remover_acentos(w.lower()) for w in floresta.words() if w.isalpha()]
dicionario = set(w for w in fl_palavras if len(w) >= 4)

# Contagem de bigramas e trigramas
bigram_counts, trigram_counts = {}, {}
total_bigrams = total_trigrams = 0
for w in fl_palavras:
    for i in range(len(w)-1):
        bi = w[i:i+2]
        bigram_counts[bi] = bigram_counts.get(bi, 0) + 1
        total_bigrams += 1
    for i in range(len(w)-2):
        tri = w[i:i+3]
        trigram_counts[tri] = trigram_counts.get(tri, 0) + 1
        total_trigrams += 1
V_bi, V_tri = 26*26, 26*26*26

# Frequências de letras em português (normalizadas)
freq_portuguese = {
    'a': 0.132272, 'b': 0.009191, 'c': 0.035846, 'd': 0.053079,
    'e': 0.153723, 'f': 0.008042, 'g': 0.012638, 'h': 0.008042,
    'i': 0.078339, 'j': 0.001838, 'k': 0.000005, 'l': 0.031020,
    'm': 0.050092, 'n': 0.047105, 'o': 0.104319, 'p': 0.018382,
    'q': 0.008272, 'r': 0.059743, 's': 0.057445, 't': 0.050092,
    'u': 0.038143, 'v': 0.018612, 'w': 0.000004, 'x': 0.001378,
    'y': 0.000008, 'z': 0.003217
}
total_freq = sum(freq_portuguese.values())
freq_portuguese = {k: v/total_freq for k, v in freq_portuguese.items()}

def decifrar_vigenere(texto, chave):
    res = []
    k = len(chave)
    for i, c in enumerate(texto):
        if 'a' <= c <= 'z':
            c_val = ord(c) - ord('a')
            k_val = ord(chave[i % k]) - ord('a')
            res.append(chr((c_val - k_val) % 26 + ord('a')))
        else:
            res.append(c)
    return ''.join(res)

def pontuacao_texto(txt):
    score = 0.0
    for i in range(len(txt)-1):
        bi = txt[i:i+2]
        if bi.isalpha():
            cnt = bigram_counts.get(bi, 0)
            score += np.log((cnt + 1) / (total_bigrams + V_bi))
    for i in range(len(txt)-2):
        tri = txt[i:i+3]
        if tri.isalpha():
            cnt = trigram_counts.get(tri, 0)
            score += 2 * np.log((cnt + 1) / (total_trigrams + V_tri))
    palavras = 0
    for sz in range(4, 11):
        for i in range(len(txt)-sz+1):
            if txt[i:i+sz] in dicionario:
                palavras += 1
    score += 7.0 * palavras
    return score

def melhor_deslocamento(fatia):
    best_k = 0; best_s = -1e9
    for k in range(26):
        dec = [(ord(c)-ord('a')-k) % 26 for c in fatia]
        s = sum(freq_portuguese[chr(v+ord('a'))] for v in dec)
        if s > best_s:
            best_s, best_k = s, k
    return chr(best_k + ord('a'))

def hill_climb(init_key, texto, max_no_improve=500):
    best_key = init_key
    best_score = pontuacao_texto(decifrar_vigenere(texto, best_key))
    no_imp = 0
    while no_imp < max_no_improve:
        i = random.randrange(len(best_key))
        letra = chr(random.randrange(26) + ord('a'))
        if letra == best_key[i]: continue
        cand = best_key[:i] + letra + best_key[i+1:]
        s = pontuacao_texto(decifrar_vigenere(texto, cand))
        if s > best_score:
            best_key, best_score = cand, s
            no_imp = 0
        else:
            no_imp += 1
    return best_key, best_score

def refinar_chave_proxima(chave_base, texto_cifrado, max_iter_sem_melhora=10000):
    melhor_chave = chave_base
    melhor_score = pontuacao_texto(decifrar_vigenere(texto_cifrado, melhor_chave))
    sem_melhora = 0
    while sem_melhora < max_iter_sem_melhora:
        nova = list(melhor_chave)
        i = random.randint(0, len(nova) - 1)
        letra_antiga = nova[i]
        nova[i] = chr((ord(letra_antiga) - ord('a') + random.randint(1, 25)) % 26 + ord('a'))
        nova_chave = ''.join(nova)
        score = pontuacao_texto(decifrar_vigenere(texto_cifrado, nova_chave))
        if score > melhor_score:
            melhor_chave = nova_chave
            melhor_score = score
            sem_melhora = 0
        else:
            sem_melhora += 1
    return melhor_chave, melhor_score, decifrar_vigenere(texto_cifrado, melhor_chave)

def refinar_posicoes(chave_base, texto, posicoes):
    from itertools import product

    melhor_chave = chave_base
    melhor_score = pontuacao_texto(decifrar_vigenere(texto, chave_base))

    for letras in product(range(26), repeat=len(posicoes)):
        nova = list(chave_base)
        for p, l in zip(posicoes, letras):
            nova[p] = chr(ord('a') + l)
        nova_chave = ''.join(nova)
        score = pontuacao_texto(decifrar_vigenere(texto, nova_chave))
        if score > melhor_score:
            melhor_chave = nova_chave
            melhor_score = score

    return melhor_chave, melhor_score, decifrar_vigenere(texto, melhor_chave)

def decifrar_automatico(texto_cifrado, K=30):
    print("============================")
    print("Iniciando Descriptografia")
    print("============================")
    
    # 1) Chave inicial por frequência
    chave_init = []
    for i in range(K):
        fat = [texto_cifrado[j] for j in range(i, len(texto_cifrado), K)]
        chave_init.append(melhor_deslocamento(''.join(fat)))
    chave_init = ''.join(chave_init)

    # 2) Reinícios aleatórios + hill-climbing
    RESTARTS = int(15*(K/10))
    best_key, best_score = None, -np.inf
    for r in range(RESTARTS):
        print(f"Iteração {r} de {RESTARTS}")
        if r == 0:
            init = chave_init
        else:
            init = ''.join(chr(random.randrange(26)+ord('a')) for _ in range(K))
        k_r, s_r = hill_climb(init, texto_cifrado)
        if s_r > best_score:
            best_key, best_score = k_r, s_r

    # 3) Resultado final
    plaintext = decifrar_vigenere(texto_cifrado, best_key)
    print("============================")
    print("Resultados Iniciais")
    print("============================")
    
    print("Chave provável:", best_key)
    print("Texto decifrado:", plaintext)
    print("Pontuação:", best_score)

    print("\n\n============================")
    print("Iniciando refinamento")
    print("============================")

    # Refinamento inicial
    best_key, best_score, plaintext = refinar_chave_proxima(best_key, texto_cifrado)
    
    # Refinamento em grupos de 3 posições com slide
    tamanho_chave = len(best_key)
    # while True:
    #     melhorou = False
    for inicio in range(tamanho_chave - 2):
        posicoes = [inicio, inicio + 1, inicio + 2]
        print(f"\nRefinando posições {posicoes}")
        
        chave_temp, score_temp, texto_temp = refinar_posicoes(
            best_key,
            texto_cifrado,
            posicoes=posicoes
        )
        
        if score_temp > best_score:
            best_key = chave_temp
            best_score = score_temp
            plaintext = texto_temp
            melhorou = True
            print(f"Melhoria encontrada! Nova pontuação: {best_score}")
            print(f"Nova chave: {best_key}")
            #break
    
        # if not melhorou:
        #     break

    print("============================")
    print("Resultados Refinados")
    print("============================")

    print("Chave provável:", best_key)
    print("Texto decifrado:", plaintext)
    print("Pontuação:", best_score)

    return best_key, plaintext, best_score

if __name__ == "__main__":
    texto_cifrado = "textocifrado"
    tamanho_chave = 10
    chave, texto_decifrado, pontuacao = decifrar_automatico(texto_cifrado, tamanho_chave) 