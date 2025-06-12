import numpy as np
from sympy import Matrix
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm
import nltk
from nltk.corpus import floresta

# Se ainda não baixou o corpus Floresta, descomente a linha abaixo:
nltk.download('floresta')

MOD = 26

# Frequências aproximadas de letras em português sem acento
PORT_FREQ = {
    'a': 0.1221, 'e': 0.1319, 'o': 0.1022, 's': 0.0735, 'r': 0.0673,
    'i': 0.0618, 'n': 0.0470, 'm': 0.0430, 'u': 0.0393, 't': 0.0387,
    'd': 0.0334, 'c': 0.0272, 'l': 0.0270, 'p': 0.0250, 'v': 0.0153,
    'q': 0.0120, 'b': 0.0123, 'f': 0.0109, 'g': 0.0102, 'h': 0.0078,
    'j': 0.0030, 'z': 0.0025, 'x': 0.0016, 'k': 0.0003, 'w': 0.0001,
    'y': 0.0001
}

PORT_WORDS = set(floresta.words())
# Conjunto de palavras comuns em português (pode expandir com dicionário melhor)
#with open("floresta_words.txt", "r", encoding="utf-8") as f:
#    PORT_WORDS = set(line.strip() for line in f if len(line.strip()) > 2)

def text_to_numbers(text):
    return [ord(c) - ord('a') for c in text]

def numbers_to_text(nums):
    return ''.join(chr((n % MOD) + ord('a')) for n in nums)

def modinv_matrix(mat):
    try:
        inv = Matrix(mat).inv_mod(MOD)
        return np.array(inv).astype(int)
    except:
        return None

def chi_squared_score(text):
    N = len(text)
    if N == 0:
        return float('inf')
    cnt = Counter(text)
    chi2 = 0.0
    for letter, expected in PORT_FREQ.items():
        observed = cnt.get(letter, 0)
        exp_count = N * expected
        if exp_count > 0:
            chi2 += ((observed - exp_count)**2) / exp_count
    return chi2

def segmentar_texto(texto, dicionario, max_len=12):
    i = 0
    palavras = []
    texto = texto.lower()
    while i < len(texto):
        for j in range(min(len(texto), i + max_len), i, -1):
            palavra = texto[i:j]
            if palavra in dicionario:
                palavras.append(palavra)
                i = j
                break
        else:
            i += 1
    return palavras

def word_coverage_ratio(texto, dicionario, min_len=3, max_len=12):
    tokens = segmentar_texto(texto, dicionario, max_len=max_len)
    covered = [False]*len(texto)
    for token in tokens:
        start = texto.find(token)
        if start >= 0:
            for i in range(start, start+len(token)):
                covered[i] = True
    return sum(covered) / len(texto)

def heuristica_rapida(texto):
    # Evita textos com excesso de letras repetidas consecutivas
    for ch in set(texto):
        if texto.count(ch * 3) > 0:
            return False
    return True

def gerar_blocos(nums, tamanho_bloco=3):
    if len(nums) % tamanho_bloco != 0:
        nums += [0] * (tamanho_bloco - (len(nums) % tamanho_bloco))
    blocos = [nums[i:i + tamanho_bloco] for i in range(0, len(nums), tamanho_bloco)]
    return blocos

def valid_invertibles(mod=MOD):
    return [i for i in range(1, mod) if np.gcd(i, mod) == 1]

def decrypt_blocks(blocks, key_inv):
    arr_blocks = np.array(blocks).T  # shape (3, n_blocks)
    decrypted = (key_inv @ arr_blocks) % MOD
    return decrypted.T.flatten().astype(int)

# --- Fase 1: Encontrar candidatos para c (último valor diagonal) ---
def encontrar_candidatos_c(blocks, top_n=10):
    candidatos = []
    invs = valid_invertibles()
    for c in invs:
        inv_c = pow(c, -1, MOD)
        # extrair o terceiro elemento do bloco e aplicar inv_c
        p3 = [(inv_c * block[2]) % MOD for block in blocks]
        texto_p3 = numbers_to_text(p3)
        score_c = chi_squared_score(texto_p3)
        candidatos.append((c, score_c))
    candidatos.sort(key=lambda x: x[1])
    return candidatos[:top_n]

