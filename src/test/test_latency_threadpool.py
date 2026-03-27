import requests
import time
import numpy as np
import matplotlib.pyplot as plt
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

URL = "https://2ycz4yvc4h.execute-api.sa-east-1.amazonaws.com/dev/sobreviventes"
TOTAL_REQUESTS = 10000
CONCURRENCY = 200  # número de requisições simultâneas

JSON_FILE = "src/config/teste.json"
with open(JSON_FILE, "r", encoding="utf-8") as f:
    payload = json.load(f)

HEADERS = {
    "Content-Type": "application/json"
}

# Função para realizar uma requisição e medir a latência
def make_request(session):
    start_time = time.time()
    status = None

    try:
        response = session.post(
            URL,
            headers=HEADERS,
            json=payload,
            timeout=10
        )
        status = response.status_code
    except Exception:
        status = None

    end_time = time.time()
    latency_ms = (end_time - start_time) * 1000

    return latency_ms, status

latencies = []
status_codes = []

print(f"Iniciando teste: {TOTAL_REQUESTS} requests | concorrência={CONCURRENCY}")

start_test = time.time()

# Função que irá realizar as requisições em paralelo usando ThreadPoolExecutor
# - Ele cria uma fila de 10000 tarefas
# - O ThreadPoolExecutor roda 200 em paralelo
# - Quando uma termina → entra outra
# - Isso continua até completar as 10000

with ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
    with requests.Session() as session:
        futures = [executor.submit(make_request, session) for _ in range(TOTAL_REQUESTS)]

        for i, future in enumerate(as_completed(futures)):
            latency, status = future.result()
            latencies.append(latency)
            status_codes.append(status)

            if (i + 1) % 100 == 0:
                print(f"{i + 1} concluídas")

end_test = time.time()

# Geração das Métricas
total_time = end_test - start_test
latencies = np.array(latencies)

p90 = np.percentile(latencies, 90)
p99 = np.percentile(latencies, 99)
rps = TOTAL_REQUESTS / total_time

success_rate = sum(1 for s in status_codes if s == 200) / len(status_codes)

print("\n===== RESULTADOS =====")
print(f"Tempo total: {total_time:.2f}s")
print(f"RPS: {rps:.2f}")
print(f"P90: {p90:.2f} ms")
print(f"P99: {p99:.2f} ms")
print(f"Sucesso (200): {success_rate * 100:.2f}%")

# Análise dos resultados
sorted_latencies = np.sort(latencies)

plt.figure()

plt.plot(sorted_latencies, label="Latência (ms)")
plt.axhline(p90, linestyle='--', label=f"P90 = {p90:.2f} ms")
plt.axhline(p99, linestyle='--', label=f"P99 = {p99:.2f} ms")

plt.title(f"Teste de Latência (Concorrência={CONCURRENCY})")
plt.xlabel("Requisições (ordenadas)")
plt.ylabel("Latência (ms)")
plt.legend()
plt.grid()

output_file = "images/latency_parallel.png"
plt.savefig(output_file)

print(f"Gráfico salvo em: {output_file}")