import csv
import random
import matplotlib.pyplot as plt
from collections import deque
import os
import time
import numpy as np

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

# ----------------------------------------------------
# --- 1. VARIÁVEIS DE AMBIENTE (Sensores de Marte) ---
# ----------------------------------------------------

def gerar_ambiente():
    tempestade_areia = random.choice([True, False])
    pista_livre = random.choice([True, False])
    sensores_ok = random.choice([True, False])

    print(f"[SENSOR] Tempestade de Areia: {tempestade_areia}")
    print(f"[SENSOR] Pista Livre: {pista_livre}")
    print(f"[SENSOR] Integridade dos Sensores: {sensores_ok}\n")

    return tempestade_areia, pista_livre, sensores_ok

# Criando o arquivo CSV
def gerar_arquivo():
    with open('modulos.csv', 'w', encoding='utf-8') as f:
        # (ID do Módulo, Nome, Prioridade, Combustível, Massa, Criticidade, Horário)
        f.write("HAB-01,Habitacao,4,60.0,20.0,Media,08:00\n")
        f.write("ENE-01,Energia,1,12.0,18.0,Extrema,08:15\n")
        f.write("LAB-01,Laboratorio Cientifico,5,85.0,15.0,Baixa,08:30\n")
        f.write("LOG-01,Logistica,3,55.0,25.0,Baixa,08:45\n")
        f.write("MED-01,Suporte Medico,2,40.0,10.0,Alta,09:00\n")
        f.write("ISRU-01,Modulo de Extracao,2,18.5,12.5,Alta,09:15\n")

    print("--- ARQUIVO CSV GERADO COM SUCESSO ---")

# -------------------------------------------
# --- 2. ESTRUTURA LINEAR (Fila de Pouso) ---
# -------------------------------------------

def ler_arquivo():
    fila_de_pouso = []
    print("Lendo dados dos módulos do CSV...\n")
    with open('modulos.csv', mode='r', encoding='utf-8') as arquivo:
        leitor = csv.reader(arquivo)
        for linha in leitor:
            if len(linha) == 0: continue
            fila_de_pouso.append(linha)
    print(f"{len(fila_de_pouso)} módulo(s) aguardando na fila de órbita.")
    return fila_de_pouso

# ----------------------------------------------------
# --- 3. ALGORITMOS DE INTELIGÊNCIA (SCORE E BUSCA) ---
# ----------------------------------------------------

# 3.1 Cálculo de Score
def calcular_score(modulo):
    """
    Calcula a urgência do pouso baseado em múltiplos fatores.
    Maior score = Maior urgência.
    """
    prioridade_nativa = int(modulo[2])
    combustivel = float(modulo[3])
    massa = float(modulo[4])
    criticidade = modulo[5]
    horario = modulo[6]

    score = 0

    # Pesos por Prioridade Técnica
    tabela_prioridade = {1: 100, 2: 80, 3: 60, 4: 40}
    score += tabela_prioridade.get(prioridade_nativa, 20)

    # Urgência por Combustível
    if combustivel <= 20: score += 40
    elif combustivel <= 40: score += 30
    elif combustivel <= 60: score += 20
    else: score += 10

    # Fator de Inércia (Massa)
    if massa >= 20: score += 20
    elif massa >= 15: score += 15
    else: score += 10

    # Fator de Risco (Criticidade)
    tabela_criticidade = {"Extrema": 50, "Alta": 35, "Media": 20}
    score += tabela_criticidade.get(criticidade, 10)

    # Fator Temporal (Horário de Chegada)
    hora, minuto = horario.split(":")
    minutos_totais = int(hora) * 60 + int(minuto)
    score += (600 - minutos_totais) / 10 # Prioriza quem chegou mais cedo

    return score

# 3.2 Busca: Localizando o módulo com menor combustível
def buscar_modulo_critico(fila_de_pouso):
    print("Buscando módulo em estado mais crítico de combustível...")
    modulo_critico = fila_de_pouso[0]
    for modulo in fila_de_pouso:
        if float(modulo[3]) < float(modulo_critico[3]):
            modulo_critico = modulo
    print(f"ALERTA: O módulo {modulo_critico[0]} é o mais crítico ({modulo_critico[3]}%)\n")
    return modulo_critico

