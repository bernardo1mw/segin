from collections import Counter
from unidecode import unidecode
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import normalize

def mono_key_by_frequency(plain_text, cipher_text):
    # Normaliza e calcula frequências
    plain = normalize(plain_text)
    cipher = normalize(cipher_text)

    freq_plain = Counter(plain)
    freq_cipher = Counter(cipher)

    # Ordena por frequência decrescente
    sorted_plain = [item[0] for item in freq_plain.most_common()]
    sorted_cipher = [item[0] for item in freq_cipher.most_common()]

    # Mapeamento inicial: cifra -> claro
    mapping = dict(zip(sorted_cipher, sorted_plain))

    # Gera chave completa: letra cifrada → letra do claro
    key = {}
    for i in range(26):
        c = chr(ord('a') + i)
        key[c] = mapping.get(c, '?')  # '?' = letra não mapeada (infrequente)

    return key


def decrypt_mono(cipher_text, key_map):
    cipher = normalize(cipher_text)
    decrypted = []

    for c in cipher:
        decrypted.append(key_map.get(c, '?'))  # usa '?' se a letra não estiver mapeada

    return ''.join(decrypted)


plain_mono = "manhaocaboalmeidaperguntaoqueelesestaofazendoaliaaquelahoraasarmasestaoapontadasparaelesenquantoestaocomasmaosnacabecaoc"
cipher_mono = "cbetbvrbzvbdcimpbwiygfejbvsfiidikikjbvnbuiepvbdmbbsfidbtvybbkbycbkikjbvbwvejbpbkwbybidikiesfbejvikjbvrvcbkcbvkebrbzirbvr"
# Chave: letra cifrada → estimativa da letra clara
mono_key = mono_key_by_frequency(
    plain_mono,
    cipher_mono
)

# Aplicando descriptografia
plain_mono_est = decrypt_mono(cipher_mono, mono_key)

print("🔓 Texto descriptografado (estimado):")
print(plain_mono_est)
print("Textos idênticos: ", plain_mono == plain_mono_est)
