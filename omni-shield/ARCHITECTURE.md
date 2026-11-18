# Omni-Shield · Arquitetura

## Visão geral
Console de segurança com cinco módulos e um modo autônomo de crise. Roda como app web (abre no celular e no PC) e foi pensado para ser empacotado sobre Linux (container ou kiosk).

```
[ Interface blindada (HTML/JS, CSP restrita) ]
        |                    |
 [ Telemetria local ]   [ Roteador de IA ]──> GroqCloud
        |                 leve: gpt-oss-20b
 [ Módulos de painel ]   potente: gpt-oss-120b
```

## Camadas
1. **Interface**: arquivo único, sem dependências externas, chave guardada só no aparelho.
2. **Roteador de IA**: pontua a complexidade da tarefa (palavras-chave, tamanho, código). Pontuação < 2 vai ao modelo leve; ≥ 2, ou modo autônomo, vai ao potente. Mede a latência de cada chamada.
3. **Módulos**
   - **Monitoramento Neuromórfico**: triagem esparsa de eventos; o núcleo principal só acorda em picos acima do limiar (linha vermelha).
   - **Núcleo Híbrido MoE-SSM**: mostra especialistas ativos (2/16 em repouso, 6–10 sob ameaça), processamento linear O(n) e status da trilha autocrítica.
   - **Mapeamento Quântico Assíncrono**: indicador de sincronização e otimização de pesos.
   - **Radar de Inteligência Competitiva**: feed de tendências públicas, com síntese por IA restrita a informação aberta.
   - **Financeiro e Defesa**: série de mercado com previsão por tendência, latência e contador de pentest com escopo fixo em localhost.
4. **Modo autônomo**: acelera a telemetria, prioriza o modelo potente e registra respostas automáticas no feed.

## Honestidade técnica
Neuromórfico, quântico, mercado e pentest exibem **dados simulados** no navegador. Para virar real:
- Telemetria: ligar a `auditd`/`eBPF` ou Suricata num servidor Linux e enviar por WebSocket.
- Mercado: API de cotações (ex.: Alpha Vantage, Brapi).
- Pentest: só em sistemas próprios ou com autorização por escrito (ex.: `nmap` no próprio host).
- Quântico: não existe acesso público em tempo real; hoje seria uma integração com IBM Quantum ou Amazon Braket em lote.

## Próximos passos
- Backend em FastAPI reutilizando `router.py` e escondendo a chave no servidor.
- Empacotar como app Android (PWA ou Capacitor).