# 3.3 Ordenação Avançada (Bubble Sort por Score)
def ordenar_fila_por_score(fila_de_pouso):
    n = len(fila_de_pouso)
    for i in range(n):
        for j in range(0, n - i - 1):
            # Compara os scores calculados em tempo real
            if calcular_score(fila_de_pouso[j]) < calcular_score(fila_de_pouso[j+1]):
                fila_de_pouso[j], fila_de_pouso[j+1] = fila_de_pouso[j+1], fila_de_pouso[j]
    print("Fila REORGANIZADA pela ordenação de Score.\n")

# --------------------------------------------------------
# --- 4. PROCESSAMENTO DA FILA E ESTRUTURAS AUXILIARES ---
# --------------------------------------------------------
def processar_fila(fila_de_pouso, tempestade, pista, sensores):
    frota_status = []
    for m in fila_de_pouso:
        frota_status.append({
            "id": m[0],
            "score": calcular_score(m),
            "combustivel": float(m[3]),
            "status": "  EM ÓRBITA",
            "msg": "Aguardando Janela"
        })

    def desenhar_painel():
        limpar_tela() 
        print("="*95)
        print("   PAINEL DE CONTROLE MGPEB - TELEMETRIA AO VIVO")
        print("="*95) 
        print(f"   SENSORES: Tempestade: {'SIM  ' if tempestade else 'NÃO  '} | Pista: {'LIVRE  ' if pista else 'OCUPADA  '} | Sensores: {'OK  ' if sensores else 'FALHA  '}")
        print("-" * 95) 
        print(f"{'ID':<10} | {'SCORE':<7} | {'COMBUSTÍVEL':<15} | {'STATUS':<15} | {'TELEMETRIA'}")
        print("-" * 95) 
        for m in frota_status:
            print(f"{m['id']:<10} | {m['score']:>5.0f}   | {m['combustivel']:>10.1f}%      | {m['status']:<15} | {m['msg']}")
        print("="*95) 

    fila_indices = list(range(len(frota_status)))

    while fila_indices:
        idx_atual = fila_indices.pop(0)
        m_atual = frota_status[idx_atual]

        m_atual['status'] = "🔎 AVALIANDO"
        m_atual['msg'] = "Analisando telemetria..."
        desenhar_painel()
        time.sleep(0.2)

        pouso_seguro = (not tempestade and pista and sensores)
        emergencia = (m_atual['combustivel'] <= 18.5)

        if pouso_seguro or emergencia:
            if emergencia and not pouso_seguro:
                m_atual['status'] = "⚠️ EMERGÊNCIA"
                m_atual['msg'] = "Pouso Forçado (Combustível Crítico)"
            else:
                m_atual['status'] = "  POUSANDO"
                m_atual['msg'] = "Descida Autorizada (Clima OK)"

            desenhar_painel()
            time.sleep(0.3)

            m_atual['status'] = "✅ EM SOLO"
            m_atual['msg'] = "Toque confirmado. Bem-vindo a Marte!"
        else:

            perda = 0.8
            m_atual['combustivel'] -= perda
            m_atual['status'] = "⏳ AGUARDANDO"
            m_atual['msg'] = f"Bloqueado. Consumo de órbita: -{perda:.1f}%"

            desenhar_painel()
            time.sleep(0.5)

            fila_indices.append(idx_atual)

    # Relatório Final
    limpar_tela()
    print("="*85)
    print(" ✅ RELATÓRIO FINAL DE OPERAÇÕES MGPEB - TODOS EM SOLO")
    print("="*85)
    for m in frota_status:
        print(f"{m['id']:<10} | {m['combustivel']:>10.1f}%     | ✅ EM SOLO      | Operação Concluída")
    print("="*85 + "\n")

    modulo_para_simular = frota_status[0]
    for m in frota_status:
        if m['combustivel'] < modulo_para_simular['combustivel']:
            modulo_para_simular = m

    return modulo_para_simular['id'], modulo_para_simular['combustivel']

