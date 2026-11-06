"""
equations.py - Equações do memorial de cálculo (versão enxuta), em ordem de dependência.

Todas as funções trabalham no SI (m, kg, s, N, Pa).
Códigos de referência:
  PAL  - Palmerio (2017), livrofoguetes.pdf (página impressa = página do PDF)
  GOE  - Goehr (2025), TCC_Luiz_Eduardo_Prince_Goehr.pdf (p. impressa; p. do PDF)
  GRA  - Grant et al. (2016), fall_final_report.pdf (p. impressa; p. do PDF)
  MAG  - Magaldi et al. (2023), análise da fuselagem ... openrocket.pdf (p. do PDF)
  SCH  - Schlichta (2025), TCC.pdf
  BAR  - Norma BAR-2/2020, Nomenclaturas.pdf
  BAW  - Barrowman (1967), Barrowman.pdf (eq. e página do PDF)
  HIB  - Hibbeler, Resistência dos Materiais (livro impresso; anotar a página da sua edição)
  Lista completa das siglas: referencias.py
"""

from math import pi, sqrt, atan


# =============================================================================
# ETAPA 1 - Critério de projeto
# =============================================================================

def tensao_admissivel(sig_lim, FS):
    """Tensão admissível: limite do material dividido pelo fator de segurança.
    sig_lim: tensão limite do material [Pa]; FS: fator de segurança [-]
    Retorna: sig_adm [Pa]
    Ref.: PAL, p. 212 (Tab. 5.4.2)."""
    return sig_lim / FS


def margem_seguranca(sig_lim, FS, sig):
    """Margem de segurança MS = sig_lim / (FS.sig) - 1 (passa se MS >= 0).
    sig_lim: tensão limite [Pa]; FS: fator de segurança [-]; sig: tensão calculada [Pa]
    Retorna: MS [-]
    Ref.: PAL, p. 212 (margem com C, Q e o coeficiente; aqui escrita em tensões)."""
    return sig_lim / (FS * sig) - 1


# =============================================================================
# ETAPA 2 - Geometria do tubo
# =============================================================================

def comprimento_total(L_n, L_c):
    """Comprimento total do foguete (ogiva + tubo).
    L_n: comprimento da ogiva [m]; L_c: comprimento do tubo [m]
    Retorna: L_tot [m]
    Ref.: geometria (não identificada)."""
    return L_n + L_c


def esbeltez_foguete(L_tot, d):
    """Esbeltez L/d (corpo rígido se < 20).
    L_tot: comprimento total [m]; d: diâmetro externo [m]
    Retorna: L/d [-]
    Ref.: PAL, p. 180."""
    return L_tot / d


def diametro_interno(d, t):
    """Diâmetro interno do tubo.
    d: diâmetro externo [m]; t: espessura de parede [m]
    Retorna: D_i [m]
    Ref.: geometria (não identificada)."""
    return d - 2 * t


def area_circulo(D):
    """Área de um círculo de diâmetro D (usada para A_ref, A_int e área do motor).
    D: diâmetro [m]
    Retorna: área [m²]
    Ref.: geometria (não identificada)."""
    return pi * D**2 / 4


def area_coroa(d, D_i):
    """Área resistente da coroa circular (parede do tubo).
    d: diâmetro externo [m]; D_i: diâmetro interno [m]
    Retorna: A [m²]
    Ref.: HIB (propriedades geométricas de áreas); usada em MAG, eq. 5."""
    return pi * (d**2 - D_i**2) / 4


def inercia_coroa(d, D_i):
    """Momento de inércia de área da coroa circular.
    d: diâmetro externo [m]; D_i: diâmetro interno [m]
    Retorna: I [m^4]
    Ref.: HIB (propriedades geométricas de áreas: I = pi.d^4/64); usada em MAG, eq. 6."""
    return pi * (d**4 - D_i**4) / 64


def fibra_extrema(d):
    """Distância do eixo à fibra mais afastada.
    d: diâmetro externo [m]
    Retorna: c [m]
    Ref.: HIB (cap. 6, fórmula da flexão)."""
    return d / 2