# --- Fase 2: Para cada c, encontrar candidatos para a,b (linha 2) ---
def encontrar_candidatos_ab(blocks, c, top_n=20):
    candidatos = []
    invs = valid_invertibles()
    inv_c = pow(c, -1, MOD)
    for a in invs:
        inv_a = pow(a, -1, MOD)
        for b in range(MOD):
            # Segunda linha de K^{-1} é: [0, 1/a, -b/(a*c)]
            # Em mod 26: [0, inv_a, (-b * inv_a * inv_c) mod 26]
            inv_b = (-b * inv_a * inv_c) % MOD
            # Calcular p2 para todos os blocos
            p2 = []
            for block in blocks:
                val = (inv_a * block[1] + inv_b * block[2]) % MOD
                p2.append(val)
            texto_p2 = numbers_to_text(p2)
            score_ab = chi_squared_score(texto_p2)
            candidatos.append((a, b, score_ab))
    candidatos.sort(key=lambda x: x[2])
    return candidatos[:top_n]

# --- Fase 3: Para cada (a,b,c), encontrar candidatos para primeira linha (x,y,z) ---

def avaliar_klinha(args):
    a, b, c, score_ab_c, x, y, z, linha2, linha3, blocks = args
    key_inv = np.array([
        [x, y, z],
        linha2,
        linha3
    ])
    key = modinv_matrix(key_inv)
    if key is None:
        print("Chave inválida")
        return None
    try:
        plain_nums = decrypt_blocks(blocks, key_inv)
        plaintext = numbers_to_text(plain_nums)
        CHAVE_REAL = np.array([
            [15, 25, 5],
            [ 0, 25, 11],
            [ 0,  0,  3]
        ])
#        if not heuristica_rapida(plaintext):
#            print("Não passou na heuristica")
#            return None
        chi2 = chi_squared_score(plaintext)
        word_cov_score = word_coverage_ratio(plaintext, PORT_WORDS)
        #combined = (1 / (chi2 + 1e-5)) * word_score
        #combined = normalize(word_score) - normalize(chi2)
        #print(f"retornando: {plaintext} {chi2} {word_cov_score}")
        if key is not None and np.array_equal(key, CHAVE_REAL):
          print(f"\nTexto real: {plaintext}")
          print("→ ACHOU com word score:", word_cov_score)
        return (plaintext, chi2, word_cov_score, key.tolist())
    except Exception as e:
        print("Erro ao avaliar klinha: ", e)
        return None

def normalize(val, min_val, max_val):
    if max_val == min_val:
        return 0.0  # evita divisão por zero
    return (val - min_val) / (max_val - min_val)

resultados_tpl1 = []
resultados_tpl2 = []
def testar_primeira_linha(candidatos_ab_c, blocks, top_n=5):
    global resultados_tpl1
    resultados = []
    invs = valid_invertibles()
    tarefas = []

    print("[*] Preparando tarefas para paralelismo...")
    for (a, b, c, score_ab_c) in candidatos_ab_c:
        inv_c = pow(c, -1, MOD)
        inv_a = pow(a, -1, MOD)
        linha2 = [0, inv_a, (-b * inv_a * inv_c) % MOD]
        linha3 = [0, 0, inv_c]

        for x in invs:
            for y in range(MOD):
                for z in invs:
                    tarefas.append((a, b, c, score_ab_c, x, y, z, linha2, linha3, blocks))

    print(f"[*] Total de combinações a testar: {len(tarefas)}")

    with ProcessPoolExecutor() as executor:
        all_results = list(tqdm(
            executor.map(avaliar_klinha, tarefas),
            total=len(tarefas),
            desc="Testando primeira linha"
        ))


    # Filtrar Nones
    print(f"Recebidos {len(all_results)} resultados\nIniciando filtragem.")
    resultados_tpl1 = all_results
    #resultados = [r for r in all_results if r is not None]
    # Extrair valores de chi2 e word_score
    # chi2_vals = [r[1] for r in resultados]
    # wscore_vals = [r[2] for r in resultados]

    # chi2_min, chi2_max = min(chi2_vals), max(chi2_vals)
    # wscore_min, wscore_max = min(wscore_vals), max(wscore_vals)

    # # Calcular score normalizado e armazenar como novo campo
    # resultados_com_score = []
    # for r in resultados:
    #     chi2_norm = normalize(r[1], chi2_min, chi2_max)
    #     wscore_norm = normalize(r[2], wscore_min, wscore_max)
    #     combined_score = wscore_norm - chi2_norm  # ou qualquer outra fórmula
    #     resultados_com_score.append((r[0], combined_score, r[1], r[2], r[3]))

    # # Ordenar pelo score normalizado (do maior para o menor)
    # resultados_com_score.sort(key=lambda x: -x[1])

    # resultados_tpl2 = resultados_com_score
    # Obter os top N
    #return resultados_com_score[:top_n]
    print(all_results[:5])
    final=all_results.sort(key=lambda x: -x[2])
    return final

