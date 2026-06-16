# faça um pip install pandas openpyxl psutil antes de rodar os scripts se preferir tambem utilize um venv

import psutil
import datetime
import json
import time
from pathlib import Path

def monitorar_tarefas_sistema():
    """Monitora processos do sistema relacionados ao processamento de telemetria."""
    
    processos_relevantes = []
    agora = datetime.datetime.now()
    
    keywords = ['telemetria', 'satelite', 'missao', 'controle', 'python', 'pandas']
    
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status', 'cmdline']):
        try:
            pinfo = proc.info
            cmdline = ' '.join(pinfo.get('cmdline', [])).lower()
            
            if any(kw in (pinfo['name'] or '').lower() or kw in cmdline for kw in keywords) or \
               pinfo['cpu_percent'] > 8 or pinfo['memory_percent'] > 15:
                
                processos_relevantes.append({
                    'timestamp': agora.isoformat(),
                    'pid': pinfo['pid'],
                    'processo': pinfo['name'],
                    'cpu_percent': round(pinfo['cpu_percent'], 2),
                    'memoria_percent': round(pinfo['memory_percent'], 2),
                    'status': pinfo['status']
                })
        except:
            continue
    
    pasta_logs = Path("logs/monitoramento")
    pasta_logs.mkdir(parents=True, exist_ok=True)
    
    nome_arquivo = pasta_logs / f"monitoramento_{agora.strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        json.dump(processos_relevantes, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Monitoramento concluído - {len(processos_relevantes)} processos registrados.")
    return processos_relevantes

if __name__ == "__main__":
    print("🚀 Iniciando Monitoramento de Tasks...")
    while True:
        monitorar_tarefas_sistema()
        time.sleep(60)