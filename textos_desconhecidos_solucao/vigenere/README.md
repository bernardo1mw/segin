
# Descrição Detalhada do Código de Quebra de Cifra de Vigenère

## 📜 Descrição Geral

Este código implementa um ataque avançado à cifra de **Vigenère**, otimizado para o idioma **português** e utiliza múltiplas heurísticas baseadas em:

- Frequência de letras;
- Frequência de bigramas e trigramas;
- Validação de palavras usando o corpus Floresta do NLTK.

O ataque é robusto, funcionando bem mesmo quando o texto cifrado é curto e a chave é longa.

---

## 🔧 Etapas do Algoritmo

### 1️⃣ **Construção de Modelos Estatísticos**

- Extrai palavras do corpus **Floresta** (`nltk.corpus.floresta`).
- Remove acentos e filtra apenas palavras com 4 ou mais letras.
- Constrói modelos de:
  - Frequência de letras;
  - Frequência de **bigramas** (pares de letras);
  - Frequência de **trigramas** (trios de letras).

Estes modelos são usados para calcular a plausibilidade de textos decifrados.

---

### 2️⃣ **Funções Principais**

#### 🔡 `decifrar_vigenere(texto, chave)`
Decifra um texto cifrado pela cifra de Vigenère usando uma chave.

#### 📊 `pontuacao_texto(txt)`
Calcula um score do texto baseado em:
- Log-probabilidade de bigramas e trigramas;
- Quantidade de palavras reais encontradas no texto.

Score maior significa maior plausibilidade linguística.

#### 🔍 `melhor_deslocamento(fatia)`
Determina o melhor deslocamento para uma fatia do texto, maximizando a frequência de letras no português.

#### 🚀 `hill_climb(init_key, texto, max_no_improve=500)`
Faz uma busca gulosa (hill climbing) tentando melhorar a chave inicial, mudando uma letra de cada vez.

#### 🔥 `refinar_chave_proxima(chave_base, texto_cifrado, max_iter_sem_melhora=10000)`
Faz um refinamento estocástico mais intenso na chave, buscando escapar de máximos locais.

#### 🛠️ `refinar_posicoes(chave_base, texto, posicoes)`
Faz uma busca exaustiva nas posições da chave especificadas, testando todas as combinações possíveis dessas posições.

---

### 3️⃣ **Pipeline Completo - `decifrar_automatico()`**

1. **Estimativa Inicial da Chave**
   - Por análise de frequência nas fatias.

2. **Busca Local com Vários Reinícios (Hill Climb)**
   - Executa múltiplos hill climbs a partir de diferentes chaves aleatórias.

3. **Refinamento Estocástico Global**
   - Busca melhorias aplicando pequenas mutações na chave.

4. **Refinamento Local em Janelas de 3 Posições**
   - Aplica busca exaustiva sobre pequenos grupos de letras da chave para refinamento final.

---

## 🧠 **Heurística de Pontuação**

- **Bigramas:** log-probabilidade simples.
- **Trigramas:** peso dobrado na pontuação.
- **Palavras:** cada palavra reconhecida no dicionário recebe um bônus alto (peso 7).

Isso garante que textos bem formados em português têm score muito mais alto.

---

## 🚀 Parâmetros

- O tamanho da chave (**K**) é definido manualmente.
- Número de reinícios no hill climbing é proporcional a `K`.

---

## 📈 Saídas

- A chave mais provável encontrada.
- O texto decifrado.
- A pontuação final do texto.

---
