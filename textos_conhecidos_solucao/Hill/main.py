# Hill 2x2: primeiro par de blocos
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import normalize, text_to_numeric, chunkify, modinv_matrix
import numpy as np

block_size = 4

with open(f"/home/bernardo/Desktop/faculdade/SEGIN/data/textos_desconhecidos/Aberto/Hill/Grupo21_{block_size}_texto_aberto.txt", "r") as f:
    plain = f.read().strip()
with open(f"/home/bernardo/Desktop/faculdade/SEGIN/data/textos_desconhecidos/Cifrado/Hill/Grupo21_{block_size}_texto_cifrado.txt", "r") as f:
    cipher = f.read().strip()

# Normalização e conversão
plain_n = text_to_numeric(normalize(plain))
cipher_n = text_to_numeric(normalize(cipher))
def find_valid_hill_key(plain_n, cipher_n, block_size, mod=26):
    step = block_size  # desliza de bloco em bloco
    max_index = len(plain_n) - block_size**2 + 1

    for i in range(0, max_index, step):
        try:
            P_block = np.array(chunkify(plain_n[i:i + block_size**2], block_size)).T
            C_block = np.array(chunkify(cipher_n[i:i + block_size**2], block_size)).T
            P_inv = modinv_matrix(P_block, mod)
            K = (C_block @ P_inv) % mod
            return K, i
        except ValueError:
            continue
    raise Exception(f"Nenhum bloco invertível encontrado para Hill {block_size}x{block_size}.")

# Executa a busca
K_NxN, start_idx = find_valid_hill_key(plain_n, cipher_n, block_size=block_size)
print(f"Chave encontrada (a partir do índice {start_idx}):\n{K_NxN}")