def raio_medio(d, t):
    """Raio médio da parede do tubo.
    d: diâmetro externo [m]; t: espessura [m]
    Retorna: R_m [m]
    Ref.: geometria; usado em PAL, p. 197."""
    return (d - t) / 2


def relacao_raio_espessura(R, t):
    """Relação R/t (parede fina se > 10).
    R: raio médio [m]; t: espessura [m]
    Retorna: R/t [-]
    Ref.: PAL, p. 197 (cilindro de parede fina)."""
    return R / t


# =============================================================================
# ETAPA 3 - Massas e CG
# =============================================================================

def massa_total(massas):
    """Massa total = soma das massas.
    massas: lista de massas [kg]
    Retorna: M_0 [kg]
    Ref.: SCH, eq. 3 (p. 23)."""
    return sum(massas)


def centro_gravidade(massas, posicoes):
    """CG = soma(m.x) / soma(m), x medido da ponta da ogiva.
    massas: lista [kg]; posicoes: lista de CGs [m]
    Retorna: x_cg [m]
    Ref.: SCH, eq. 3 (p. 23); BAR, p. 2."""
    return sum(m * x for m, x in zip(massas, posicoes)) / sum(massas)


def massa_tubo_trecho(rho, A, x_fim, x_ini):
    """Massa de um trecho do tubo entre x_ini e x_fim (volume x densidade).
    rho: massa específica [kg/m³]; A: área da parede [m²]; x_fim, x_ini: posições [m]
    Retorna: m [kg]
    Ref.: definição de massa específica m = rho.V (não identificada na bibliografia)."""
    return rho * A * (x_fim - x_ini)


def massa_frente(m_ogiva, m_tubo_frente, m_ant_baia, m_avi, m_rec):
    """Massa de tudo que está à frente do anteparo de empuxo (o tubo empurra essa massa).
    m_ogiva, m_tubo_frente, m_ant_baia, m_avi, m_rec: massas [kg]
    Retorna: M_frente [kg]
    Ref.: PAL, p. 247 (esforço normal = efeito de tudo acima da seção)."""
    return m_ogiva + m_tubo_frente + m_ant_baia + m_avi + m_rec


def massa_propelente(m_cheio, m_vazio):
    """Massa de propelente = motor cheio - motor vazio.
    m_cheio, m_vazio: massas do motor [kg]
    Retorna: m_p [kg]
    Ref.: catálogo do motor (não identificada na bibliografia)."""
    return m_cheio - m_vazio


def massa_apos_queima(M_0, m_p):
    """Massa do foguete depois da queima.
    M_0: massa de decolagem [kg]; m_p: massa de propelente [kg]
    Retorna: M_q [kg]
    Ref.: GRA, eq. 3 (p. 8; PDF 18) - massa fixa + propelente."""
    return M_0 - m_p


# =============================================================================
# ETAPA 4 - Atmosfera na altitude de V_max
# =============================================================================

def temperatura_altitude(H):
    """Temperatura do ar na altitude H.
    H: altitude [m]
    Retorna: T_c [°C]
    Ref.: GOE, eq. 11 (p. 30; PDF 31)."""
    return 15 - 0.0065 * H


def pressao_altitude(T_c):
    """Pressão do ar na temperatura T_c (resultado convertido de kPa para Pa).
    T_c: temperatura [°C]
    Retorna: p [Pa]
    Ref.: GOE, eq. 10 (p. 30; PDF 31)."""
    return 101.325 * ((T_c + 273.16) / 288.16) ** 5.256 * 1000


def velocidade_som(T_c):
    """Velocidade do som.
    T_c: temperatura [°C]
    Retorna: a [m/s]
    Ref.: GOE, eq. 12 (p. 31; PDF 32)."""
    return 20.05 * sqrt(273.16 + T_c)


def densidade_ar(p, R, T_c):
    """Densidade do ar pela equação do gás perfeito.
    p: pressão [Pa]; R: constante do ar [J/(kg.K)]; T_c: temperatura [°C]
    Retorna: rho [kg/m³]
    Ref.: PAL, p. 45 (pressão estática, gás perfeito)."""
    return p / (R * (T_c + 273.15))


# =============================================================================
# ETAPA 5 - Cargas LC1, LC2, LC3 e LC5
# =============================================================================

