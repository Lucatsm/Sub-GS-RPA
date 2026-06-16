# faça um pip install pandas openpyxl psutil antes de rodar os scripts se preferir tambem utilize um venv

import pandas as pd
from pathlib import Path

def processar_arquivos_telemetria(pasta_entrada: str = "telemetria_recebida"):
    """Processa arquivos de telemetria com foco em temperatura, consumo de energia,
    posicionamento orbital e estado dos equipamentos."""
    
    pasta = Path(pasta_entrada)
    arquivos = list(pasta.glob("*.csv")) + list(pasta.glob("*.json")) + list(pasta.glob("*.xlsx"))
    
    if not arquivos:
        print("❌ Nenhum arquivo de telemetria encontrado.")
        return None
    
    dados_consolidados = []
    
    for arquivo in arquivos:
        try:
            if arquivo.suffix == ".csv":
                df = pd.read_csv(arquivo)
            elif arquivo.suffix == ".json":
                df = pd.read_json(arquivo)
            else:
                df = pd.read_excel(arquivo)
            
            # Padronização de colunas
            df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
            
            # Adiciona metadados
            df['arquivo_origem'] = arquivo.name
            df['data_processamento'] = pd.Timestamp.now()
            
            dados_consolidados.append(df)
            print(f"✅ Processado: {arquivo.name} ({len(df)} registros)")
            
        except Exception as e:
            print(f"⚠️ Erro ao processar {arquivo.name}: {e}")
    
    if dados_consolidados:
        consolidado = pd.concat(dados_consolidados, ignore_index=True)
        
        # Análise básica dos campos principais
        relatorio = {
            "Total_Registros": len(consolidado),
            "Data_Processamento": pd.Timestamp.now(),
            "Temperatura_Media": round(consolidado['temperatura'].mean(), 2) if 'temperatura' in consolidado.columns else None,
            "Temperatura_Max": round(consolidado['temperatura'].max(), 2) if 'temperatura' in consolidado.columns else None,
            "Consumo_Energia_Total": round(consolidado['consumo_energia'].sum(), 2) if 'consumo_energia' in consolidado.columns else None,
            "Equipamentos_Anormais": len(consolidado[consolidado.get('estado_equipamento', '') == 'Anormal']) if 'estado_equipamento' in consolidado.columns else 0,
        }
        
        nome_saida = f"CONSOLIDADO_TELEMETRIA_{pd.Timestamp.now():%Y%m%d_%H%M%S}.csv"
        consolidado.to_csv(nome_saida, index=False, encoding='utf-8')
        
        print(f"\n🎉 Processamento concluído!")
        print(f"📊 Total de registros: {len(consolidado):,}")
        print(f"🌡️  Temperatura média: {relatorio['Temperatura_Media']}°C")
        print(f"⚡ Consumo total: {relatorio['Consumo_Energia_Total']} unidades")
        print(f"📁 Arquivo salvo: {nome_saida}")
        
        return consolidado
    return None

if __name__ == "__main__":
    processar_arquivos_telemetria()