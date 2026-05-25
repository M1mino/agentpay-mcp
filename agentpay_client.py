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

    def _get(self, path: str) -> dict:
        url = f"{self.base_url}{path}"
        resp = httpx.get(url, timeout=10)
        if resp.status_code != 200:
            raise AgentPayError(f"GET {path}: {resp.status_code} {resp.text}")
        return resp.json()

    def _post(self, path: str, body: dict) -> dict:
        url = f"{self.base_url}{path}"
        resp = httpx.post(url, json=body, timeout=10)
        if resp.status_code != 200:
            raise AgentPayError(f"POST {path}: {resp.status_code} {resp.text}")
        return resp.json()

    def get_balance(self, address: str) -> dict:
        """Get agent's credit balance by on-chain address."""
        return self._get(f"/balance/{address}")

    def register(self, address: str) -> dict:
        """Register a new agent by its on-chain address."""
        return self._post("/register", {"address": address})

    def pay(self, sender: str, recipient: str, amount: float,
            nonce: int, signature: str) -> dict:
        """Transfer CREDIT between agents with EIP-191 signature."""
        return self._post("/pay", {
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
            "nonce": nonce,
            "signature": signature,
        })

    def audit(self) -> dict:
        """Get system audit (wallet balance, total CREDIT, agent count)."""
        return self._get("/audit")
