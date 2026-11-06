"""
main.py - Execução do cálculo estrutural do minifoguete
(memorial enxuto com bibliografia disponível, base Rev. 8).

Os cálculos são feitos em SI pelas funções de equations.py, na ordem de dependência.
Na tabela, alguns valores são exibidos em unidades práticas (mm, g, MPa, kPa, °).
"""

from math import degrees

import inputs as e
import equations as eq

MM, G, MPA, KPA = 1e3, 1e3, 1e-6, 1e-3   # fatores de exibição: m->mm, kg->g, Pa->MPa, Pa->kPa


class CalculoFoguete:
    """Executa as etapas 1 a 10 do memorial e guarda os resultados para a tabela."""

    def __init__(self):
        self.resultados = []
        self.etapa1_criterio()
        self.etapa2_geometria_tubo()
        self.etapa3_massas()
        self.etapa4_atmosfera()
        self.etapa5_cargas()
        self.etapa6_tubo()
        self.etapa7_ogiva()
        self.etapa8_aletas()
        self.etapa9_motor()
        self.etapa10_espessuras()

    def _guardar(self, nome, sigla, valor, unidade, fator=1.0):
        self.resultados.append((nome, sigla, valor * fator, unidade))

    def _titulo(self, texto):
        self.resultados.append((texto, None, None, None))

    # ------------------------------------------------------------------ Etapa 1
    def etapa1_criterio(self):
        self._titulo("ETAPA 1 - Critério de projeto")
        self.sig_adm_c = eq.tensao_admissivel(e.sig_c, e.FS)
        self.sig_adm_n = eq.tensao_admissivel(e.sig_n, e.FS)
        self._guardar("Tensão admissível do PVC", "σ_adm,c", self.sig_adm_c, "MPa", MPA)
        self._guardar("Tensão admissível do PLA", "σ_adm,n", self.sig_adm_n, "MPa", MPA)

    # ------------------------------------------------------------------ Etapa 2
    def etapa2_geometria_tubo(self):
        self._titulo("ETAPA 2 - Geometria do tubo")
        self.L_tot = eq.comprimento_total(e.L_n, e.L_c)
        self.esbeltez = eq.esbeltez_foguete(self.L_tot, e.d_ext)
        self.D_i = eq.diametro_interno(e.d_ext, e.t_c)
        self.A_ref = eq.area_circulo(e.d_ext)
        self.A = eq.area_coroa(e.d_ext, self.D_i)
        self.I = eq.inercia_coroa(e.d_ext, self.D_i)
        self.c = eq.fibra_extrema(e.d_ext)
        self.R_m = eq.raio_medio(e.d_ext, e.t_c)
        self.R_t = eq.relacao_raio_espessura(self.R_m, e.t_c)
        self.A_int = eq.area_circulo(self.D_i)
        self._guardar("Comprimento total", "L_tot", self.L_tot, "mm", MM)
        self._guardar("Esbeltez do foguete (< 20)", "L/d", self.esbeltez, "-")
        self._guardar("Diâmetro interno", "D_i", self.D_i, "mm", MM)
        self._guardar("Área de referência", "A_ref", self.A_ref, "mm²", MM**2)
        self._guardar("Área da parede", "A", self.A, "mm²", MM**2)
        self._guardar("Momento de inércia", "I", self.I, "mm⁴", MM**4)
        self._guardar("Fibra extrema", "c", self.c, "mm", MM)
        self._guardar("Raio médio", "R_m", self.R_m, "mm", MM)
        self._guardar("Relação raio/espessura (> 10)", "R_m/t_c", self.R_t, "-")
        self._guardar("Área interna", "A_int", self.A_int, "mm²", MM**2)

    # ------------------------------------------------------------------ Etapa 3
    def etapa3_massas(self):
        self._titulo("ETAPA 3 - Massas e CG")
        massas = [e.m_estr, e.m_mot, e.m_avi, e.m_rec]
        posicoes = [e.x_estr, e.x_mot, e.x_avi, e.x_rec]
        self.M_0 = eq.massa_total(massas)
        self.x_cg = eq.centro_gravidade(massas, posicoes)
        self.m_tubo_frente = eq.massa_tubo_trecho(e.rho_c, self.A, e.x_T, e.L_n)
        self.M_frente = eq.massa_frente(e.m_ogiva, self.m_tubo_frente, e.m_ant_baia, e.m_avi, e.m_rec)
        self.m_p = eq.massa_propelente(e.m_mot, e.m_mot_v)
        self.M_q = eq.massa_apos_queima(self.M_0, self.m_p)
        self._guardar("Massa de decolagem", "M_0", self.M_0, "g", G)
        self._guardar("Centro de gravidade (da ponta)", "x_cg", self.x_cg, "mm", MM)
        self._guardar("Massa do tubo à frente de x_T", "m_tubo,f", self.m_tubo_frente, "g", G)
        self._guardar("Massa à frente do anteparo", "M_frente", self.M_frente, "g", G)
        self._guardar("Massa de propelente", "m_p", self.m_p, "g", G)
        self._guardar("Massa após a queima", "M_q", self.M_q, "g", G)

    # ------------------------------------------------------------------ Etapa 4
    def etapa4_atmosfera(self):
        self._titulo("ETAPA 4 - Atmosfera em V_max")
        self.T_c = eq.temperatura_altitude(e.H_Vmax)
        self.p = eq.pressao_altitude(self.T_c)
        self.a = eq.velocidade_som(self.T_c)
        self.rho = eq.densidade_ar(self.p, e.R_ar, self.T_c)
        self._guardar("Temperatura do ar", "T_c", self.T_c, "°C")
        self._guardar("Pressão do ar", "p", self.p, "kPa", KPA)
        self._guardar("Velocidade do som", "a", self.a, "m/s")
        self._guardar("Densidade do ar", "ρ", self.rho, "kg/m³")

    # ------------------------------------------------------------------ Etapa 5
    def etapa5_cargas(self):
        self._titulo("ETAPA 5 - Cargas LC1, LC2, LC3 e LC5")
        # LC1 - empuxo máximo (arrasto desprezível, M = M_0)
        self.axg1 = eq.fator_carga_axial(e.F_max, 0.0, self.M_0)
        self.N_ax1 = eq.compressao_tubo(0.0, self.M_frente, self.axg1)
        # LC2 - V_max com rajada
        self.Q = eq.pressao_dinamica(self.rho, e.V_max)
        self.alpha = eq.angulo_ataque(e.V_raj, e.V_max)
        self.N_n = eq.forca_normal(self.Q, self.A_ref, e.C_Na_n, self.alpha)
        self.M_2 = eq.massa_instante(self.M_0, self.m_p, e.t_LC2, e.t_q)
        self.axg2 = eq.fator_carga_axial(e.T_LC2, e.D_LC2, self.M_2)
        self.N_ax2 = eq.compressao_tubo(e.D_LC2, self.M_frente, self.axg2)
        self.M_LC2 = eq.momento_fletor_LC2(self.N_n, self.x_cg, e.X_n)
        # LC3 - ejeção
        self.F_pu = eq.forca_ruptura_pinos(e.n_p, e.tau_p, e.d_p)
        self.p_ej = eq.pressao_ejecao(e.FS_ej, self.F_pu, self.A_int)
        # LC5 - separação da ogiva
        self.F_sep = eq.forca_separacao(e.m_ogiva, e.D_LC2, self.M_q)
        self._guardar("LC1: fator de carga axial", "(a+g)_1", self.axg1, "m/s²")
        self._guardar("LC1: compressão no tubo", "N_ax,1", self.N_ax1, "N")
        self._guardar("LC2: pressão dinâmica", "Q", self.Q, "Pa")
        self._guardar("LC2: ângulo de ataque", "α", degrees(self.alpha), "°")
        self._guardar("LC2: força normal na ogiva", "N_n", self.N_n, "N")
        self._guardar("LC2: massa no instante de V_max", "M_2", self.M_2, "g", G)
        self._guardar("LC2: fator de carga axial", "(a+g)_2", self.axg2, "m/s²")
        self._guardar("LC2: compressão no tubo", "N_ax,2", self.N_ax2, "N")
        self._guardar("LC2: momento fletor no tubo", "M_LC2", self.M_LC2, "N.m")
        self._guardar("LC3: ruptura dos pinos", "F_p,u", self.F_pu, "N")
        self._guardar("LC3: pressão de ejeção", "p_ej", self.p_ej, "kPa", KPA)
        self._guardar("LC5: separação da ogiva", "F_sep", self.F_sep, "N")

    # ------------------------------------------------------------------ Etapa 6
    def etapa6_tubo(self):
        self._titulo("ETAPA 6 - Tubo de PVC")
        self.sig_a1 = eq.tensao_normal(self.N_ax1, self.A)
        self.sig_comb = eq.tensao_flexao_composta(self.N_ax2, self.A, self.M_LC2, self.c, self.I)
        self.MS_comb = eq.margem_seguranca(e.sig_c, e.FS, self.sig_comb)
        self.k = eq.raio_giracao(self.I, self.A)
        self.S_r = eq.indice_esbeltez(self.L_tot, self.k)
        self.S_rD = eq.esbeltez_transicao(e.E_c, e.S_yc)
        self.P_cr = eq.carga_critica_euler(e.E_c, self.A, self.S_r)
        self.FS_col = eq.razao_cargas(self.P_cr, self.N_ax1)
        self.sig_anel = eq.tensao_anel(self.p_ej, self.R_m, e.t_c)
        self.MS_anel = eq.margem_seguranca(e.sig_c, e.FS, self.sig_anel)
        self.F_pino = eq.forca_por_elemento(self.F_pu, e.n_p)
        self.sig_br = eq.tensao_esmagamento(self.F_pino, e.d_p, e.t_c)
        self.MS_br = eq.margem_seguranca(e.sig_c, e.FS, self.sig_br)
        self.sig_ant = eq.tensao_viga_distribuida(self.p_ej, self.D_i / 2, e.t_ant)
        self.MS_ant = eq.margem_seguranca(e.sig_n, e.FS, self.sig_ant)
        self._guardar("Tensão de compressão (LC1)", "σ_a,1", self.sig_a1, "MPa", MPA)
        self._guardar("Tensão de flexão composta (LC2)", "σ_comb", self.sig_comb, "MPa", MPA)
        self._guardar("Margem - flexão composta", "MS_comb", self.MS_comb, "-")
        self._guardar("Raio de giração", "k", self.k, "mm", MM)
        self._guardar("Índice de esbeltez", "S_r", self.S_r, "-")
        self._guardar("Esbeltez de transição (Euler se S_r >)", "(S_r)_D", self.S_rD, "-")
        self._guardar("Carga crítica de Euler", "P_cr", self.P_cr, "N")
        self._guardar("Fator de segurança à flambagem", "FS_col", self.FS_col, "-")
        self._guardar("Tensão de anel na ejeção (LC3)", "σ_2", self.sig_anel, "MPa", MPA)
        self._guardar("Margem - ejeção", "MS_ej", self.MS_anel, "-")
        self._guardar("Força em cada pino", "F_pino", self.F_pino, "N")
        self._guardar("Esmagamento do furo no PVC", "σ_br", self.sig_br, "MPa", MPA)
        self._guardar("Margem - furo no PVC", "MS_br", self.MS_br, "-")
        self._guardar("Tensão nos anteparos da baia", "σ_ant", self.sig_ant, "MPa", MPA)
        self._guardar("Margem - anteparos da baia", "MS_ant", self.MS_ant, "-")

    # ------------------------------------------------------------------ Etapa 7
    def etapa7_ogiva(self):
        self._titulo("ETAPA 7 - Ogiva e junção com pinos")
        self.a_f = eq.raio_livre_fundo(e.D_o, e.t_o)
        self.sig_fundo = eq.tensao_viga_distribuida(self.p_ej, self.a_f, e.t_cap)
        self.MS_fundo = eq.margem_seguranca(e.sig_n, e.FS, self.sig_fundo)
        self.sig_br_o = eq.tensao_esmagamento(self.F_pino, e.d_p, e.t_o)
        self.MS_br_o = eq.margem_seguranca(e.sig_n, e.FS, self.sig_br_o)
        self.ret_ogiva = eq.razao_cargas(self.F_pu, self.F_sep)
        self._guardar("Raio livre do fundo do ombro", "a_f", self.a_f, "mm", MM)
        self._guardar("Tensão no fundo do ombro", "σ_fundo", self.sig_fundo, "MPa", MPA)
        self._guardar("Margem - fundo do ombro", "MS_fundo", self.MS_fundo, "-")
        self._guardar("Esmagamento do furo no ombro", "σ_br,o", self.sig_br_o, "MPa", MPA)
        self._guardar("Margem - furo no ombro", "MS_br,o", self.MS_br_o, "-")
        self._guardar("Retenção da ogiva em voo (>= FS)", "F_pu/F_sep", self.ret_ogiva, "-")

    # ------------------------------------------------------------------ Etapa 8
    def etapa8_aletas(self):
        self._titulo("ETAPA 8 - Aletas: flutter")
        self.S = eq.area_aleta(e.C_r, e.C_t, e.s_al)
        self.AR = eq.razao_aspecto(e.s_al, self.S)
        self.lam = eq.afilamento(e.C_t, e.C_r)
        self.C_x_al = eq.centroide_corda(e.C_r, e.C_t, e.x_r)
        self.eps = eq.parametro_epsilon(self.C_x_al, e.C_r)
        self.DN = eq.constante_DN(self.eps, e.kappa, e.p_0)
        self.V_f = eq.velocidade_flutter(self.a, e.G_f, self.DN, self.AR, e.t_f, e.C_r, self.lam, self.p, e.p_0)
        self.V_f_min = eq.velocidade_flutter_minima(e.FS_V, e.V_max)
        self.fator_flut = eq.razao_cargas(self.V_f, e.V_max)
        self._guardar("Área de uma aleta", "S", self.S, "mm²", MM**2)
        self._guardar("Razão de aspecto", "AR", self.AR, "-")
        self._guardar("Afilamento", "λ", self.lam, "-")
        self._guardar("Centroide na corda", "C_x", self.C_x_al, "mm", MM)
        self._guardar("Parâmetro de Bennett", "ε", self.eps, "-")
        self._guardar("Constante do denominador", "DN", self.DN, "Pa")
        self._guardar("Velocidade de flutter", "V_f", self.V_f, "m/s")
        self._guardar("Flutter mínimo exigido", "V_f,min", self.V_f_min, "m/s")
        self._guardar("Razão flutter / V_max (>= FS_V)", "V_f/V_max", self.fator_flut, "-")

    # ------------------------------------------------------------------ Etapa 9
    def etapa9_motor(self):
        self._titulo("ETAPA 9 - Compartimento do motor")
        self.sig_ae = eq.tensao_viga_concentrada(e.F_max, e.t_ae)
        self.MS_ae = eq.margem_seguranca(e.sig_n, e.FS, self.sig_ae)
        self.tau_ae = eq.tensao_colagem(e.F_max, self.D_i, e.t_ae)
        self.MS_cola_ae = eq.margem_seguranca(e.tau_cola, e.FS, self.tau_ae)
        self._guardar("Tensão no anteparo de empuxo", "σ_ae", self.sig_ae, "MPa", MPA)
        self._guardar("Margem - anteparo de empuxo", "MS_ae", self.MS_ae, "-")
        self._guardar("Cisalhamento na colagem do anteparo", "τ_ae", self.tau_ae, "MPa", MPA)
        self._guardar("Margem - colagem do anteparo", "MS_cola", self.MS_cola_ae, "-")

    # ----------------------------------------------------------------- Etapa 10
    def etapa10_espessuras(self):
        self._titulo("ETAPA 10 - Espessuras mínimas")
        t_flex = eq.t_min_flexao_composta(e.FS, e.sig_c, self.N_ax2, self.M_LC2, self.R_m)
        t_ej = eq.t_min_anel(e.FS, self.p_ej, self.R_m, e.sig_c)
        t_eul = eq.t_min_euler(e.FS, self.N_ax1, self.L_tot, e.E_c, self.R_m)
        t_pino = eq.t_min_esmagamento_pino(e.tau_p, e.d_p, self.sig_adm_c)
        self.t_tubo = eq.espessura_minima(t_flex, t_ej, t_eul, t_pino)
        self.t_baia = eq.t_min_viga_distribuida(self.D_i / 2, e.FS, self.p_ej, e.sig_n)
        self.t_fundo = eq.t_min_viga_distribuida(self.a_f, e.FS, self.p_ej, e.sig_n)
        self.t_ae = eq.t_min_viga_concentrada(e.FS, e.F_max, e.sig_n)
        self.t_aleta = eq.t_min_flutter(e.C_r, self.DN, self.AR, self.lam, self.p, e.p_0, self.V_f_min, e.G_f, self.a)
        self._guardar("Tubo: flexão composta", "t_flex", t_flex, "mm", MM)
        self._guardar("Tubo: ejeção", "t_ej", t_ej, "mm", MM)
        self._guardar("Tubo: Euler", "t_Euler", t_eul, "mm", MM)
        self._guardar("Tubo: furo do pino", "t_pino", t_pino, "mm", MM)
        self._guardar("Tubo: espessura mínima", "t_min,tubo", self.t_tubo, "mm", MM)
        self._guardar("Tubo: folga (adotada/mínima)", "folga_tubo", eq.folga(e.t_c, self.t_tubo), "-")
        self._guardar("Anteparos da baia: mínima", "t_min,baia", self.t_baia, "mm", MM)
        self._guardar("Anteparos da baia: folga", "folga_baia", eq.folga(e.t_ant, self.t_baia), "-")
        self._guardar("Fundo do ombro: mínima", "t_min,fundo", self.t_fundo, "mm", MM)
        self._guardar("Fundo do ombro: folga", "folga_fundo", eq.folga(e.t_cap, self.t_fundo), "-")
        self._guardar("Anteparo de empuxo: mínima", "t_min,ae", self.t_ae, "mm", MM)
        self._guardar("Anteparo de empuxo: folga", "folga_ae", eq.folga(e.t_ae, self.t_ae), "-")
        self._guardar("Aleta: espessura mínima (flutter)", "t_min,aleta", self.t_aleta, "mm", MM)
        self._guardar("Aleta: folga", "folga_aleta", eq.folga(e.t_f, self.t_aleta), "-")

    # -------------------------------------------------------------- Tabela
    def imprimir(self):
        largura = 84
        print("=" * largura)
        print("RESULTADOS DOS CÁLCULOS".center(largura))
        print("=" * largura)
        print(f"{'Variável':<42}{'Sigla':<14}{'Valor':>14}   {'Unidade':<8}")
        for nome, sigla, valor, unidade in self.resultados:
            if sigla is None:
                print("-" * largura)
                print(nome)
                print("-" * largura)
            else:
                texto = f"{valor:.1f}" if abs(valor) >= 1000 else f"{valor:.4g}"
                print(f"{nome:<42}{sigla:<14}{texto:>14}   {unidade:<8}")
        print("=" * largura)


if __name__ == "__main__":
    CalculoFoguete().imprimir()
