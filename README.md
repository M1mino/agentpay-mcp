# AgentPay MCP Server

MCP сервер для [AgentPay](https://github.com/M1mino/agentpay) — платёжного слоя AI-агентов.

Позволяет любому MCP-совместимому агенту (Claude Code, Codex, Cline, Hermes, OpenClaw) проверять баланс, регистрироваться и переводить CREDIT через EIP-191 подписи.

## Инструменты

| Инструмент | Описание |
|-----------|----------|
| `get_balance` | Баланс агента по адресу (0x...) |
| `register` | Регистрация нового агента |
| `pay` | Перевод CREDIT с EIP-191 подписью |
| `audit` | Статистика системы (USDC, CREDIT, агенты) |

## Подключение

```json
{
  "mcpServers": {
    "agentpay": {
      "url": "http://localhost:8005/mcp"
    }
  }
}
```

## Требования

- Python 3.11+
- AgentPay сервер на порту 8004 (или `AGENTPAY_URL`)

## Установка

```bash
pip install -r requirements.txt
python server.py
```
