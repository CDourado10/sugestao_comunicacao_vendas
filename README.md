# Sistema de Sugestão de Comunicação Comercial (Bluetech – PoC)

Este repositório contém uma **prova de conceito** de um assistente que apoia vendedores da Bluetech no relacionamento com clientes via WhatsApp, gerando respostas personalizadas de acordo com o histórico do cliente.

A aplicação foi construída em **Python** utilizando o framework **[Chainlit](https://chainlit.io/)** para a interface interativa.

---

## ⚙️ Funcionalidades

| Recurso | Estado |
|---------|--------|
| Banco de dados simulado em memória | ✅ |
| Carregamento de perfil e histórico do cliente | ✅ |
| Geração simples de sugestão de resposta (heurística) | ✅ |
| Interface web Chainlit (hot-reload) | ✅ |
| Integração real com WhatsApp API | ❌ (a implementar) |
| Uso de LLM para sugestões | ❌ |
| Persistência em banco de dados real | ❌ |

---

## 🖥️ Pré-requisitos

* Python 3.11+
* `pip install chainlit`
* (Opcional) Ambiente virtual: `python -m venv .venv && .venv\Scripts\activate`

---

## 🚀 Como executar

```bash
# 1. Instale dependência principal
pip install chainlit

# 2. Rode a aplicação com auto-reload
chainlit run cl_app.py -w
```

Abra o navegador em `http://localhost:8000`.

---

## 🧪 Teste rápido

Digite um dos IDs abaixo quando solicitado e envie mensagens de teste:

| ID | Cliente | Interesses |
|----|---------|------------|
| `c001` | Marcelo Tavares | Película automotiva Window Blue 50%, Linha Ultra Performance |
| `c002` | Ana Paula | Película de segurança 8 mil, Linha Comum Segurança |
| `c003` | Carlos Lima | Película Nano Carbono Residencial, Linha Alta Performance |

O sistema exibirá o perfil, o histórico recente e sugestões de resposta baseadas em heurísticas simples (palavras-chave como **desconto**, **garantia**, **instalação** etc.).

---

## 🗂️ Estrutura básica

```
├─ cl_app.py          # Código principal Chainlit (UI + lógica)
├─ suporte_comunicacao_comercial.txt  # Documento de escopo
├─ .gitignore
└─ README.md          # (este arquivo)
```

---

## 🔭 Próximos passos / Roadmap

1. Conectar a **WhatsApp Business API** (ou Twilio/Z-API) para ingestão de mensagens reais.
2. Persistir dados em um **PostgreSQL** ou MongoDB.
3. Substituir heurísticas por **LLM** (OpenAI GPT-4o ou modelo local) para sugestões contextuais.
4. Implementar dashboard e feedback loop para aprendizado contínuo.
5. Adicionar testes automatizados e CI.

---

## 🤝 Contribuições

Pull requests são bem-vindos! Abra também *issues* para reportar problemas ou sugerir funcionalidades.

---

## 📄 Licença

Projeto disponibilizado sob a licença MIT. Consulte o arquivo `LICENSE` (a ser incluído).
