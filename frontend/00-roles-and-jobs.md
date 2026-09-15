# Roles and jobs

Four kinds of people and one machine. The application knows who is signed in, and every
change set carries that name.

| Role | Who they are | What they come to do | Screens they live on |
|---|---|---|---|
| **Analyst** | The person who writes and reviews scenario records | Write a scenario end to end; review someone else's; bring in a new scenario from research; keep the framework mapping honest | Scenario (edit), Bring in a scenario, Frameworks |
| **Facilitator and system owners** | The person who runs a scoring meeting, and the people who own the systems being scored | Score every evidence row of a scenario on the two questions, name the exact source, the owner, the evidence, the ticket; read it back; leave with owned gaps | Session, Scenario |
| **Detection engineer** | The person who turns evidence into something the organization acts on, and who tests the claims | Write and maintain use cases; check readiness; design tests; read scorecards; accept or reject proposed rescores; review agent proposals | Use cases, Scenario management, Scenario |
| **Reader** | Leadership, risk, compliance, anyone asking "would we see this" | Read one scenario in plain language; read the coverage, exposure and maturity figures with their caveats; find which scenarios a framework identifier touches | Scenario (read), Coverage, Reports, Frameworks, Documentation |
| **Administrator** | Whoever owns the framework baseline, the environments and the shapes | Cut a baseline, define an environment, maintain an infrastructure shape, manage organizations | Administration |
| **The agentic platform** | Not a person. An orchestrator dispatching one sub agent per scenario | Hands over one run document per scenario per run through the import endpoint. Has no screen | none |

## Two rules about people that the interface enforces

1. **The reviewer is never the author.** A record cannot be published by the person who wrote it. The Publish action refuses, with the validator's message, and the screen says why.
2. **Every change has a name and a reason.** A change set without both is refused by the server. The Save dialog asks for the reason every time; the name is the signed in person.
