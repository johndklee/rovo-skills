import os
from dataclasses import dataclass, fields

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    atlassian_site_url: str
    jira_project_key: str
    confluence_space_key: str
    rovo_agent_id: str
    atlassian_email: str
    atlassian_api_token: str
    confluence_parent_page_id: str = ""

    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            atlassian_site_url=os.environ.get("ATLASSIAN_SITE_URL", ""),
            jira_project_key=os.environ.get("JIRA_PROJECT_KEY", ""),
            confluence_space_key=os.environ.get("CONFLUENCE_SPACE_KEY", ""),
            confluence_parent_page_id=os.environ.get("CONFLUENCE_PARENT_PAGE_ID", ""),
            rovo_agent_id=os.environ.get("ROVO_AGENT_ID", ""),
            atlassian_email=os.environ.get("ATLASSIAN_EMAIL", ""),
            atlassian_api_token=os.environ.get("ATLASSIAN_API_TOKEN", ""),
        )

    def missing_fields(self) -> list[str]:
        # confluence_parent_page_id is optional, everything else is required
        required = {f.name for f in fields(self)} - {"confluence_parent_page_id"}
        return [name for name in required if not getattr(self, name)]
