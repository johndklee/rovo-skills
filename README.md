# rovo-skills

A test repo for building an [Atlassian Rovo](https://www.atlassian.com/software/rovo) Agent that:

1. **Generates Jira sprint reports** — pulls issues from the active sprint of a Jira project and summarizes progress/status.
2. **Publishes to Confluence** — creates a Confluence page with the current view of the sprint.

This is an evaluation project, not a production tool.

## Architecture

This is a [Forge](https://developer.atlassian.com/platform/forge/) app (TypeScript/Node.js) that defines a custom **Rovo Agent** (`rovo:agent` module in [manifest.yml](manifest.yml)). The agent has two actions, implemented as Forge functions in [src/index.ts](src/index.ts):

- `get-sprint-issues` — queries Jira for issues in the project's active sprint.
- `publish-sprint-report` — creates a Confluence page with report content.

```
Rovo Agent (chat) -> Forge action functions -> Jira / Confluence REST APIs
```

Forge apps run on Atlassian's hosted infrastructure — you develop and test locally with `forge tunnel`, then `forge deploy`/`forge install` to run it against a real Jira/Confluence site. There's no local Python process or direct MCP client in this design; Forge is the only supported way to build custom Rovo Agent actions today (Python is not a supported Forge runtime).

## Setup

Requires Node.js 22.x/24.x and the Forge CLI, plus an Atlassian account with Forge access.

```bash
npm install
npx forge login    # interactive — needs an Atlassian API token
npx forge register "your-app-name"   # first time only: creates a Developer Space + registers the app
```

`forge register` writes a real `app.id` into `manifest.yml` for you.

```bash
npx forge lint      # validates manifest.yml
npx forge tunnel     # run/test locally against a real dev site
npx forge deploy     # deploy to Atlassian
npx forge install    # install the app on your Jira/Confluence site
```

## Status

- App registered, `forge lint` passes clean.
- Not yet deployed/installed against a real Jira/Confluence site — the Jira JQL query (`sprint in openSprints()`) and Confluence v2 page-creation call are based on documented, stable REST API endpoints but untested end-to-end.
- Next step: `forge tunnel` or `forge deploy` + `forge install` against a real dev site to actually exercise the two actions.

## Note

This repo is public. Do not commit API keys, tokens, credentials, or other sensitive/personal data. Forge auth (via `forge login`) is stored in your local Forge CLI config, not in this repo.