def fator_carga_axial(T, D, M):
    """Fator de carga axial (a_x + g) = (T - D) / M.
    T: empuxo [N]; D: arrasto [N]; M: massa [kg]
    Retorna: a_x + g [m/s²]
    Ref.: GRA, eqs. 1-2 (p. 8; PDF 18)."""
    return (T - D) / M


def compressao_tubo(D, M_frente, axg):
    """Compressão no tubo logo à frente do anteparo de empuxo: N = D + M_frente.(a_x + g).
    D: arrasto à frente da seção [N] (0 no LC1); M_frente: massa à frente [kg]; axg: a_x + g [m/s²]
    Retorna: N_ax [N]
    Ref.: PAL, p. 247-248; MAG, eq. 3 (PDF 3)."""
    return D + M_frente * axg


def pressao_dinamica(rho, V):
    """Pressão dinâmica Q = 1/2.rho.V².
    rho: densidade do ar [kg/m³]; V: velocidade [m/s]
    Retorna: Q [Pa]
    Ref.: PAL, p. 45."""
    return 0.5 * rho * V**2


def angulo_ataque(V_raj, V):
    """Ângulo de ataque criado pela rajada lateral.
    V_raj: rajada [m/s]; V: velocidade do foguete [m/s]
    Retorna: alpha [rad]
    Ref.: PAL, p. 46 e p. 246."""
    return atan(V_raj / V)


def forca_normal(Q, A_ref, C_Na, alpha):
    """Força normal N = Q.A_ref.C_Nα.alpha.
    Q: pressão dinâmica [Pa]; A_ref: área de referência [m²]; C_Na: coeficiente [1/rad]; alpha: [rad]
    Retorna: N [N]
    Ref.: PAL, p. 183."""
    return Q * A_ref * C_Na * alpha


def massa_instante(M_0, m_p, t, t_q):
    """Massa no instante t, supondo queima a taxa constante.
    M_0: massa de decolagem [kg]; m_p: propelente [kg]; t: instante [s]; t_q: tempo de queima [s]
    Retorna: M [kg]
    Ref.: hipótese de taxa constante (não identificada); GRA, eq. 3 separa massa fixa e propelente."""
    return M_0 - m_p * min(1.0, t / t_q)


def momento_fletor_LC2(N_n, x_cg, X_n):
    """Momento fletor no tubo na seção do CG: M = N_n.(x_cg - X_n), sem descontar a inércia.
    N_n: força normal da ogiva [N]; x_cg: CG [m]; X_n: CP da ogiva [m]
    Retorna: M [N.m]
    Ref.: aplicação de M_F = C.b de PAL, p. 247 (forma simplificada não identificada na bibliografia)."""
    return N_n * (x_cg - X_n)


def forca_ruptura_pinos(n_p, tau_p, d_p):
    """Força que rompe todos os pinos por cisalhamento.
    n_p: número de pinos [-]; tau_p: resistência ao cisalhamento [Pa]; d_p: diâmetro [m]
    Retorna: F_p,u [N]
    Ref.: HIB (cap. 1, tensão de cisalhamento média tau = V/A)."""
    return n_p * tau_p * pi * d_p**2 / 4


def pressao_ejecao(FS_ej, F_pu, A_int):
    """Pressão de ejeção de projeto (força de projeto dividida pela área interna).
    FS_ej: fator de separação [-]; F_pu: ruptura dos pinos [N]; A_int: área interna [m²]
    Retorna: p_ej [Pa]
    Ref.: PAL, p. 197 (F = p.A)."""
    return FS_ej * F_pu / A_int


def forca_separacao(m_n, D, M_q):
    """Tendência de separação da ogiva depois da queima (arrasto da ogiva desprezado).
    m_n: massa da ogiva [kg]; D: arrasto [N]; M_q: massa após a queima [kg]
    Retorna: F_sep [N]
    Ref.: dedução com F = m.a de GRA, eq. 2 (forma final não identificada na bibliografia)."""
    return m_n * D / M_q


# =============================================================================
# ETAPA 6 - Tubo de PVC
# =============================================================================

