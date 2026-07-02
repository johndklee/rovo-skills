# rovo-skills

A test repo for building an [Atlassian Rovo](https://www.atlassian.com/software/rovo) Agent that:

1. **Generates Jira sprint reports** — pulls issues from the active sprint of a Jira project and summarizes progress/status.
2. **Publishes to Confluence** — creates a Confluence page with the current view of the sprint.

This is an evaluation project, not a production tool. It's also intended as a reference for any engineer trying to learn how to build an app using **Forge**, **Rovo**, and **Jira/Confluence** — the setup steps below walk through the whole path from a blank Atlassian account to a working, testable app.

## Architecture

This is a [Forge](https://developer.atlassian.com/platform/forge/) app (TypeScript/Node.js) that defines a custom **Rovo Agent** (`rovo:agent` module in [manifest.yml](manifest.yml)). The agent has two actions, implemented as Forge functions in [src/index.ts](src/index.ts):

- `get-sprint-issues` — queries Jira for issues in the project's active sprint.
- `publish-sprint-report` — creates a Confluence page with report content.

```
Rovo Agent (chat) -> Forge action functions -> Jira / Confluence REST APIs
```

Forge apps run on Atlassian's hosted infrastructure — you develop and test locally with `forge tunnel`, then `forge deploy`/`forge install` to run it against a real Jira/Confluence site. There's no local Python process or direct MCP client in this design; Forge is the only supported way to build custom Rovo Agent actions today (Python is not a supported Forge runtime).

## Setup

### Prerequisites

- **Node.js 22.x or 24.x.** Forge CLI 13.x warns/may misbehave on other versions (23.x, 25.x, 26.x included). Check with `node --version`; on macOS with Homebrew: `brew install node@24 && brew link --overwrite node@24`.
- **A Jira/Confluence Cloud site.** If you don't already have one, sign up at [atlassian.com/try/cloud/signup](https://www.atlassian.com/try/cloud/signup). The **Free** plan (up to 10 users, no credit card, permanent) is enough to `forge deploy`/`forge install` this app, but **not enough to actually chat with the Rovo Agent** — see the Rovo access note below. See [atlassian.com/software/free](https://www.atlassian.com/software/free) for plan comparisons.
- **Rovo access, to actually invoke the agent.** Rovo requires a **Standard, Premium, or Enterprise** plan — it is not available on Free, and there is no free/developer-only bypass ([confirmed via Atlassian's own activation docs](https://support.atlassian.com/organization-administration/docs/activate-or-deactivate-rovo-on-your-site/)). Separately, Atlassian also gates Rovo activation behind a **verified business domain** for the org admin account — generic domains (gmail.com, outlook.com, etc.) are excluded. Practical path: start a **Premium trial** (30 days, free) on your site, using an org admin email on a real custom domain you control, then check admin console → Apps → AI settings → AI-enabled apps to activate Rovo.
- **An Atlassian account** with access to create a Forge app.
- **An Atlassian API token**, used to log in the Forge CLI: create one at [id.atlassian.com/manage-profile/security/api-tokens](https://id.atlassian.com/manage-profile/security/api-tokens). Never commit this token — `forge login` stores it in your local Forge CLI config, not in this repo.

### Steps

```bash
npm install
npx forge login
```

`forge login` prompts interactively for your Atlassian email and the API token above.

```bash
npx forge register "your-app-name"
```

First time only. If your account isn't in a Developer Space yet, this also prompts you to create one (just a container for your Forge apps) — pick any name. `forge register` then writes a real `app.id` into `manifest.yml` for you.

```bash
npx forge lint      # validates manifest.yml
npx forge tunnel     # run/test locally against a real dev site
npx forge deploy     # deploy to Atlassian
npx forge install    # install the app on your Jira/Confluence site
```

`forge tunnel` and `forge install` need a real Jira/Confluence site (a free [developer sandbox site](https://developer.atlassian.com/platform/forge/set-up-instance/) works) to target.

## Status

- App registered, `forge lint` passes clean, deployed and installed on both Jira and Confluence for a test site.
- Rovo chat isn't reachable on that site yet — it's on the Free plan, which doesn't include Rovo (see the Rovo access note above). Still need a Premium/Standard trial + business-domain admin email to actually invoke the agent end-to-end.
- The Jira JQL query (`sprint in openSprints()`) and Confluence v2 page-creation call are based on documented, stable REST API endpoints but still untested end-to-end since the agent itself can't be invoked yet.

## Note

This repo is public. Do not commit API keys, tokens, credentials, or other sensitive/personal data. Forge auth (via `forge login`) is stored in your local Forge CLI config, not in this repo.
