from flask import Flask, render_template
import psutil
import platform
from datetime import datetime

app = Flask(__name__)

def get_system_info():
    return {
        "Sistema Operacional": platform.system(),
        "Versão": platform.version(),
        "Plataforma": platform.platform(),
        "Processador": platform.processor(),
        "Arquitetura": platform.architecture()[0],
        "Data de Inicialização": datetime.fromtimestamp(psutil.boot_time()).strftime("%d/%m/%Y %H:%M:%S"),
    }

def get_cpu_info():
    return {
        "Uso de CPU (%)": psutil.cpu_percent(interval=1),
        "Núcleos Físicos": psutil.cpu_count(logical=False),
        "Núcleos Lógicos": psutil.cpu_count(logical=True),
    }

def get_memory_info():
    memory = psutil.virtual_memory()
    return {
        "Total (GB)": round(memory.total / (1024 ** 3), 2),
        "Disponível (GB)": round(memory.available / (1024 ** 3), 2),
        "Usada (GB)": round(memory.used / (1024 ** 3), 2),
        "Uso (%)": memory.percent,
    }

def get_disk_info():
    disk = psutil.disk_usage('/')
    return {
        "Total (GB)": round(disk.total / (1024 ** 3), 2),
        "Usado (GB)": round(disk.used / (1024 ** 3), 2),
        "Livre (GB)": round(disk.free / (1024 ** 3), 2),
        "Uso (%)": disk.percent,
    }

@app.route('/')
def index():
    system_info = get_system_info()
    cpu_info = get_cpu_info()
    memory_info = get_memory_info()
    disk_info = get_disk_info()

    return render_template('index.html',
                           system_info=system_info,
                           cpu_info=cpu_info,
                           memory_info=memory_info,
                           disk_info=disk_info)

if __name__ == "__main__":
    app.run(debug=True)
