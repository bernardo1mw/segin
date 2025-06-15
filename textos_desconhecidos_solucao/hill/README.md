
# 🧠 Documentação Técnica — Ataque à Cifra de Hill 3x3 com Pré-filtragem Heurística

## 📜 1. Descrição do Problema

Este código tem como objetivo realizar a **criptanálise da cifra de Hill 3x3**, onde a matriz de chave possui formato triangular superior:

```
| x y z |
| 0 a b |
| 0 0 c |
```

O ataque não possui a chave original nem o texto aberto, apenas o texto cifrado.

O processo consiste em quebrar a cifra explorando propriedades matemáticas da cifra de Hill e utilizando heurísticas linguísticas em português para avaliar a qualidade dos textos decifrados.

## 🏛️ 2. Fundamentos da Cifra de Hill

- É uma cifra poligráfica baseada em álgebra linear.
- Cada bloco de 3 letras é convertido em um vetor numérico.
- O vetor é multiplicado pela matriz-chave no módulo 26.
- A decifragem requer a inversa da matriz no módulo 26.

## 🔐 3. Formato da Matriz-Chave

A matriz possui a seguinte estrutura triangular superior:

```
| x y z |
| 0 a b |
| 0 0 c |
```

- `x`, `a`, `c` devem ser inversíveis em módulo 26 (i.e., gcd(valor, 26) = 1).
- O objetivo é encontrar `(a, b, c)` e depois `(x, y, z)`.

## 🏗️ 4. Estrutura do Algoritmo

### 🔹 Passo 1 — Encontrar candidatos para `c` (linha 3)

- A letra na posição 3 do bloco só sofre influência do valor `c`.
- A função `encontrar_candidatos_c()` calcula o chi-quadrado das frequências das letras após aplicar todos os `c` possíveis.
- Seleciona os `top_n` melhores `c` com menor chi-quadrado.

### 🔹 Passo 2 — Encontrar candidatos para `(a, b)` (linha 2)

- A letra na posição 2 do bloco é afetada por `a` e `b`.
- A função `encontrar_candidatos_ab()` testa todas as combinações válidas de `(a, b)` e calcula o chi-quadrado das letras na segunda posição dos blocos.
- Filtra os melhores.

### 🔹 Passo 3 — Explorar a Primeira Linha `(x, y, z)`

- A primeira linha tem impacto total no texto.
- É a parte mais pesada computacionalmente.
- A função `testar_primeira_linha()` explora todas as combinações válidas de `(x, y, z)`:
  - `x` e `z` devem ser inversíveis.
  - `y` varia de 0 a 25.

Utiliza `ProcessPoolExecutor` para paralelizar os testes.

## 🎯 5. Avaliação de cada chave

Para cada chave candidata, é gerado o texto decifrado. Esse texto é avaliado por três métricas:

### 1️⃣ Chi-Quadrado (`chi_squared_score`)

- Mede a aderência das frequências das letras ao idioma português.
- Valores menores indicam que a distribuição de letras é mais natural.

### 2️⃣ Word Coverage (`word_coverage_ratio`)

- Mede a proporção de caracteres que fazem parte de palavras reais do português.
- Realiza uma segmentação gulosa do texto usando o corpus `nltk.floresta`.

### 3️⃣ Heurística combinada

```
combined_score = word_score - chi_squared / fator
```

Quanto maior o `word_score` e menor o `chi_squared`, melhor a chave.

## 🏃‍♂️ 6. Paralelização

- Toda a expansão da primeira linha é paralelizada usando `ProcessPoolExecutor`.
- Isso permite testar milhares de chaves simultaneamente, reduzindo drasticamente o tempo.

## 🔍 7. Funções-chave

### ✔️ Avaliação da Chave:

```python
def avaliar_klinha(args):
```
- Calcula:
  - Texto decifrado
  - Chi-quadrado
  - Word coverage
- Retorna uma tupla com os resultados.

### ✔️ Testar Primeira Linha:

```python
def testar_primeira_linha(candidatos_ab_c, blocks, top_n=5):
```
- Recebe os melhores `(a, b, c)`.
- Gera tarefas com combinações de `(x, y, z)`.
- Executa em paralelo.
- Retorna os `top_n` melhores resultados.

### ✔️ Ataque Principal:

```python
def ataque_hill_otimizado(ciphertext, max_c=10, max_ab=20, top_k=5):
```
- Orquestra todo o processo:
  - Candidatos para `c`
  - Candidatos para `(a,b)`
  - Teste da primeira linha
- Imprime os melhores resultados.

## 📦 8. Heurística Rápida

```python
def heuristica_rapida(texto):
```
- Filtra textos com excesso de repetições como `aaaa` ou `bbb`.
- Rápido pré-filtro para eliminar chaves claramente inválidas.

## 🔎 9. Avaliar Chave Manualmente

```python
def testar_chave_hardcoded(ciphertext, chave):
```
- Permite testar uma chave manual, fornecida pelo usuário.
- Calcula chi², word coverage e combined score.

## ⚙️ 10. Fluxo Geral do Código

```
1. Converter texto cifrado para números.
2. Gerar blocos de tamanho 3.
3. Encontrar os melhores valores de c.
4. Para cada c:
    - Encontrar os melhores (a, b).
5. Para cada (a, b, c):
    - Explorar todas as combinações de (x, y, z) com paralelização.
6. Avaliar os textos decifrados.
7. Retornar os melhores resultados com a chave e o texto.
```

## 🚧 11. Limitações

- Crescimento exponencial no espaço da primeira linha `(x, y, z)`.
- Mesmo com paralelização, o Hill 4x4 já se torna proibitivo nesse modelo.
- Para Hill 4x4, usar estratégias como:
  - 🔥 Simulated Annealing
  - 🔥 Algoritmos Genéticos
  - 🔥 Beam Search
