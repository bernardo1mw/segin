import numpy as np
import re
from collections import Counter
from itertools import product
from sympy import Matrix
from unidecode import unidecode

# -------------------------
# Utilitários
# -------------------------

def normalize(text):
    """Remove acentos, converte para minúsculas, remove não-letras."""
    text = unidecode(text.lower())
    return re.sub('[^a-z]', '', text)

def text_to_numeric(text):
    """Converte texto em lista de números: a=0, ..., z=25"""
    return [ord(c) - ord('a') for c in text]

def numeric_to_text(nums):
    """Converte lista de números para texto"""
    return ''.join(chr(n % 26 + ord('a')) for n in nums)

def chunkify(lst, size):
    """Divide lista em blocos do mesmo tamanho"""
    return [lst[i:i + size] for i in range(0, len(lst), size)]

# -------------------------
# Inversão Modular para Hill
# -------------------------

def modinv_matrix(mat, mod=26):
    """Inversa modular de uma matriz usando sympy"""
    print(mat)
    sympy_mat = Matrix(mat)
    if sympy_mat.det() % mod == 0:
        raise ValueError(f"Matriz não invertível mod {mod}")
    return np.array(sympy_mat.inv_mod(mod)).astype(int) % mod
