"""HTTP client for AgentPay REST API."""

import httpx
from typing import Optional

from config import AGENTPAY_URL


class AgentPayError(Exception):
    """AgentPay API error."""


class AgentPayClient:
    """Proxies requests to AgentPay REST API."""

    def __init__(self, base_url: str = AGENTPAY_URL):
        self.base_url = base_url.rstrip("/")

    def _get(self, path: str, params: Optional[dict] = None) -> dict:
        url = f"{self.base_url}{path}"
        resp = httpx.get(url, params=params, timeout=10)
        if resp.status_code != 200:
            raise AgentPayError(f"GET {path}: {resp.status_code} {resp.text}")
        return resp.json()

    def _post(self, path: str, body: dict) -> dict:
        url = f"{self.base_url}{path}"
        resp = httpx.post(url, json=body, timeout=10)
        if resp.status_code != 200:
            raise AgentPayError(f"POST {path}: {resp.status_code} {resp.text}")
        return resp.json()

    def get_balance(self, agent_address: str) -> dict:
        """Get agent's credit balance."""
        return self._get("/balance", {"agent_address": agent_address})

    def register(self, agent_address: str) -> dict:
        """Register a new agent."""
        return self._post("/register", {"agent_address": agent_address})

    def pay(self, from_address: str, to_address: str, amount: float,
            signature: str, nonce: int) -> dict:
        """Transfer CREDIT between agents with EIP-191 signature."""
        return self._post("/pay", {
            "from": from_address,
            "to": to_address,
            "amount": amount,
            "signature": signature,
            "nonce": nonce,
        })

    def audit(self) -> dict:
        """Get system audit (wallet balance, total CREDIT, agent count)."""
        return self._get("/audit")
