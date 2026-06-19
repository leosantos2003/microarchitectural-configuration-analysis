import pandas as pd
import matplotlib.pyplot as plt
import os

# Caminho dos dados (como o script está em "novo_teste", busca direto em "Resultados")
caminho_dados = 'Resultados'
pasta_saida = 'Gráficos'

# Cria a pasta de saída se ela não existir
if not os.path.exists(pasta_saida):
    os.makedirs(pasta_saida)
    print(f"Pasta '{pasta_saida}' criada com sucesso.")

# Dicionário mapeando os arquivos CSV e os detalhes de como plotar cada um
arquivos_config = {
    'CacheSize_time.csv': {'param': 'size', 'ylabel': 'Tempo de Execução (s)', 'title': 'Desempenho: Tempo de Exec. vs Tamanho da Cache', 'out': 'Grafico_CacheSize_Tempo.png'},
    'CacheSize_IPC.csv': {'param': 'size', 'ylabel': 'IPC', 'title': 'Desempenho: IPC vs Tamanho da Cache', 'out': 'Grafico_CacheSize_IPC.png'},
    'FetchBuffer_time.csv': {'param': 'buffer-size', 'ylabel': 'Tempo de Execução (s)', 'title': 'Desempenho: Tempo de Exec. vs Fetch Buffer', 'out': 'Grafico_FetchBuffer_Tempo.png'},
    'FetchBuffer_IPC.csv': {'param': 'buffer-size', 'ylabel': 'IPC', 'title': 'Desempenho: IPC vs Fetch Buffer', 'out': 'Grafico_FetchBuffer_IPC.png'},
    'CacheAssociativity_time.csv': {'param': 'associativity', 'ylabel': 'Tempo de Execução (s)', 'title': 'Desempenho: Tempo de Exec. vs Associatividade da Cache', 'out': 'Grafico_Associativity_Tempo.png'},
    'CacheAssociativity_IPC.csv': {'param': 'associativity', 'ylabel': 'IPC', 'title': 'Desempenho: IPC vs Associatividade da Cache', 'out': 'Grafico_Associativity_IPC.png'},
}

def plot_metric(caminho_csv, config):
    if not os.path.exists(caminho_csv):
        print(f"Aviso: O arquivo {caminho_csv} não foi encontrado. Pulando...")
        return

    # Lê o CSV
    df = pd.read_csv(caminho_csv)
    
    plt.figure(figsize=(9, 6))
    
    # Programas base
    programs = ['bubblesort', 'fft', 'matrix-mult']
    
    # Filtra apenas os programas que realmente existem nas colunas do CSV
    valid_progs = [p for p in programs if p in df.columns]
    
    # Calcula a média (média da linha considerando os três algoritmos)
    if valid_progs:
        df['Média Global'] = df[valid_progs].mean(axis=1)
    
    # Converte o eixo X para string para que os níveis fiquem espaçados uniformemente
    param_col = config['param']
    x_vals = df[param_col].astype(str)
    
    # Desenha a linha para cada programa individual (com leve transparência para destacar a média)
    for prog in valid_progs:
        plt.plot(x_vals, df[prog], marker='o', linewidth=2, markersize=7, alpha=0.6, label=prog)
        
    # Desenha a linha da Média (Destacada: Preta, tracejada e mais grossa)
    if 'Média Global' in df.columns:
        plt.plot(x_vals, df['Média Global'], marker='D', linewidth=3, markersize=8, 
                 color='black', linestyle='--', label='Média Global')
    
    # Embelezamento do Gráfico
    plt.title(config['title'], fontsize=14, fontweight='bold')
    plt.xlabel(f"{param_col.capitalize()} (Níveis)", fontsize=12)
    plt.ylabel(config['ylabel'], fontsize=12)
    plt.legend(title='Legenda', fontsize=10, loc='best')
    plt.grid(True, linestyle=':', alpha=0.8)
    plt.ticklabel_format(axis='y', style='plain')
    plt.tight_layout()
    
    # Salva o gráfico
    caminho_saida = os.path.join(pasta_saida, config['out'])
    plt.savefig(caminho_saida, dpi=150)
    plt.close()
    print(f"Gráfico salvo: {caminho_saida}")

# Executa a geração para cada arquivo configurado
print("Iniciando a geração dos gráficos...")
for arquivo_csv, config in arquivos_config.items():
    caminho_completo = os.path.join(caminho_dados, arquivo_csv)
    plot_metric(caminho_completo, config)

print("Processo finalizado com sucesso!")