import requests
import time
import numpy as np
import matplotlib.pyplot as plt
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

URL_r1 = "https://2ycz4yvc4h.execute-api.sa-east-1.amazonaws.com/dev/sobreviventes"
METHOD_R1 = "POST"

URL_r2 = "https://2ycz4yvc4h.execute-api.sa-east-1.amazonaws.com/dev/sobreviventes"
METHOD_R2 = "GET"

URL_r3 = "https://2ycz4yvc4h.execute-api.sa-east-1.amazonaws.com/dev/sobreviventes/123"
METHOD_R3 = "GET"

URL_r4 = "https://2ycz4yvc4h.execute-api.sa-east-1.amazonaws.com/dev/sobreviventes/123"
METHOD_R4 = "DELETE"
TOTAL_REQUESTS = 100

JSON_FILE = "src/config/teste.json"
with open(JSON_FILE, "r", encoding="utf-8") as f:
    payload = json.load(f)

HEADERS = {
    "Content-Type": "application/json"
}

# Função para realizar uma requisição e medir a latência de uma transação
def make_request(URL, METHOD):
    start_time = time.time()
    status = None

    try:
        if METHOD == "POST":
            response = requests.post(
                URL,
                headers=HEADERS,
                json=payload,
                timeout=10
            )
            status = response.status_code
        elif METHOD == "GET":
            response = requests.get(
                URL,
                headers=HEADERS,
                timeout=10
            )
            status = response.status_code
        elif METHOD == "DELETE":
            response = requests.delete(
                URL,
                headers=HEADERS,
                timeout=10
            )
            status = response.status_code
    except Exception:
        status = None

    end_time = time.time()
    latency_ms = (end_time - start_time) * 1000

    return latency_ms, status

latencies_r1 = []
latencies_r2 = []
latencies_r3 = []
latencies_r4 = []
for i in range(TOTAL_REQUESTS):
    latency, status = make_request(URL_r1, METHOD_R1)
    latencies_r1.append(latency)
    print(f"Request R1 {i+1}/{TOTAL_REQUESTS} - Latency: {latency:.2f} ms - Status: {status}")

    latency, status = make_request(URL_r2, METHOD_R2)
    latencies_r2.append(latency)
    print(f"Request R2 {i+1}/{TOTAL_REQUESTS} - Latency: {latency:.2f} ms - Status: {status}")

    latency, status = make_request(URL_r3, METHOD_R3)
    latencies_r3.append(latency)
    print(f"Request R3 {i+1}/{TOTAL_REQUESTS} - Latency: {latency:.2f} ms - Status: {status}")

    latency, status = make_request(URL_r4, METHOD_R4)
    latencies_r4.append(latency)
    print(f"Request R4 {i+1}/{TOTAL_REQUESTS} - Latency: {latency:.2f} ms - Status: {status}")

fig, axes = plt.subplots(4, 1, figsize=(10, 12))

axes[0].plot(latencies_r1, label='R1 - POST', marker='o', linestyle='-', color='blue')
axes[0].set_title('Gráfico 1: Chamada do Modelo', fontsize=12, fontweight='bold')
axes[0].set_xlabel('Latência (ms) - P90: {:.2f} ms | P99: {:.2f} ms'.format(np.percentile(latencies_r1, 90), np.percentile(latencies_r1, 99)))
axes[0].set_ylabel('Frequência')
axes[0].grid(True, alpha=0.3, axis='y')

axes[1].plot(latencies_r2, label='R2 - GET', marker='s', linestyle='--', color='green')
axes[1].set_title('Gráfico 2: Consulta do resultado', fontsize=12, fontweight='bold')
axes[1].set_xlabel('Latência (ms) - P90: {:.2f} ms | P99: {:.2f} ms'.format(np.percentile(latencies_r2, 90), np.percentile(latencies_r1, 99)))
axes[1].set_ylabel('Frequência')
axes[1].grid(True, alpha=0.3, axis='y')

axes[2].plot(latencies_r3, label='R3 - GET', marker='^', linestyle='-.', color='red')
axes[2].set_title('Gráfico 3: Consulta de ID', fontsize=12, fontweight='bold')
axes[2].set_xlabel('Latência (ms) - P90: {:.2f} ms | P99: {:.2f} ms'.format(np.percentile(latencies_r3, 90), np.percentile(latencies_r3, 99)))
axes[2].set_ylabel('Frequência')
axes[2].grid(True, alpha=0.3, axis='y')

axes[3].plot(latencies_r4, label='R4 - DELETE', marker='d', linestyle=':', color='orange')
axes[3].set_title('Gráfico 4: Deleção de Registro', fontsize=12, fontweight='bold')
axes[3].set_xlabel('Latência (ms) - P90: {:.2f} ms | P99: {:.2f} ms'.format(np.percentile(latencies_r4, 90), np.percentile(latencies_r4, 99)))
axes[3].set_ylabel('Frequência')
axes[3].grid(True, alpha=0.3, axis='y')

# Ajustar espaçamento entre subplots
plt.tight_layout()

# Salvar figura
plt.savefig('images/latency_distribution_onerequest.png', dpi=150, bbox_inches='tight')
print("Gráficos salvos como 'latency_distribution_onerequest.png'")