# ----------------------------------------------------
# --- 5. SIMULAÇÃO FÍSICA (Consumo de Combustível) ---
# ----------------------------------------------------
def simulacao_fisica(nome_modulo="ISRU-01", tanque_atual=18.5):
    altitude = 1000.0
    queima_fixa = 0.8

    tempo_maximo_voo = tanque_atual / queima_fixa
    velocidade_limite = altitude / tempo_maximo_voo
    velocidade = random.uniform(velocidade_limite - 10.0, velocidade_limite + 10.0)

    tempo = 0

    print("\n" + "="*65)
    print(f"INICIANDO SIMULAÇÃO FÍSICA DE DESCIDA (MÓDULO: {nome_modulo})")
    print(f"ALERTA METEOROLÓGICO: Velocidade de queda ajustada em {velocidade:.1f} m/s")
    print("="*65)

    while altitude > 0 and tanque_atual > 0:
        print(f"{tempo:02d}s | {altitude:7.1f}m | {tanque_atual:5.1f}% | QUEIMA CONSTANTE")
        altitude -= velocidade
        tanque_atual -= queima_fixa

        if tanque_atual < 0:
            tanque_atual = 0.0

        tempo += 1

    print("-" * 65)
    if altitude <= 0:
        print(f">> SUCESSO: Toque no solo confirmado! Restante: {tanque_atual:.1f}%")
    else:
        print(f">> ALERTA FATAL: Impacto a {altitude:.1f}m de altura. (Combustível Esgotado)")

# ----------------------------------------------------
# --- ROTINA PRINCIPAL DO SISTEMA ---
# ----------------------------------------------------
def rotina_mgpeb():
    print("\n--- PROTOCOLO MGPEB INICIADO ---\n")
    tempestade, pista, sensores = gerar_ambiente()
    gerar_arquivo()
    fila_de_pouso = ler_arquivo()

    buscar_modulo_critico(fila_de_pouso)

    # Aplicando a ordenação por Score
    ordenar_fila_por_score(fila_de_pouso)
    # Chamada do painel
    id_dinamico, comb_dinamico = processar_fila(fila_de_pouso, tempestade, pista, sensores)
    # Chamada da simulação física
    simulacao_fisica(id_dinamico, comb_dinamico)

# ====================================================================
# --- INTERFACE E MENU PRINCIPAL ---
# ====================================================================

temperatura_orbital = random.randint(10, 30)
carga_estacao = random.randint(50, 100)
pressao_comportas = random.randint(20, 60)
integridade_deck = random.randint(0, 1)
sinal_frota = random.randint(0, 1)
reservatorio_central = random.randint(0, 100)