def tensao_flexao_composta(N, A, M, c, I):
    """Tensão normal máxima com força axial e flexão: sigma = N/A + M.c/I.
    N: força axial [N]; A: área [m²]; M: momento [N.m]; c: fibra extrema [m]; I: inércia [m^4]
    Retorna: sigma [Pa]
    Ref.: MAG, eqs. 5-6 (PDF 4)."""
    return N / A + M * c / I


def tensao_normal(F, A):
    """Tensão normal média sigma = F/A.
    F: força [N]; A: área [m²]
    Retorna: sigma [Pa]
    Ref.: GRA, eq. 16 (p. 38; PDF 48); MAG, eq. 5."""
    return F / A


def raio_giracao(I, A):
    """Raio de giração k = raiz(I/A).
    I: inércia [m^4]; A: área [m²]
    Retorna: k [m]
    Ref.: GRA, eq. 10 (p. 13; PDF 23)."""
    return sqrt(I / A)


def indice_esbeltez(L, k):
    """Índice de esbeltez da coluna S_r = L/k.
    L: comprimento [m]; k: raio de giração [m]
    Retorna: S_r [-]
    Ref.: GRA, eq. 9 (p. 13; PDF 23)."""
    return L / k


def esbeltez_transicao(E, S_yc):
    """Esbeltez a partir da qual vale Euler: (S_r)_D = pi.raiz(2E/S_yc).
    E: módulo [Pa]; S_yc: escoamento em compressão [Pa]
    Retorna: (S_r)_D [-]
    Ref.: GRA, eq. 12 (p. 13; PDF 23)."""
    return pi * sqrt(2 * E / S_yc)


def carga_critica_euler(E, A, S_r):
    """Carga crítica de flambagem de Euler P_cr = pi².E.A / S_r².
    E: módulo [Pa]; A: área [m²]; S_r: índice de esbeltez [-]
    Retorna: P_cr [N]
    Ref.: GRA, eq. 11 (p. 13; PDF 23)."""
    return pi**2 * E * A / S_r**2


def razao_cargas(F_resistente, F_aplicada):
    """Razão entre uma força resistente e a força aplicada (FS de coluna, retenção da ogiva).
    F_resistente: [N]; F_aplicada: [N]
    Retorna: razão [-]
    Ref.: definição de fator de segurança, PAL, p. 212."""
    return F_resistente / F_aplicada


def tensao_anel(p, R, t):
    """Tensão circunferencial (de anel) em cilindro de parede fina sob pressão interna.
    p: pressão [Pa]; R: raio médio [m]; t: espessura [m]
    Retorna: sigma_2 [Pa]
    Ref.: PAL, p. 197."""
    return p * R / t


def forca_por_elemento(F, n):
    """Divide uma força igualmente entre n elementos (pinos).
    F: força total [N]; n: número de elementos [-]
    Retorna: força por elemento [N]
    Ref.: equilíbrio por simetria (não identificada)."""
    return F / n


def tensao_esmagamento(F, d, t):
    """Tensão de esmagamento no furo sigma = F/(d.t).
    F: força no pino [N]; d: diâmetro do furo [m]; t: espessura da parede [m]
    Retorna: sigma_br [Pa]
    Ref.: HIB (cap. 1, tensão de esmagamento média)."""
    return F / (d * t)


def tensao_viga_distribuida(p, a, t):
    """Tensão máxima numa placa circular tratada como viga biapoiada com carga distribuída.
    Viga de vão 2a e largura 2a, carga total p.pi.a²: M = w.L²/8 e sigma = 6M/(b.t²).
    p: pressão [Pa]; a: raio da placa [m]; t: espessura [m]
    Retorna: sigma [Pa]
    Ref.: HIB (viga biapoiada: M = wL²/8; flexão: sigma = M.c/I); modelo de viga = hipótese
    conservadora (não identificada na bibliografia)."""
    return 3 * pi / 4 * p * a**2 / t**2


