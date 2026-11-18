"""Roteador de tarefas GroqCloud: modelo leve para tarefas simples,
modelo potente so para demandas complexas, com monitoramento de latencia."""
import os, re, time, json, statistics
from groq import Groq

LEVE = os.getenv("MODELO_LEVE", "openai/gpt-oss-20b")
POTENTE = os.getenv("MODELO_POTENTE", "openai/gpt-oss-120b")
client = Groq(api_key=os.environ["GROQ_API_KEY"])

PALAVRAS_COMPLEXAS = [
    "analise", "analisa", "compare", "explique detalhadamente", "passo a passo",
    "codigo", "código", "programa", "algoritmo", "debug", "otimize", "arquitetura",
    "prove", "demonstre", "estrategia", "estratégia", "plano", "resuma o texto",
    "raciocine", "calcule", "matematica", "matemática", "refatore",
]

def complexidade(tarefa: str) -> int:
    t = tarefa.lower()
    pontos = 0
    pontos += sum(2 for p in PALAVRAS_COMPLEXAS if p in t)
    pontos += len(t.split()) // 25          # textos longos pesam mais
    pontos += t.count("?") > 1               # varias perguntas
    pontos += 2 if re.search(r"```|def |class |function", t) else 0
    return pontos

def rotear(tarefa: str) -> str:
    return POTENTE if complexidade(tarefa) >= 2 else LEVE

def executar(tarefa: str, modelo: str | None = None) -> dict:
    modelo = modelo or rotear(tarefa)
    inicio = time.perf_counter()
    r = client.chat.completions.create(
        model=modelo,
        messages=[{"role": "user", "content": tarefa}],
        max_tokens=400,
    )
    lat = time.perf_counter() - inicio
    return {
        "tarefa": tarefa[:60], "modelo": modelo, "latencia_s": round(lat, 3),
        "tokens": r.usage.completion_tokens if r.usage else None,
        "resposta": r.choices[0].message.content.strip()[:200],
    }

if __name__ == "__main__":
    tarefas = [
        "Qual é a capital da França?",
        "Traduza 'bom dia' para inglês.",
        "Diga um sinônimo de feliz.",
        "Analise passo a passo a complexidade de um algoritmo de ordenação quicksort e compare com mergesort.",
        "Escreva um código Python que implemente uma fila com prioridade e explique detalhadamente a arquitetura.",
    ]
    print("== Teste de inferencia ==")
    roteado, sempre_potente = [], []
    for t in tarefas:
        a = executar(t)                     # com roteamento
        b = executar(t, POTENTE)            # sem roteamento (sempre o maior)
        roteado.append(a["latencia_s"]); sempre_potente.append(b["latencia_s"])
        print(json.dumps(a, ensure_ascii=False))
        print(f"   sem roteamento ({POTENTE}): {b['latencia_s']}s")
    print("\n== Latencia ==")
    print(f"Com roteamento:  total {sum(roteado):.2f}s | media {statistics.mean(roteado):.2f}s")
    print(f"Sempre potente:  total {sum(sempre_potente):.2f}s | media {statistics.mean(sempre_potente):.2f}s")
    ganho = (1 - sum(roteado) / sum(sempre_potente)) * 100
    print(f"Ganho de velocidade: {ganho:.1f}%")