def iniciar_sistema():
    gerar_arquivo()
    limpar_tela()
    print("=" * 65)
    print("      SISTEMA DE GERENCIAMENTO DE POUSO (MGPEB) - BASE MARCIANA  ")
    print("=" * 65)
    print("\nDIAGNÓSTICO DA ESTAÇÃO ORBITAL INICIADO. AGUARDANDO COMANDOS.\n")
    time.sleep(1)

    while True:
        limpar_tela()
        time.sleep(0.3)

        print("\n" + "="*40)
        print("PAINEL DE CONTROLE PRINCIPAL")
        print("="*40)
        print(" 1- Verificar Status da Estação (Deque)")
        print(" 2- Mostrar Gráfico da Frota (Matplotlib)")
        print(" 3- Iniciar Protocolo de Pouso MGPEB")
        print(" 4- Modelagem Física de Descida (Gráfico)")
        print(" 5- Encerrar Sistema\n")

        time.sleep(0.2)
        opcao = input("Digite a opção: ")
        if not opcao.isdigit(): continue
        opcao = int(opcao)

        match opcao:
            case 1:
                print('\n' + '=' * 60)
                def analisar_sistema_termico():
                    return f"Temperatura orbital em {temperatura_orbital}°C"
                def analisar_rede_eletrica():
                    return f"Carga da Estação em {carga_estacao}%"
                def analisar_reservatorio():
                    return f"Reservatório Central em {reservatorio_central}%"
                def analisar_pressurizacao():
                    return f"Pressão das comportas em {pressao_comportas}%"
                def analisar_deck_lancamento():
                    return "Deck de Lançamento: " + ("100%" if integridade_deck else "Crítico")
                def analisar_comunicacao_frota():
                    return "Comunicação: " + ("Ok" if sinal_frota else "Falha")

                fila = deque()
                fila.append(("SISTEMA TÉRMICO", analisar_sistema_termico))
                fila.append(("REDE ELÉTRICA", analisar_rede_eletrica))
                fila.append(("SUPRIMENTO", analisar_reservatorio))
                fila.append(("PRESSURIZAÇÃO", analisar_pressurizacao))
                fila.append(("CASCO", analisar_deck_lancamento))
                fila.append(("FROTA", analisar_comunicacao_frota))

                print("PROCESSANDO DIAGNÓSTICO:\n")
                while fila:
                    nome, funcao = fila.popleft()
                    print(f"[{nome}] {funcao()}")
                input("\n[PAUSA] ENTER para voltar...")

            case 2:
                print("\nLENDO DADOS DO SATÉLITE E GERANDO GRÁFICO...")
                # puxa os dados direto do CSV
                modulos_atuais = ler_arquivo()
                modulos_nomes = [m[0] for m in modulos_atuais]
                niveis_combustivel = [float(m[3]) for m in modulos_atuais]

                fig, ax = plt.subplots(figsize=(10, 6))
                fig.patch.set_facecolor('#0b1a2a')
                ax.set_facecolor('#0b1a2a')

                cores = ['#FF5252' if c <= 18.5 else '#00E5FF' for c in niveis_combustivel]

                barras = ax.bar(modulos_nomes, niveis_combustivel, color=cores, width=0.6)
                ax.axhline(18.5, color='#FFD700', linestyle='--', linewidth=2, label='Emergência MGPEB (18.5%)')

                for barra in barras:
                    altura = barra.get_height()
                    ax.text(barra.get_x() + barra.get_width()/2., altura + 1.5,
                            f'{altura}%', ha='center', va='bottom', color='white', fontweight='bold')

                ax.set_title(" Painel MGPEB: Combustível Inicial de Chegada da Frota", color='white', fontsize=14, fontweight='bold')
                ax.set_xlabel("Módulos na Fila de Pouso", color='white', fontsize=12)
                ax.set_ylabel("Combustível Restante (%)", color='white', fontsize=12)
                ax.tick_params(colors='white')

                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.spines['left'].set_color('white')
                ax.spines['bottom'].set_color('white')

                ax.legend(loc='upper right', facecolor='#0b1a2a', edgecolor='white', labelcolor='white')
                plt.tight_layout()

                plt.show()
                plt.close('all')

                time.sleep(1.5)
                input("\n [PAUSA] Pressione ENTER para voltar ao menu: ")

            case 3:
                rotina_mgpeb()
                time.sleep(1.5)
                input("\n [PAUSA] Pressione ENTER para voltar ao painel: ")

            case 4:
                print("\nGERANDO MODELO MATEMÁTICO DE DESCIDA...")

                t = np.linspace(0, 25, 200)
                c = 18.5 - 0.8 * t
                c = np.clip(c, 0, None)

                fig, ax = plt.subplots(figsize=(10, 6))
                fig.patch.set_facecolor('#0b1a2a')
                ax.set_facecolor('#0b1a2a')

                ax.plot(t, c, color='#00E5FF', linewidth=3, label='Consumo C(t) = 18.5 - 0.8t')

                tempo_impacto = 18.5 / 0.8
                ax.scatter([tempo_impacto], [0], color='#FF5252', s=120, zorder=5, label=f'Esgotamento ({tempo_impacto:.2f}s)')
                ax.axhline(18.5, color='#FFD700', linestyle='--', linewidth=1, alpha=0.7, label='Nível Crítico (18.5%)')

                ax.set_title("Modelo Matemático de Descida (ISRU-01)", color='white', fontsize=14, fontweight='bold')
                ax.set_xlabel("Tempo em segundos (t)", color='white', fontsize=12)
                ax.set_ylabel("Combustível Restante (%)", color='white', fontsize=12)
                ax.tick_params(colors='white')

                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.spines['left'].set_color('white')
                ax.spines['bottom'].set_color('white')
                ax.grid(True, color='#ffffff', alpha=0.1, linestyle='--')
                ax.legend(loc='upper right', facecolor='#0b1a2a', edgecolor='white', labelcolor='white')

                plt.tight_layout()

                plt.show()
                plt.close('all')

                time.sleep(1.5)
                print("\n" + "="*65)
                input(" [PAUSA] Clique nesta linha e aperte ENTER para voltar ao menu: ")

            case 5:
                print("\nEncerrando sistema...")
                break

iniciar_sistema()
