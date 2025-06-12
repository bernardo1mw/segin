import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import normalize, text_to_numeric, numeric_to_text

def extract_vigenere_key(plain_text, cipher_text, key_length):
    plain_n = text_to_numeric(normalize(plain_text))
    cipher_n = text_to_numeric(normalize(cipher_text))

    key = [ (c - p) % 26 for p, c in zip(plain_n, cipher_n) ]

    # Agrupar por posição na chave
    final_key = [ key[i] for i in range(key_length) ]

    return final_key, numeric_to_text(final_key)

def expand_vigenere_key(key_text, length):
    repeats = (length + len(key_text) - 1) // len(key_text)  # teto da divisão
    return (key_text * repeats)[:length]


k_len = 60

with open(f"/home/bernardo/Desktop/faculdade/SEGIN/data/textos_conhecidos/Aberto/Vigenere/Grupo21_{k_len}_texto_aberto.txt", "r") as f:
    plain = f.read().strip()
with open(f"/home/bernardo/Desktop/faculdade/SEGIN/data/textos_conhecidos/Cifrado/Vigenere/Grupo21_{k_len}_texto_cifrado.txt", "r") as f:
    cipher = f.read().strip()
with open(f"/home/bernardo/Desktop/faculdade/SEGIN/data/textos_conhecidos/Aberto/Vigenere/Grupo21_{k_len}_key.txt", "r") as f:
    key_cipher = f.read().strip()


text_length = len(plain)
key_nums, key_text = extract_vigenere_key(plain, cipher, key_length=k_len)
key_expanded = expand_vigenere_key(key_text, text_length)
print(f"🔐 Chave Vigenère (tamanho {k_len}): {key_text}")
print(f"🔐 Chave Vigenère Expandida (tamanho {k_len}): {key_expanded}")
print(f"Chaves idênticas: {key_cipher == key_expanded}")

