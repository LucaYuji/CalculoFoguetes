"""
inputs.py - Variáveis de entrada do programa.

Os valores são lidos do arquivo inputs.csv (colunas: Variável, Valor, Unidade, Descrição).
O programa usa só as colunas Variável e Valor; Unidade e Descrição são para consulta.
Para mudar um valor, edite apenas o CSV.
Todas as variáveis estão no SI (m, kg, s, N, Pa).

Códigos de referência usados nos comentários:
  PAL  - Palmerio (2017), livrofoguetes.pdf
  GOE  - Goehr (2025), TCC_Luiz_Eduardo_Prince_Goehr.pdf (p. impressa / p. do PDF)
  MED  - Medeiros e Wiebeck (2013), pvc.pdf
  BAW  - Barrowman (1967), Barrowman.pdf (eq. e página do PDF)
  OR   - Modelo/simulação OpenRocket da equipe, 28/10/2026 (dado, não é referência de equação)
  CAT  - Catálogo do fabricante (dado de produto, não é referência de equação)
  Lista completa das siglas: referencias.py
"""

import csv
import os

_CAMINHO_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inputs.csv")


def _ler_csv(caminho):
    """Lê o CSV e devolve um dicionário {nome_da_variável: valor} (colunas 1 e 2)."""
    valores = {}
    with open(caminho, newline="", encoding="utf-8") as arquivo:
        leitor = csv.reader(arquivo)
        next(leitor)  # pula o cabeçalho (Variável, Valor, Unidade, Descrição)
        for linha in leitor:
            if linha and linha[0].strip():
                valores[linha[0].strip()] = float(linha[1])
    return valores


_v = _ler_csv(_CAMINHO_CSV)

# ---------------------------------------------------------------------------
# Critérios de projeto
# ---------------------------------------------------------------------------
FS = _v["FS"]                  # FS - fator de segurança estrutural [-] - PAL, Tab. 5.4.2, p. 212 (1,5 = "outras cargas perigosas"; adotado pelo grupo)
FS_ej = _v["FS_ej"]            # FS_ej - fator sobre a ruptura dos pinos na ejeção [-] - critério do projeto (referência não identificada)
FS_V = _v["FS_V"]              # FS_V - fator mínimo sobre a velocidade de flutter [-] - GOE, p. 31 (PDF 32) define V_f/V_max; valor 1,5 escolhido pelo grupo

# ---------------------------------------------------------------------------
# Tubo da fuselagem (PVC) e geometria geral
# ---------------------------------------------------------------------------
d_ext = _v["d_ext"]            # d - diâmetro externo do tubo [m] - OR
t_c = _v["t_c"]                # t_c - espessura de parede do tubo [m] - OR (medir no tubo real)
L_n = _v["L_n"]                # L_n - comprimento da ogiva [m] - OR
L_c = _v["L_c"]                # L_c - comprimento do tubo do corpo [m] - OR
E_c = _v["E_c"]                # E_c - módulo de elasticidade do PVC [Pa] - MED, Tab. 5 (p. 642; PDF 8), amostra 1
sig_c = _v["sig_c"]            # σ_c - tensão de ruptura do PVC [Pa] - MED, Tab. 5 (p. 642; PDF 8), amostra 1
S_yc = _v["S_yc"]              # S_yc - escoamento em compressão do PVC (≈ σ_c) [Pa] - hipótese (referência não identificada)
rho_c = _v["rho_c"]            # ρ_c - massa específica do PVC [kg/m³] - OR (material PVC)

# ---------------------------------------------------------------------------
# PLA impresso (ogiva, anteparos)
# ---------------------------------------------------------------------------
sig_n = _v["sig_n"]            # σ_n - tensão limite do PLA [Pa] - hipótese, a ensaiar (referência não identificada)

# ---------------------------------------------------------------------------
# Ogiva, ombro e baia
# ---------------------------------------------------------------------------
m_ogiva = _v["m_ogiva"]        # m_n - massa da ogiva [kg] - planilha Rev. 7 (OR: 0,1028 kg)
D_o = _v["D_o"]                # D_o - diâmetro externo do ombro da ogiva [m] - OR
t_o = _v["t_o"]                # t_o - espessura da parede do ombro [m] - OR
t_cap = _v["t_cap"]            # t_cap - espessura do fundo do ombro [m] - OR
t_ant = _v["t_ant"]            # t_ant - espessura dos anteparos da baia de aviônicos [m] - OR
m_ant_baia = _v["m_ant_baia"]  # m_ant - massa dos 2 anteparos da baia [kg] - planilha Rev. 7

