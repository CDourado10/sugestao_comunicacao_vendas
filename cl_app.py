import chainlit as cl
from datetime import datetime

# ----------------------------
# Banco de dados SIMULADO
# ----------------------------
# Cada cliente possui um histórico de mensagens e um perfil resumido.
FAKE_DB = {
    "c001": {
        "profile": {
            "nome": "Marcelo Tavares",
            "preferencia_tom": "informal",
            "interesses": ["película automotiva Window Blue 50%", "linha ultra performance"],
            "ultima_compra": "2025-06-15",
        },
        "messages": [
            {"ts": "2025-07-03 09:10", "from": "cliente", "content": "Bom dia! Qual é a garantia da película Window Blue 50%?"},
            {"ts": "2025-07-03 09:15", "from": "vendedor", "content": "Olá Marcelo! A garantia é de 10 anos contra desbotamento."},
        ],
    },
    "c002": {
        "profile": {
            "nome": "Ana Paula",
            "preferencia_tom": "formal",
            "interesses": ["película de segurança 8 mil", "linha comum segurança"],
            "ultima_compra": "2025-05-28",
        },
        "messages": [
            {"ts": "2025-07-02 16:20", "from": "cliente", "content": "Boa tarde, preciso de uma película de segurança para vitrine, vocês têm a 8 mil?"},
        ],
    },
    "c003": {
        "profile": {
            "nome": "Carlos Lima",
            "preferencia_tom": "informal",
            "interesses": ["película nano carbono residencial", "linha alta performance"],
            "ultima_compra": "2025-04-12",
        },
        "messages": [
            {"ts": "2025-07-01 11:05", "from": "cliente", "content": "Oi, a nano carbono reduz muito o calor?"},
            {"ts": "2025-07-01 11:07", "from": "vendedor", "content": "Olá Carlos! Reduz até 80% da energia solar."},
        ],
    },
}

# ----------------------------
# Funções auxiliares
# ----------------------------

def format_history(msgs: list[dict]) -> str:
    """Converte o histórico de mensagens em texto legível."""
    lines = []
    for m in msgs[-5:]:  # mostra no máximo as 5 últimas
        who = "Você" if m["from"] == "vendedor" else "Cliente"
        lines.append(f"[{m['ts']}] {who}: {m['content']}")
    return "\n".join(lines)


def generate_suggestion(client_id: str, last_user_content: str | None = None) -> str:
    """Gera sugestão simples baseada no perfil e última mensagem."""
    client = FAKE_DB.get(client_id)
    if not client:
        return "Cliente não encontrado."

    perfil = client["profile"]
    name = perfil["nome"]
    tom = perfil["preferencia_tom"]
    # Heurística muito simples para prova de conceito
    saudacao = "Oi" if tom == "informal" else "Olá"
    intro = f"{saudacao} {name.split()[0]}, tudo bem?"

    if last_user_content:
        text = last_user_content.lower()
        if "desconto" in text or "preço" in text or "valor" in text:
            corpo = "Temos uma condição especial esta semana: 10% OFF e frete grátis na instalação. Posso enviar o orçamento detalhado?"
        elif "garantia" in text:
            corpo = "Nossas películas contam com garantia de 10 anos contra desbotamento e delaminação. Gostaria que eu envie o certificado de garantia?"
        elif "instalação" in text or "agendar" in text:
            corpo = "Podemos agendar a instalação com nossa equipe certificada. Qual data funciona melhor para você?"
        else:
            interesses = ", ".join(perfil["interesses"])
            corpo = f"Vi que você tem interesse em {interesses}. Gostaria de receber mais informações ou amostras?"
    else:
        interesses = ", ".join(perfil["interesses"])
        corpo = f"Vi que você tem interesse em {interesses}. Gostaria de receber mais informações?"

    fechamento = "Fico à disposição!" if tom == "informal" else "Estou à disposição para auxiliá-la."
    return f"{intro} {corpo} {fechamento}"

# ----------------------------
# Hooks Chainlit
# ----------------------------

@cl.on_chat_start
async def chat_start():
    """Solicita o ID do cliente assim que o vendedor abre o chat."""
    await cl.Message(
        content="Bem-vindo! Por favor, digite o ID do cliente (ex.: c001) para carregar o histórico.",
    ).send()

@cl.on_message
async def main(message: cl.Message):
    user_session = cl.user_session

    # Se ainda não temos cliente salvo, interpretar primeira mensagem como ID
    client_id = user_session.get("client_id")
    if client_id is None:
        client_id = message.content.strip()
        if client_id not in FAKE_DB:
            await cl.Message(content="ID não encontrado. Tente novamente.").send()
            return
        user_session.set("client_id", client_id)

        history = FAKE_DB[client_id]["messages"]
        profile = FAKE_DB[client_id]["profile"]

        # Envia resumo do perfil
        await cl.Message(
            content=(
                f"Perfil do cliente: {profile['nome']}\n"
                f"Preferência de tom: {profile['preferencia_tom']}\n"
                f"Interesses: {', '.join(profile['interesses'])}\n"
                f"Última compra: {profile['ultima_compra']}"
            )
        ).send()

        # Envia histórico recente
        await cl.Message(
            content="Histórico recente:\n" + format_history(history)
        ).send()
        return

    # Já temos client_id salvo – gerar sugestão de resposta
    suggestion = generate_suggestion(client_id, message.content)

    # Exibe sugestão ao vendedor
    await cl.Message(
        content="Sugestão de resposta:\n" + suggestion,
    ).send()

    # Opcional: registrar que sugestão foi gerada (simulado)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    FAKE_DB[client_id]["messages"].append({"ts": now, "from": "vendedor", "content": suggestion})
