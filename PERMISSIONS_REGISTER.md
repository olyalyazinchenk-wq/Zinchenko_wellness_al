# Permissions Register

Date: 2026-04-12
Purpose: define what access and approvals are needed to move this project from prototype to execution

## Already Available

- read and write access inside local workspace areas
- inspection of local project files
- creation of new local documentation and code

## Permissions We Will Need Next

### 1. Local Development Environment

Needed:

- permission to install or enable required tooling if missing
- Python runtime that works normally from terminal
- Git CLI
- optionally Node.js if frontend build tooling is introduced

Why:

- the current machine does not expose working `git`, `node`, or `npm` in this shell
- Python appears partially present but not usable in a normal way yet

Approval rule:

- request approval before any install or machine-level change

### 2. Telegram

Needed:

- Telegram bot token from BotFather
- confirmation of the bot username to be used
- test chat or test account for QA
- decision on delivery mode: polling first, webhook later

Why:

- current bot code uses a placeholder token only
- no live Telegram integration can be tested without explicit credentials

Approval rule:

- credentials should be injected via environment variables or secure secret storage, never hardcoded

### 3. AI Provider

Needed:

- OpenAI API key
- model policy for draft generation
- cost ceiling for testing

Why:

- the bot imports prompt templates but has no live LLM integration

Approval rule:

- secrets must be stored outside committed code

### 4. Sensitive Health Data Handling

Needed:

- explicit confirmation that client health data may be processed in this workflow
- approved consent text
- storage retention rule
- approved disclaimer language

Why:

- the product processes symptoms and lab data, which are sensitive

Approval rule:

- no production client data should be processed until consent and storage policy are defined

### 5. Payments and Monetization

Needed:

- selected payment provider
- operating country and currency assumptions
- refund and fulfillment policy

Why:

- monetization is a core goal, but there is no current payment flow

### 6. Hosting and Operations

Needed:

- target deployment environment
- domain or subdomain if web access is needed
- logging and monitoring choice

Why:

- current prototype is local only

## Recommended Approval Sequence

1. Approve product direction and first offer.
2. Approve Telegram bot creation and provide token.
3. Approve AI API usage and provide key.
4. Approve local tool installation if needed.
5. Approve hosting target after MVP logic works locally.

## What I Will Not Do Without Clear Approval

- install system software
- use external credentials
- connect to production Telegram assets
- process real client medical data
- publish misleading autonomous medical claims
