
# 📜 Documentação - Extração de Chave da Cifra de Vigenère

## 📌 Objetivo

Este script tem como objetivo **extrair a chave utilizada em uma cifra de Vigenère**, dado o texto aberto (plaintext) e o texto cifrado (ciphertext), ambos conhecidos, além do tamanho da chave.

---

## 🚀 Descrição do Funcionamento

### 1️⃣ **Importação de Dependências**
```python
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import normalize, text_to_numeric, numeric_to_text
```
- Insere o diretório pai no caminho (`sys.path`) para importar funções auxiliares (`utils.py`).
- Funções utilizadas do módulo `utils`:
  - `normalize`: normaliza texto (ex.: remover acentos e caracteres inválidos).
  - `text_to_numeric`: converte texto para lista de números (a=0, b=1, ..., z=25).
  - `numeric_to_text`: faz o caminho inverso, converte números para texto.

---

### 2️⃣ **Extração da Chave**
```python
def extract_vigenere_key(plain_text, cipher_text, key_length):
    plain_n = text_to_numeric(normalize(plain_text))
    cipher_n = text_to_numeric(normalize(cipher_text))

    key = [ (c - p) % 26 for p, c in zip(plain_n, cipher_n) ]

    final_key = [ key[i] for i in range(key_length) ]

    return final_key, numeric_to_text(final_key)
```
- A cifra de Vigenère funciona como:
```plaintext
c_i = (p_i + k_i) mod 26
```
- Para extrair a chave:
```plaintext
k_i = (c_i - p_i) mod 26
```
- O vetor `key` contém a chave **expandida** (repetida até o tamanho do texto).
- A linha:
```python
final_key = [ key[i] for i in range(key_length) ]
```
- Extrai a chave **original**, com comprimento igual a `key_length`.

---

### 3️⃣ **Expansão da Chave**
```python
def expand_vigenere_key(key_text, length):
    repeats = (length + len(key_text) - 1) // len(key_text)
    return (key_text * repeats)[:length]
```
- Expande uma chave de tamanho fixo até o tamanho do texto.
- A expansão é cíclica.

---

### 4️⃣ **Leitura dos Arquivos**
```python
with open(..._texto_aberto.txt) as f: plain = f.read().strip()
with open(..._texto_cifrado.txt) as f: cipher = f.read().strip()
with open(..._key.txt) as f: key_cipher = f.read().strip()
```
- Lê três arquivos:
  - Texto aberto.
  - Texto cifrado.
  - Chave correta (para verificação).

---

### 5️⃣ **Processamento Principal**
```python
key_nums, key_text = extract_vigenere_key(plain, cipher, key_length=k_len)
key_expanded = expand_vigenere_key(key_text, text_length)
```
- Extrai a chave (`key_text`).
- Gera a chave expandida (`key_expanded`) para comparar com a chave verdadeira.

---

### 6️⃣ **Validação e Impressão dos Resultados**
```python
print(f"🔐 Chave Vigenère (tamanho {k_len}): {key_text}")
print(f"🔐 Chave Vigenère Expandida (tamanho {k_len}): {key_expanded}")
print(f"Chaves idênticas: {key_cipher == key_expanded}")
```
- Valida se a chave extraída, quando expandida, é idêntica à chave real fornecida.

---

## ✔️ Resultado Esperado

- Impressão da chave extraída.
- Verificação se a chave expandida bate com a chave real do arquivo.

---

## 💡 Observações

- O script assume que o tamanho da chave (`k_len`) é conhecido.
- O sucesso depende de ambos os textos (aberto e cifrado) estarem bem alinhados e normalizados.