# Função principal orquestradora
candidatos_ab_c = []
resultados_finais = []
def ataque_hill_otimizado(ciphertext, max_c=10, max_ab=20, top_k=5):
    print("[+] Convertendo texto para números...")
    nums = text_to_numbers(ciphertext)
    blocks = gerar_blocos(nums)

    print("[+] Encontrando candidatos para c...")
    candidatos_c = encontrar_candidatos_c(blocks, top_n=max_c)
    print(f"    Encontrados {len(candidatos_c)} candidatos para c.")

    candidatos_ab_c = []
    for c, score_c in tqdm(candidatos_c, desc="[*] Avaliando candidatos (a,b) para cada c"):
        ab_candidates = encontrar_candidatos_ab(blocks, c, top_n=max_ab)
        for (a, b, score_ab) in ab_candidates:
            combined_score = score_c + score_ab
            candidatos_ab_c.append((a, b, c, combined_score))
    candidatos_ab_c.sort(key=lambda x: x[3])
    candidatos_ab_c = candidatos_ab_c[:max_c*max_ab]

    print(f"\n[+] Testando primeira linha (x,y,z) para {len(candidatos_ab_c)} candidatos...")
    resultados = testar_primeira_linha(candidatos_ab_c, blocks, top_n=top_k)
    resultados_finais = resultados
    print("[+] Resultados obtidos:")
    for idx, (text, combined, chi2, wscore, key) in enumerate(resultados[:10]):
        print(f"Resultado #{idx+1}")
        print(f"Texto: {text}")
        print(f"Pontuação combinada: {combined:.4f}, Chi-quadrado: {chi2:.2f}, Palavras conhecidas: {wscore:.2f}")
        print(f"Chave inversa (mod 26):\n{np.array(key)}\n")
    return resultados

def testar_chave_hardcoded(ciphertext, chave):
    from sympy import Matrix

    print("[+] Convertendo texto para números...")
    nums = text_to_numbers(ciphertext)
    blocks = gerar_blocos(nums)

    print("[+] Tentando inverter chave fornecida...")
    try:
        inv_key = Matrix(chave).inv_mod(MOD)
        inv_key_np = np.array(inv_key).astype(int)
    except:
        print("Erro: chave não invertível no módulo 26.")
        return

    print("[+] Decriptando texto...")
    plain_nums = decrypt_blocks(blocks, inv_key_np)
    plaintext = numbers_to_text(plain_nums)

    print("[+] Executando heurísticas...")
    if not heuristica_rapida(plaintext):
        print("Rejeitado pela heurística rápida.")
        return

    chi2 = chi_squared_score(plaintext)
    word_cov_score = word_coverage_ratio(plaintext, PORT_WORDS)
#    combined = (1 / (chi2 + 1e-5)) * word_score  # Score combinado
    #resultados_tpl1 = resultados
    # Extrair valores de chi2 e word_score
    chi2_vals = [r[1] for r in resultados_tpl1]
    wscore_vals = [r[2] for r in resultados_tpl1]

    chi2_min, chi2_max = min(chi2_vals), max(chi2_vals)
    wscore_min, wscore_max = min(wscore_vals), max(wscore_vals)

    # Calcular score normalizado e armazenar como novo campo

    chi2_norm = normalize(chi2, chi2_min, chi2_max)
    wscore_norm = normalize(word_cov_score, wscore_min, wscore_max)
    combined_score = wscore_norm - chi2_norm  # ou qualquer outra fórmula

    print("🔍 Resultados:")
    print(f"→ Texto: {plaintext}")
    print(f"→ Chi-quadrado: {chi2:.4f}")
    print(f"→ Combined score: {combined_score:.4f}")
#    print(f"→ Pontuação combinada: {combined:.4f}")
    return (plaintext, word_cov_score)


# Exemplo de uso
if __name__ == "__main__":
    aberto = "vacomospaistoqueiointerfoneumavozfemininaatendeuenaoeraadesahariennedisseumpodesubiroportaoseabriumeolheinoespelhodoelev"
    fechado = "nwgimqvlapjfiwisqquofqmpjfmcoakbxbykrxynaaijnliivnafbzphjqiaifzzjnydjkycwikstjmuioxzfjqchaeamgezeikxdhlgytempdmurqzemgtl"
    chave = np.array([[15, 25, 5], [0, 25, 11], [0, 0, 3]])  # para validar se quiser testar
    #testar_chave_hardcoded(fechado, chave)


    # Use o texto cifrado para recuperar a chave e o texto aberto
    ataque_hill_otimizado(fechado)