def tensao_viga_concentrada(F, t):
    """Tensão máxima numa placa circular tratada como viga biapoiada com carga no centro.
    Viga de vão 2a e largura 2a: M = F.L/4 e sigma = 6M/(b.t²) = 1,5.F/t² (não depende de a).
    F: força no centro [N]; t: espessura [m]
    Retorna: sigma [Pa]
    Ref.: HIB (viga biapoiada: M = PL/4; flexão: sigma = M.c/I); modelo de viga = hipótese
    conservadora (não identificada na bibliografia)."""
    return 1.5 * F / t**2


# =============================================================================
# ETAPA 7 - Ogiva e junção
# =============================================================================

def raio_livre_fundo(D_o, t_o):
    """Raio livre do fundo do ombro.
    D_o: diâmetro externo do ombro [m]; t_o: parede do ombro [m]
    Retorna: a_f [m]
    Ref.: geometria (não identificada)."""
    return (D_o - 2 * t_o) / 2


# =============================================================================
# ETAPA 8 - Aletas
# =============================================================================

def area_aleta(C_r, C_t, s):
    """Área de uma aleta trapezoidal.
    C_r, C_t: cordas de raiz e ponta [m]; s: envergadura [m]
    Retorna: S [m²]
    Ref.: GOE, eq. 3 (p. 25; PDF 26)."""
    return (C_r + C_t) * s / 2


def razao_aspecto(s, S):
    """Razão de aspecto AR = s²/S.
    s: envergadura [m]; S: área [m²]
    Retorna: AR [-]
    Ref.: GOE, eq. 3 (p. 25; PDF 26)."""
    return s**2 / S


def afilamento(C_t, C_r):
    """Afilamento lambda = C_t/C_r.
    C_t, C_r: cordas [m]
    Retorna: lambda [-]
    Ref.: GOE, eq. 4 (p. 25; PDF 26)."""
    return C_t / C_r


def centroide_corda(C_r, C_t, x_r):
    """Posição do centroide da aleta na direção da corda (a partir do bordo de ataque da raiz).
    C_r, C_t: cordas [m]; x_r: enflechamento [m]
    Retorna: C_x [m]
    Ref.: GOE, eq. 9 (p. 30; PDF 31)."""
    return (2 * C_t * x_r + C_t**2 + x_r * C_r + C_t * C_r + C_r**2) / (3 * (C_t + C_r))


def parametro_epsilon(C_x, C_r):
    """Distância do centroide ao ponto de 1/4 da corda, em fração de C_r.
    C_x: centroide [m]; C_r: corda da raiz [m]
    Retorna: epsilon [-]
    Ref.: GOE, eq. 8 (p. 30; PDF 31)."""
    return C_x / C_r - 0.25


def constante_DN(epsilon, kappa, p_0):
    """Constante do denominador da equação de flutter (correção de Bennett).
    epsilon: [-]; kappa: razão de calores específicos [-]; p_0: pressão ao nível do mar [Pa]
    Retorna: DN [Pa]
    Ref.: GOE, eq. 6 (p. 28; PDF 29)."""
    return 24 * epsilon * kappa * p_0 / pi


def velocidade_flutter(a, G, DN, AR, t, C_r, lam, p, p_0):
    """Velocidade de início de flutter (Martin com DN de Bennett).
    a: som [m/s]; G: cisalhamento [Pa]; DN: [Pa]; AR, lam: [-]; t: espessura [m];
    C_r: corda da raiz [m]; p: pressão em V_max [Pa]; p_0: pressão ao nível do mar [Pa]
    Retorna: V_f [m/s]
    Ref.: GOE, eq. 7 (p. 29; PDF 30)."""
    denominador = DN * AR**3 / ((t / C_r) ** 3 * (AR + 2)) * (lam + 1) / 2 * (p / p_0)
    return a * sqrt(G / denominador)


def velocidade_flutter_minima(FS_V, V_max):
    """Velocidade de flutter mínima exigida.
    FS_V: fator [-]; V_max: velocidade máxima [m/s]
    Retorna: V_f,min [m/s]
    Ref.: GOE, p. 31 (PDF 32) - fator V_f/V_max."""
    return FS_V * V_max


# =============================================================================
# ETAPA 9 - Compartimento do motor
# =============================================================================

