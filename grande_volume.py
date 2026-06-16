# faça um pip install pandas openpyxl psutil antes de rodar os scripts se preferir tambem utilize um venv

import pandas as pd
from pathlib import Path
import json

def processar_arquivos_telemetria(pasta_entrada: str = "telemetria_recebida"):
    """Processa arquivos de telemetria (CSV, JSON e Excel) com foco no arquivo JSON grande."""
    
    pasta = Path(pasta_entrada)
    arquivos = list(pasta.glob("*.csv")) + list(pasta.glob("*.json")) + list(pasta.glob("*.xlsx"))
    
    if not arquivos:
        print("❌ Nenhum arquivo encontrado na pasta telemetria_recebida/")
        return None
    
    dados_consolidados = []
    
    for arquivo in arquivos:
        try:
            print(f"📂 Processando: {arquivo.name}")
            
            if arquivo.suffix == ".json":
                # Tratamento especial para o arquivo JSON grande
                with open(arquivo, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Extrai os registros (o que realmente importa)
                records = data.get('records', [])
                if records:
                    df = pd.json_normalize(records, sep='_')
                    print(f"   ✅ JSON processado: {len(df)} registros extraídos")
                else:
                    print("   ⚠️ Nenhum registro encontrado no JSON")
                    continue
                    
            elif arquivo.suffix == ".csv":
                df = pd.read_csv(arquivo)
            else:  # Excel
                df = pd.read_excel(arquivo)
            
            # Padronização de colunas
            df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
            
            # Adiciona metadados
            df['arquivo_origem'] = arquivo.name
            df['data_processamento'] = pd.Timestamp.now()
            
            dados_consolidados.append(df)
            
        except Exception as e:
            print(f"⚠️ Erro ao processar {arquivo.name}: {e}")
    
    if dados_consolidados:
        consolidado = pd.concat(dados_consolidados, ignore_index=True)
        
        nome_saida = f"CONSOLIDADO_TELEMETRIA_{pd.Timestamp.now():%Y%m%d_%H%M%S}.csv"
        consolidado.to_csv(nome_saida, index=False, encoding='utf-8')
        
        print(f"\n🎉 Processamento finalizado com sucesso!")
        print(f"📊 Total de registros consolidados: {len(consolidado):,}")
        print(f"📁 Arquivo salvo: {nome_saida}")
        
        # Mostrar algumas estatísticas úteis
        if 'thermal_obc_temp_c' in consolidado.columns:
            print(f"🌡️ Temperatura OBC média: {consolidado['thermal_obc_temp_c'].mean():.2f}°C")
        if 'power_battery_soc_pct' in consolidado.columns:
            print(f"🔋 SOC Bateria médio: {consolidado['power_battery_soc_pct'].mean():.2f}%")
        
        return consolidado
    return None

if __name__ == "__main__":
    processar_arquivos_telemetria()