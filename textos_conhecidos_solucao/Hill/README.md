
# 📄 Documentação do Código — Descoberta de Chave na Cifra de Hill NxN

## 📜 Descrição Geral

Este código tem como objetivo **descobrir a chave (matriz K)** utilizada na cifra de Hill de tamanho NxN, a partir de um texto conhecido em claro (`plain`) e seu correspondente texto cifrado (`cipher`).

O processo se baseia na propriedade fundamental da cifra de Hill:

> **C = K × P (mod m)**  
> Onde:
> - C = bloco cifrado (matriz)
> - P = bloco de texto claro (matriz)
> - K = chave (matriz NxN)

A chave pode ser obtida por:
> **K = C × P⁻¹ (mod m)**  
(se P é invertível módulo m)

---

## 📂 Organização do Código

### 🔗 Importações
```python
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import normalize, text_to_numeric, chunkify, modinv_matrix
import numpy as np
```

- Adiciona o diretório pai ao path (`sys.path.append`) para importar funções utilitárias de `utils.py`:
  - `normalize`: remove acentos, espaços e coloca em minúsculas.
  - `text_to_numeric`: converte texto para lista de números (a=0, b=1, ..., z=25).
  - `chunkify`: divide listas em blocos.
  - `modinv_matrix`: calcula a matriz inversa módulo 26.

---

### 📑 Carregamento dos Dados
```python
block_size = 4

with open("/path/aberto.txt") as f:
    plain = f.read().strip()
with open("/path/cifrado.txt") as f:
    cipher = f.read().strip()
```

- Define o tamanho do bloco (NxN).
- Carrega texto claro (`plain`) e texto cifrado (`cipher`) a partir de arquivos.

---

### 🔄 Pré-processamento
```python
plain_n = text_to_numeric(normalize(plain))
cipher_n = text_to_numeric(normalize(cipher))
```
- Normaliza (remove espaços, acentos e transforma em minúsculas).
- Converte textos para listas de números (inteiros de 0 a 25).

---

## 🔍 Função Principal — `find_valid_hill_key()`
```python
def find_valid_hill_key(plain_n, cipher_n, block_size, mod=26):
```
- Procura um bloco de texto claro (`P_block`) que seja **invertível módulo 26**.
- A cada tentativa:
  - Extrai um bloco de tamanho NxN do texto claro e do cifrado.
  - Calcula a inversa módulo 26 de `P_block`.
  - Obtém a chave pela fórmula: **K = (C_block × P_inv) mod 26**.

Se um bloco válido for encontrado, retorna:
- A matriz chave `K`.
- O índice inicial do bloco dentro do texto (`start_idx`).

Caso nenhum bloco válido seja encontrado, levanta uma exceção.

---

### 🚀 Execução
```python
K_NxN, start_idx = find_valid_hill_key(plain_n, cipher_n, block_size=block_size)
print(f"Chave encontrada (a partir do índice {start_idx}):
{K_NxN}")
```
- Executa a função e imprime a chave encontrada e o índice onde ela foi extraída.

---

## ✅ Observações Importantes
- O método funciona apenas se houver no texto claro um bloco NxN cuja matriz seja **invertível módulo 26**.
- Caso contrário, será necessário:
  - Usar outros blocos.
  - Ou empregar métodos de ataque mais avançados (heurísticos, força bruta ou análise estatística).

---

## 🧠 Conclusão
Este código implementa a base matemática fundamental da criptanálise conhecida como **ataque de texto claro conhecido** para a cifra de Hill NxN.
