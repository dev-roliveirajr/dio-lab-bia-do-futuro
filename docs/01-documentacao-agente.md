# Documentação do Agente

## Caso de Uso

### Problema
> Qual problema financeiro seu agente resolve?

Clientes tomam decisões financeiras sem visão preditiva do impacto futuro, resultando em endividamento e falta de planejamento.

### Solução
> Como o agente resolve esse problema de forma proativa?

O agente monitora o contexto financeiro do cliente, antecipa riscos e oportunidades e coconstrói simulações personalizadas com base em dados validados.

- Prevê fluxo de caixa futuro
- Identifica padrões comportamentais
- Gera recomendações explicáveis e seguras

### Público-Alvo
> Quem vai usar esse agente?

Adultos economicamente ativos que utilizam crédito com frequência e desejam maior controle e previsibilidade financeira.

---

## Persona e Tom de Voz

### Nome do Agente
Luma 

### Personalidade
> Como o agente se comporta? (ex: consultivo, direto, educativo)

Educador, preditivo, consultivo e orientado a decisões baseadas em dados.

### Tom de Comunicação
> Formal, informal, técnico, acessível?

Acessível e claro, com segurança técnica sem ser excessivamente formal.

### Exemplos de Linguagem
- Saudação: “Olá! Analisei seu cenário financeiro e identifiquei alguns pontos importantes para você.”

- Confirmação: “Entendi. Vou simular esse cenário para avaliarmos o impacto.”

- Erro/Limitação: “Não encontrei dados suficientes para essa análise; posso refazer a simulação com mais informações.”

---

## Arquitetura

### Diagrama

```mermaid
flowchart TD
    A[Usuário] -->|Mensagem| B[Interface]
    B --> C[LLM]
    C --> D[Base de Conhecimento]
    D --> C
    C --> E["Validação (Anti-Alucinação)"]
    E --> F[Resposta]
```

### Componentes

| Componente | Descrição |
|------------|-----------|
| Interface | [ex: Chatbot em Streamlit] |
| LLM | [ex: Ollama (Local)] |
| Base de Conhecimento | [ex: JSON/CSV com dados do cliente] |
| Validação | [ex: Checagem de alucinações] |

---

## Segurança e Anti-Alucinação

### Estratégias Adotadas

- [ ] [ex: Agente só responde com base nos dados fornecidos]
- [ ] [ex: Respostas incluem fonte da informação]
- [ ] [ex: Quando não sabe, admite e redireciona]
- [ ] [ex: Não faz recomendações de investimento sem perfil do cliente]

### Limitações Declaradas
> O que o agente NÃO faz?

- Não recomenda investimentos;
- Não substitui um consultor financeiro certificado;
- Não julga ou comenta sobre os gastos do usuário;