
# 📜 Documentação — Análise e Descriptografia por Frequência para Cifra Monoalfabética

## ✅ Descrição Geral
Este código realiza uma descriptografia estimada de uma **cifra monoalfabética simples**, utilizando uma análise de frequência das letras no texto cifrado e no texto claro.

A cifra monoalfabética consiste na substituição de cada letra do texto claro por uma letra fixa do alfabeto, de acordo com uma chave de substituição.

## 🚀 Estrutura do Código

### 1️⃣ Imports
```python
from collections import Counter
from unidecode import unidecode
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import normalize
```
- `Counter`: conta a frequência de cada letra.
- `unidecode`: remove acentos e normaliza caracteres.
- `normalize`: função própria (do módulo utils) para normalizar os textos (remover espaços, acentos e transformar em minúsculas).

---

### 2️⃣ Função `mono_key_by_frequency(plain_text, cipher_text)`

#### ✔️ Objetivo:
Gerar uma chave de mapeamento entre as letras do texto cifrado e do texto claro, **baseada na frequência das letras.**

#### ✔️ Etapas:
1. Normaliza os textos (`plain` e `cipher`).
2. Calcula a frequência de cada letra usando `Counter`.
3. Ordena as letras do texto claro e do cifrado por frequência decrescente.
4. Faz o mapeamento associando a letra mais frequente do texto cifrado com a mais frequente do texto claro, e assim por diante.
5. Cria um dicionário `key` que mapeia todas as 26 letras do alfabeto:
   - Se uma letra não existir no texto cifrado, ela recebe `'?'`.

#### ✔️ Saída:
Dicionário `key` com o mapeamento:  
**letra cifrada → letra do texto claro (estimada)**

---

### 3️⃣ Função `decrypt_mono(cipher_text, key_map)`

#### ✔️ Objetivo:
Descriptografar o texto cifrado utilizando o mapa de chave fornecido.

#### ✔️ Etapas:
1. Normaliza o texto cifrado.
2. Para cada letra, consulta o mapeamento na chave `key_map`.
3. Se uma letra não estiver presente no mapa, retorna `'?'`.

#### ✔️ Saída:
String com o texto descriptografado (estimado).

---

### 4️⃣ Execução Principal

#### ✔️ Textos de entrada:
```python
plain_mono = "..."     # Texto claro conhecido
cipher_mono = "..."    # Texto cifrado
```

#### ✔️ Processos:
1. Geração da chave estimada:
```python
mono_key = mono_key_by_frequency(plain_mono, cipher_mono)
```
2. Descriptografia:
```python
plain_mono_est = decrypt_mono(cipher_mono, mono_key)
```
3. Impressão dos resultados:
- Texto descriptografado (estimado).
- Verificação se o texto estimado é igual ao texto claro original.

---

## 🔍 Exemplo de Saída:

```
🔓 Texto descriptografado (estimado):
manhaocaboalmeidaperguntaoqueelesestaofazendoaliaaquelahoraasarmasestaoapontadasparaelesenquantoestaocomasmaosnacabecaoc
Textos idênticos: True
```

---

## ⚙️ Observações Técnicas
- Este método depende da distribuição de frequência de letras. Funciona bem para textos longos.
- Em textos curtos, pode haver erros se as distribuições não forem representativas.
- A letra `'?'` indica que não houve correspondência suficiente.

## 🧠 Melhorias Futuras
- Refinamento usando análise de bigramas ou trigramas.
- Aplicação de algoritmos genéticos ou simulated annealing para ajustar erros em textos curtos.
- Uso de dicionários para pós-correção de palavras.

---

## ✍️ Autor
Gerado automaticamente via ChatGPT (OpenAI) — 2025