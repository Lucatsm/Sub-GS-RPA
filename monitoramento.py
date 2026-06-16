# faça um pip install pandas openpyxl psutil antes de rodar os scripts se preferir tambem utilize um venv

import pandas as pd
from pathlib import Path
import datetime

def monitorar_processos_embarcados(arquivo_csv: str = "processos_embarcados.csv"):
    """Lê o arquivo CSV de processos embarcados e gera relatório de monitoramento."""
    
    # Tenta encontrar o arquivo na pasta telemetria_recebida
    caminho = Path(arquivo_csv)
    if not caminho.exists():
        caminho = Path("telemetria_recebida") / arquivo_csv
        if not caminho.exists():
            print(f"❌ Arquivo não encontrado: {arquivo_csv}")
            return None
    
    # Lê o CSV
    df = pd.read_csv(caminho)
    
    print(f"✅ Arquivo carregado: {caminho.name}")
    print(f"📊 Total de processos: {len(df)}")
    
    # Análises principais
    analise = {
        'Data_Analise': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'Total_Processos': len(df),
        'Processos_Ativos': len(df[df['state'] == 'R']),  # Running
        'CPU_Media': round(df['cpu_pct'].mean(), 2),
        'CPU_Max': df['cpu_pct'].max(),
        'Memoria_Media_pct': round(df['mem_pct'].mean(), 2),
        'Memoria_Max_pct': df['mem_pct'].max(),
    }
    
    # Processos por subsistema
    por_subsystem = df.groupby('subsystem').agg({
        'cpu_pct': 'mean',
        'mem_pct': 'mean',
        'pid': 'count'
    }).round(2)
    por_subsystem = por_subsystem.rename(columns={'pid': 'quantidade'})
    
    # Processos com maior consumo
    top_cpu = df.nlargest(5, 'cpu_pct')[['process_name', 'subsystem', 'cpu_pct', 'mem_pct', 'state']]
    
    # Salvar relatório
    nome_relatorio = f"RELATORIO_MONITORAMENTO_{datetime.datetime.now():%Y%m%d_%H%M%S}.txt"
    
    with open(nome_relatorio, "w", encoding="utf-8") as f:
        f.write("=== RELATÓRIO DE MONITORAMENTO DE PROCESSOS EMBARCADOS ===\n\n")
        f.write(f"Data da Análise: {analise['Data_Analise']}\n")
        f.write(f"Arquivo Origem: {caminho.name}\n\n")
        
        f.write("--- Resumo Geral ---\n")
        for key, value in analise.items():
            f.write(f"{key}: {value}\n")
        
        f.write("\n--- Processos por Subsistema ---\n")
        f.write(por_subsystem.to_string())
        
        f.write("\n\n--- Top 5 Processos por Uso de CPU ---\n")
        f.write(top_cpu.to_string(index=False))
    
    # Mostrar no terminal
    print(f"\n🎯 Resumo do Monitoramento:")
    print(f"   Total de Processos: {analise['Total_Processos']}")
    print(f"   CPU Média: {analise['CPU_Media']}%")
    print(f"   Memória Média: {analise['Memoria_Media_pct']}%")
    print(f"   Processos em Execução (R): {analise['Processos_Ativos']}")
    print(f"\n📁 Relatório completo salvo em: {nome_relatorio}")
    
    return df, analise


if __name__ == "__main__":
    monitorar_processos_embarcados()