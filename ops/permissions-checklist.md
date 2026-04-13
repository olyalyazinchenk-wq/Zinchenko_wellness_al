# Permission Checklist

Use this checklist before any privileged action.

## Always required explicit approval

- Create or modify cloud compute resources that can incur cost.
- Install software globally on the machine.
- Open external GUI apps on the user's desktop.
- Change network/proxy settings.
- Access external accounts or connectors not already configured.

## Safe by default (no escalation expected)

- Read and edit files inside project workspace.
- Run local Python and PowerShell commands inside workspace.
- Generate local reports and logs.

## Approval message format

When escalation is needed, ask in one sentence:

- What action will be performed.
- Why it is needed now.
- What outcome it unlocks.

Example:

"Allow creating one Yandex Cloud VM to host the private model endpoint for the bot so we can test production latency?"
