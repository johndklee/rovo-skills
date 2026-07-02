"""
Smoke test for the Jira -> Rovo agent -> Atlassian MCP wiring.

Usage:
    cp .env.example .env   # fill in your values
    python test_connection.py
"""
import sys

from rovo_skills.config import Config
from rovo_skills.rovo_client import RovoAgentClient


def main() -> int:
    config = Config.from_env()
    missing = config.missing_fields()
    if missing:
        print("Missing config values in .env:")
        for field in missing:
            print(f"  - {field}")
        print("\nCopy .env.example to .env and fill these in, then rerun.")
        return 1

    print(f"Invoking Rovo agent '{config.rovo_agent_id}' on {config.atlassian_site_url} ...")
    client = RovoAgentClient(config)
    try:
        result = client.invoke("List the open issues in the current sprint.")
    except Exception as exc:
        print(f"Connection test failed: {exc}")
        print(
            "\nIf this is a 404/auth error, the invocation endpoint in "
            "rovo_skills/rovo_client.py (AGENT_INVOKE_PATH) likely needs "
            "updating once the real Rovo agent API contract is confirmed."
        )
        return 1

    print("Success! Response from Rovo agent:")
    print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
