# AgentPay MCP Server

Платёжный слой для AI-агентов через MCP протокол.

## Обзор

Проксирует запросы к AgentPay REST API. Агенты могут управлять CREDIT-балансами через EIP-191 подписи, не имея прямого доступа к AgentPay API.

## Инструменты

- `get_balance(agent_address)` — баланс CREDIT
- `register(agent_address)` — регистрация
- `pay(from, to, amount, signature, nonce)` — перевод
- `audit()` — статистика системы

## Формат подписи EIP-191

Для `pay` агент подписывает сообщение:
```
agentpay_v1:pay:{sender}:{recipient}:{amount}:{nonce}
```
Ключ подписи должен совпадать с `from_address`.

## Зависимости

- `mcp` — FastMCP сервер
- `httpx` — HTTP клиент к AgentPay

## Запуск

```
pip install -r requirements.txt
python server.py
```

Сервер стартует на порту 8005.
