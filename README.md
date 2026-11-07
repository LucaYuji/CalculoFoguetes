# Calculo Foguetes

# Programa de Cálculo Estrutural – Minifoguete

Cálculo estrutural de um minifoguete com 500 m de apogeu e massa máxima de 1,5 kg. O programa segue o *Memorial de Cálculo Estrutural*.

Projeto acadêmico – FATEC São José dos Campos, Grupo 2 (Estrutura).

## Requisitos

- Python 3.8 ou superior
- Só bibliotecas padrão (`math`, `csv`, `os`); nada para instalar

## Como executar

```bash
python main.py
```

O resultado sai no terminal, em uma tabela com as colunas **Variável | Sigla | Valor | Unidade**, separada por etapa.

## Estrutura

| Arquivo | Conteúdo |
| --- | --- |
| `inputs.csv` | Dados de entrada, com as colunas `Variável, Valor, Unidade, Descrição`. Todos os valores estão em SI. |
| `inputs.py` | Lê o CSV e cria uma variável para cada entrada. Cada variável traz em comentário o nome, a unidade e a referência. |
| `equations.py` | As equações, uma função por equação, em ordem de dependência. A docstring de cada função diz o que ela calcula, as variáveis com unidades e a referência. |
| `main.py` | Classe `CalculoFoguete`: chama as funções na ordem das etapas e imprime a tabela. Não implementa nenhuma equação. |
| `referencias.py` | Significado das siglas de bibliografia (só comentários). |

## Etapas de cálculo

1. Critério de projeto: tensão admissível e margem de segurança
2. Geometria do tubo
3. Massas e centro de gravidade
4. Atmosfera na altitude da velocidade máxima
5. Cargas: LC1 (empuxo máximo), LC2 (velocidade máxima com rajada), LC3 (ejeção), LC5 (separação da ogiva)
6. Tubo de PVC e anteparos da baia: flexão composta, Euler, vaso de parede fina, esmagamento
7. Ogiva e junção com pinos
8. Aletas: geometria e velocidade de flutter
9. Compartimento do motor: anteparo de empuxo e colagem
10. Espessuras mínimas e folgas

## Alterar os dados

Basta editar a coluna `Valor` do `inputs.csv` e executar `python main.py` de novo. Os nomes da coluna `Variável` não podem mudar, porque o `inputs.py` lê as variáveis por esses nomes.

## Critério de aprovação

- Margem de segurança: MS = σ_lim / (FS · σ) − 1 ≥ 0
- Folga de espessura: t_adotada / t_min ≥ 1

## Referências

Siglas usadas nos comentários e docstrings (a lista completa está em `referencias.py`):

| Sigla | Fonte |
| --- | --- |
| PAL | Palmerio – *Introdução à tecnologia de foguetes* (2017) |
| GOE | Goehr – TCC sobre flutter em aletas, UFSC (2025) |
| GRA | Grant et al. – *Team 24: IREC Fall Final Report*, FAMU/FSU (2016) |
| MAG | Magaldi, Mattos e Lima – fuselagem de minifoguete no OpenRocket, SIINTEC (2023) |
| MED | Medeiros e Wiebeck – PVC orientado, *Polímeros* (2013) |
| SCH | Schlichta – TCC sobre foguete de 500 m, UFSC (2025) |
| BAR | Norma BAR-2/2020 |
| BAW | Barrowman (1967) |
| HIB | Hibbeler – *Resistência dos materiais* |
| OR / CAT | Modelo OpenRocket da equipe / catálogo do fabricante (fontes de dados) |

Quando uma expressão não tem fonte identificada, a docstring informa "não identificada". As hipóteses próprias do grupo (placa tratada como viga biapoiada, momento sem alívio de inércia, inversões de espessura) aparecem como dedução no memorial.
