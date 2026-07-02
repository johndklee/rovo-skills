# rovo-skills

A test repo for building [Atlassian Rovo Skills](https://www.atlassian.com/software/rovo) that:

1. **Generate Jira sprint reports** — pull data from an active sprint and summarize progress/status.
2. **Publish to Confluence** — create or update a Confluence page with the current view of the sprint.

This is an evaluation project, not a production tool.

## Architecture

Local Python code invokes a **Rovo agent**, which talks to Jira/Confluence via the **remote Atlassian MCP server**. The Python code never calls Jira/Confluence or the MCP server directly.

```
Python (this repo) -> Rovo agent -> Atlassian MCP server (remote) -> Jira / Confluence
```

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # fill in your Atlassian site, project, agent ID, and credentials
python test_connection.py
```

`rovo_skills/rovo_client.py` invokes the configured Rovo agent over HTTP. The exact invocation endpoint/payload is currently a placeholder (marked `TODO`) pending confirmation of the real Rovo agent API contract.

## Note

This repo is public. Do not commit API keys, tokens, credentials, or other sensitive/personal data. Use environment variables or a local `.env` file (already git-ignored) for any secrets needed by the skills.