def tensao_colagem(F, D, h):
    """Cisalhamento médio numa faixa colada cilíndrica tau = F/(pi.D.h) (colagem do anteparo).
    F: força [N]; D: diâmetro da faixa [m]; h: altura colada [m]
    Retorna: tau [Pa]
    Ref.: HIB (cap. 1, tensão de cisalhamento média tau = V/A)."""
    return F / (pi * D * h)


# =============================================================================
# ETAPA 10 - Espessuras mínimas (inversão das equações das etapas 6 a 9)
# =============================================================================

def t_min_flexao_composta(FS, sig_lim, N, M, R):
    """Espessura mínima do tubo por flexão composta (parede fina: A = 2.pi.R.t, I = pi.R³.t).
    FS: [-]; sig_lim: [Pa]; N: força axial [N]; M: momento [N.m]; R: raio médio [m]
    Retorna: t_min [m]
    Ref.: inversão de MAG, eqs. 5-6 (dedução)."""
    return FS / sig_lim * (N / (2 * pi * R) + M / (pi * R**2))


def t_min_anel(FS, p, R, sig_lim):
    """Espessura mínima do tubo pela pressão de ejeção.
    FS: [-]; p: pressão [Pa]; R: raio médio [m]; sig_lim: [Pa]
    Retorna: t_min [m]
    Ref.: inversão de PAL, p. 197 (dedução)."""
    return FS * p * R / sig_lim


def t_min_euler(FS, N, L, E, R):
    """Espessura mínima do tubo pela flambagem de Euler (parede fina: k² = R²/2).
    FS: [-]; N: força axial [N]; L: comprimento [m]; E: módulo [Pa]; R: raio médio [m]
    Retorna: t_min [m]
    Ref.: inversão de GRA, eqs. 9-11 (dedução)."""
    return FS * N * L**2 / (pi**3 * E * R**3)


def t_min_esmagamento_pino(tau_p, d_p, sig_adm):
    """Espessura mínima da parede para o furo do pino não esmagar.
    tau_p: cisalhamento do pino [Pa]; d_p: diâmetro [m]; sig_adm: tensão admissível [Pa]
    Retorna: t_min [m]
    Ref.: inversão de sigma = F/(d.t), HIB (dedução)."""
    return pi * tau_p * d_p / (4 * sig_adm)


def t_min_viga_distribuida(a, FS, p, sig_lim):
    """Espessura mínima da placa (modelo de viga) com carga distribuída.
    a: raio [m]; FS: [-]; p: pressão [Pa]; sig_lim: [Pa]
    Retorna: t_min [m]
    Ref.: inversão de tensao_viga_distribuida (dedução)."""
    return a * sqrt(3 * pi / 4 * FS * p / sig_lim)


def t_min_viga_concentrada(FS, F, sig_lim):
    """Espessura mínima da placa (modelo de viga) com carga concentrada no centro.
    FS: [-]; F: força [N]; sig_lim: [Pa]
    Retorna: t_min [m]
    Ref.: inversão de tensao_viga_concentrada (dedução)."""
    return sqrt(1.5 * FS * F / sig_lim)


def t_min_flutter(C_r, DN, AR, lam, p, p_0, V, G, a):
    """Espessura mínima da aleta para V_f = V (V = FS_V.V_max).
    C_r: corda [m]; DN: [Pa]; AR, lam: [-]; p, p_0: [Pa]; V: [m/s]; G: [Pa]; a: [m/s]
    Retorna: t_min [m]
    Ref.: inversão de GOE, eq. 7 (dedução)."""
    return C_r * (DN * AR**3 / (AR + 2) * (lam + 1) / 2 * (p / p_0) * V**2 / (G * a**2)) ** (1 / 3)


def espessura_minima(*criterios):
    """Espessura mínima da peça = maior valor entre os critérios.
    criterios: espessuras mínimas de cada critério [m]
    Retorna: t_min [m]
    Ref.: PAL, p. 212 (FS aplicado em todos os critérios)."""
    return max(criterios)


def folga(valor_adotado, valor_minimo):
    """Folga = adotado / mínimo (passa se > 1).
    valor_adotado, valor_minimo: mesma unidade
    Retorna: folga [-]
    Ref.: definição (não identificada)."""
    return valor_adotado / valor_minimo
