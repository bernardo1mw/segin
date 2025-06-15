
# 📄 Relatório Técnico — Ataque à Cifra de Substituição Monoalfabética

## 🔐 Descrição do Algoritmo Implementado

### 🚀 Arquitetura do Ataque Premium+
O algoritmo desenvolvido é uma abordagem de criptoanálise avançada para a cifra de substituição monoalfabética. Ele combina múltiplas técnicas de otimização e análise linguística:

### 🏗️ Componentes Principais:
1. **Modelo Estatístico de Linguagem (Português)**
   - ✅ **Bigramas e Trigramas** extraídos do corpus **Floresta (NLTK)**.
   - ✅ Suavização de Laplace.

2. **Validação Morfológica**
   - ✅ Verificação de presença de palavras no texto decifrado usando o corpus **Floresta**.

3. **Pattern Matching Linguístico**
   - ✅ Checagem de palavras comuns, prefixos e sufixos (`que`, `para`, `ção`, `ista`, `pre`, etc.).

4. **Mecanismos de Busca e Otimização**
   - 🔥 **Algoritmo Genético**
   - 🔥 **Simulated Annealing (SA)**
   - 🔥 **Hill Climbing Finalizador**

---

## 🎯 Métrica de Avaliação (Fitness Function)

\`\`\`
score total = score n-gramas + α * score palavras + β * score padrões
\`\`\`

- ✅ **N-gramas:** Avalia fluidez estatística do texto.
- ✅ **Palavras:** Verifica ocorrência de palavras válidas.
- ✅ **Padrões:** Checa presença de padrões linguísticos.

---

## 🚧 Motivos Matemáticos para o Fracasso na Descriptografia Completa

### 📏 Tamanho do Texto:
- ✅ O texto possui **120 caracteres**.

### 🔍 Desafio Matemático:
- A cifra possui:

\`\`\`
26! ≈ 4 x 10^26
\`\`\`

- Espaço de busca colossal.

### 📉 Informação Estatística Insuficiente:
- Modelos de n-gramas precisam de recorrência estatística, o que não acontece em textos tão curtos.

---

## 🔒 Causas Técnicas Detalhadas

| Fator                         | Impacto                                    |
|-------------------------------|---------------------------------------------|
| **Tamanho do texto (120)**     | Insuficiente para garantir convergência estatística. |
| **Espaço de busca (26!)**      | Impraticável para força bruta.             |
| **Entropia linguística baixa** | Bigramas e trigramas são subamostrados.    |
| **Soluções múltiplas**         | Muitas chaves geram textos plausíveis, mas incorretos. |
| **Falta de redundância**       | A língua não se manifesta estatisticamente em textos curtos. |

---

## ✅ Resultados Observados

- O texto decifrado tem:
  - ✅ Alta coerência linguística.
  - ❌ Não corresponde exatamente ao texto aberto.

---

## 💡 Validação Científica

Documentado em:

- *"Cryptanalysis"* — Helen Fouché Gaines.
- *"The Codebreakers"* — David Kahn.

---
