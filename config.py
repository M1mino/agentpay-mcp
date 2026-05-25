"""AgentPay MCP Server — Configuration."""

import os

# MCP server
MCP_HOST = os.getenv("MCP_HOST", "0.0.0.0")
MCP_PORT = int(os.getenv("MCP_PORT", "8005"))

# AgentPay REST API (локальный)
AGENTPAY_URL = os.getenv("AGENTPAY_URL", "http://localhost:8004")
