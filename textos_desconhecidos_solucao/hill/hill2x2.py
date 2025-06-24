import numpy as np
from math import gcd
from collections import Counter
from nltk.corpus import floresta

MOD = 26

# --- Utils ---
def text_to_numbers(text):
    return [ord(c) - ord('a') for c in text]

def numbers_to_text(nums):
    return ''.join(chr(n + ord('a')) for n in nums)

def modinv(a):
    for i in range(1, MOD):
        if (a * i) % MOD == 1:
            return i
    return None

# --- Corpus Floresta para validação ---
floresta_vocab = set(w.lower() for w in floresta.words() if w.isalpha())

def count_known_words(text, min_len=3):
    total = 0
    matches = 0
    for i in range(len(text)):
        for j in range(i + min_len, min(len(text) + 1, i + 12)):
            if text[i:j] in floresta_vocab:
                matches += 1
                break
        total += 1
    return matches / total if total else 0

# --- Função de inversão da matriz triangular superior ---
def inv_triang_matrix(x, y, z):
    inv_x = modinv(x)
    inv_z = modinv(z)
    if inv_x is None or inv_z is None:
        return None
    inv = np.array([
        [inv_x % MOD, (-inv_x * y * inv_z) % MOD],
        [0, inv_z % MOD]
    ], dtype=int)
    return inv

# --- Função principal de ataque ---
def ataque_hill_triang(cipher_text):
    nums = text_to_numbers(cipher_text)
    if len(nums) % 2 != 0:
        nums.append(0)  # padding se necessário

    blocos = [nums[i:i+2] for i in range(0, len(nums), 2)]

    valid_vals = [i for i in range(1, 26) if gcd(i, 26) == 1]
    resultados = []

    for x in valid_vals:
        for y in range(26):
            for z in valid_vals:
                inv = inv_triang_matrix(x, y, z)
                if inv is None:
                    continue

                decifrado_nums = []
                for bloco in blocos:
                    vec = np.array(bloco).reshape((2, 1))
                    dec = np.dot(inv, vec) % MOD
                    decifrado_nums.extend(dec.flatten().astype(int))

                texto_decifrado = numbers_to_text(decifrado_nums)

                # Avaliação por palavras
                word_score = count_known_words(texto_decifrado)

                resultados.append((x, y, z, texto_decifrado, word_score))

    # Ordena pelos melhores word_score
    resultados.sort(key=lambda x: -x[4])
    return resultados

if __name__ == "__main__":
    cipher_text = "dzvzkwwutatrkwhapdvqdeuqsadqacnnxegwwusaautahejeqlpvdfrldlbnuejefileheoqidkuacnnxekunfnagiyetvvgoqxdkubfkqqlausaddsilrdz"
   
    resultados = ataque_hill_triang(cipher_text)

    for x, y, z, texto, word_score in resultados[:10]:
        print(f"x={x}, y={y}, z={z}, Words={word_score:.2f}")
        print(texto)
        print('-'*60)