# ---------------------------------------------------------------------------
# Pinos de cisalhamento (junção ogiva-tubo)
# ---------------------------------------------------------------------------
n_p = _v["n_p"]                # n_p - número de pinos [-] - projeto
d_p = _v["d_p"]                # d_p - diâmetro dos pinos de náilon [m] - projeto (Rev. 3)
tau_p = _v["tau_p"]            # τ_u,p - resistência ao cisalhamento do náilon [Pa] - hipótese, a ensaiar (referência não identificada)

# ---------------------------------------------------------------------------
# Massas e posições por sistema (x medido a partir da ponta da ogiva)
# ---------------------------------------------------------------------------
x_T = _v["x_T"]                # x_T - face dianteira do anteparo de empuxo [m] - OR
m_estr = _v["m_estr"]          # m_estr - massa da estrutura (inclui ogiva) [kg] - planilha Rev. 7 (soma dos componentes)
x_estr = _v["x_estr"]          # x_estr - CG da estrutura [m] - planilha Rev. 7
m_mot = _v["m_mot"]            # m_mot - massa do motor G80T carregado [kg] - catálogo AeroTech (banco do OR)
x_mot = _v["x_mot"]            # x_mot - CG do motor carregado [m] - catálogo/OR
m_avi = _v["m_avi"]            # m_avi - massa dos aviônicos [kg] - OR (pesar)
x_avi = _v["x_avi"]            # x_avi - CG dos aviônicos [m] - OR
m_rec = _v["m_rec"]            # m_rec - massa da recuperação [kg] - OR (pesar)
x_rec = _v["x_rec"]            # x_rec - CG da recuperação [m] - OR

# ---------------------------------------------------------------------------
# Motor AeroTech G80T
# ---------------------------------------------------------------------------
m_mot_v = _v["m_mot_v"]        # m_mot,v - massa do motor vazio [kg] - catálogo AeroTech (banco do OR)
F_max = _v["F_max"]            # F_max - empuxo máximo [N] - curva de empuxo G80T (OR)
t_q = _v["t_q"]                # t_q - tempo de queima [s] - curva de empuxo G80T (OR)

# ---------------------------------------------------------------------------
# Dados de voo (simulação OpenRocket)
# ---------------------------------------------------------------------------
H_Vmax = _v["H_Vmax"]          # H - altitude em que ocorre V_max [m] - OR
V_max = _v["V_max"]            # V_max - velocidade máxima [m/s] - OR
t_LC2 = _v["t_LC2"]            # t - instante de V_max [s] - OR
T_LC2 = _v["T_LC2"]            # T - empuxo no instante de V_max [N] - OR
D_LC2 = _v["D_LC2"]            # D - arrasto total no instante de V_max [N] - OR
V_raj = _v["V_raj"]            # V_raj - rajada lateral de projeto [m/s] - PAL, p. 246 (VLS-1)
R_ar = _v["R_ar"]              # R - constante do ar [J/(kg.K)] - atmosfera padrão (referência não identificada na pasta)

# ---------------------------------------------------------------------------
# Coeficientes aerodinâmicos (dados)
# ---------------------------------------------------------------------------
C_Na_n = _v["C_Na_n"]          # C_Nα,n - coef. de força normal da ogiva [1/rad] - BAW, eq. 3-66 (PDF 31): 2.A_base/A_ref = 2
X_n = _v["X_n"]                # X_n - centro de pressão da ogiva (0,466.L_n) [m] - BAW, eq. 3-89 (PDF 39): X = L - V/A_base (planilha Rev. 7)

# ---------------------------------------------------------------------------
# Aletas (G10)
# ---------------------------------------------------------------------------
C_r = _v["C_r"]                # C_r - corda na raiz [m] - OR
C_t = _v["C_t"]                # C_t - corda na ponta [m] - OR
s_al = _v["s_al"]              # s - envergadura [m] - OR
x_r = _v["x_r"]                # x_r - enflechamento do bordo de ataque [m] - OR
t_f = _v["t_f"]                # t_f - espessura da aleta [m] - OR
G_f = _v["G_f"]                # G - módulo de cisalhamento do G10 [Pa] - hipótese, confirmar com fornecedor (referência não identificada)
kappa = _v["kappa"]            # κ - razão de calores específicos do ar [-] - GOE, p. 28 (PDF 29)
p_0 = _v["p_0"]                # p_0 - pressão ao nível do mar [Pa] - GOE, p. 30 (PDF 31)

# ---------------------------------------------------------------------------
# Compartimento do motor
# ---------------------------------------------------------------------------
t_ae = _v["t_ae"]              # t_ae - espessura do anteparo de empuxo (PLA) [m] - OR
tau_cola = _v["tau_cola"]      # τ_cola - cisalhamento do epóxi sobre PVC [Pa] - hipótese conservadora (referência não identificada)
