#!/usr/bin/env python3
"""
AgentPay MCP Server — AI agents can check balances, register,
and transfer CREDIT via EIP-191 signatures.

Connects to AgentPay REST API (localhost:8004).
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp.server.fastmcp import FastMCP
from agentpay_client import AgentPayClient, AgentPayError
from config import MCP_HOST, MCP_PORT

# MCP server
mcp = FastMCP(
    "AgentPay MCP",
    instructions="Платёжный слой для AI-агентов. Проверка баланса, "
                 "регистрация, перевод CREDIT через подпись EIP-191.",
    host=MCP_HOST,
    port=MCP_PORT,
    sse_path="/sse",
    streamable_http_path="/mcp",
    mount_path="/",
)

# Client to AgentPay REST API
api = AgentPayClient()


# ─── Tools ─────────────────────────────────────

@mcp.tool(
    name="get_balance",
    description="Get the CREDIT balance of an agent by its Ethereum address. "
                "Address should start with 0x."
)
def get_balance(address: str) -> str:
    """Check agent's credit balance."""
    try:
        result = api.get_balance(address)
        balance = result.get("balance", 0)
        return (
            f"**Agent:** `{address[:15]}...`\n"
            f"**Balance:** {balance} CREDIT"
        )
    except AgentPayError as e:
        return f"❌ Error: {e}"


@mcp.tool(
    name="register",
    description="Register a new agent by its Ethereum address (0x...). "
                "Creates an account in AgentPay with zero balance."
)
def register(address: str) -> str:
    """Register a new agent."""
    try:
        result = api.register(address)
        return (
            f"✅ Agent `{result.get('agent_id', address[:15])}` "
            f"registered successfully!\n"
            f"**Balance:** 0 CREDIT"
        )
    except AgentPayError as e:
        return f"❌ Error: {e}"


@mcp.tool(
    name="pay",
    description="Transfer CREDIT between agents. Requires an EIP-191 signature "
                "over the message format: 'AgentPay Transfer: {sender}->{recipient} "
                "{amount} nonce:{nonce}'. The signing key must match sender address."
)
def pay(sender: str, recipient: str, amount: float,
        nonce: int, signature: str) -> str:
    """Transfer CREDIT with EIP-191 signature."""
    try:
        result = api.pay(sender, recipient, amount, nonce, signature)
        return (
            f"✅ Transfer complete\n"
            f"**From:** `{sender[:15]}...`\n"
            f"**To:** `{recipient[:15]}...`\n"
            f"**Amount:** {amount} CREDIT\n"
            f"**Fee:** {result.get('fee', 0)} CREDIT\n"
            f"**Status:** {result.get('status', 'completed')}"
        )
    except AgentPayError as e:
        return f"❌ Error: {e}"


@mcp.tool(
    name="audit",
    description="Get system-wide audit: USDC balance, total CREDIT in circulation, "
                "number of registered agents, and recent transactions."
)
def audit() -> str:
    """Get AgentPay system audit."""
    try:
        result = api.audit()
        return (
            f"**📊 AgentPay Audit**\n"
            f"**Wallet:** `{result.get('wallet', 'unknown')[:15]}...`\n"
            f"**USDC Balance:** {result.get('usdc_balance', 0)} USDC\n"
            f"**Total CREDIT:** {result.get('total_credit', 0)}\n"
            f"**Agents:** {result.get('agent_count', 0)}\n"
            f"**Network:** {result.get('network', 'Base')}\n"
            f"**Version:** {result.get('version', '0.2.0')}"
        )
    except AgentPayError as e:
        return f"❌ Error: {e}"


# ─── Main ──────────────────────────────────────

if __name__ == "__main__":
    mcp.run(transport="sse")
