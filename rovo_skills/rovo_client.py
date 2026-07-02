"""
Client for invoking a Rovo agent, which internally talks to Jira/Confluence
via the remote Atlassian MCP server.

TODO: AGENT_INVOKE_PATH and the request/response shape below are placeholders —
confirm the real Rovo agent invocation contract and update this once known.
"""
import requests

from .config import Config


class RovoAgentClient:
    AGENT_INVOKE_PATH = "/gateway/api/rovo/agents/{agent_id}/invoke"

    def __init__(self, config: Config):
        self.config = config
        self.session = requests.Session()
        self.session.auth = (config.atlassian_email, config.atlassian_api_token)

    def _url(self) -> str:
        path = self.AGENT_INVOKE_PATH.format(agent_id=self.config.rovo_agent_id)
        return f"{self.config.atlassian_site_url.rstrip('/')}{path}"

    def invoke(self, prompt: str) -> dict:
        response = self.session.post(self._url(), json={"prompt": prompt})
        response.raise_for_status()
        return response.json()
