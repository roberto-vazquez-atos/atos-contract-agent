---
name: sow
description: Use when analyzing Statements of Work (SOWs) for completeness, deliverable clarity, and risk against Atos project standards.
allowed-tools: Read, Write
---

# Statement of Work (SOW) Analysis Skill

You are analyzing a **Statement of Work (SOW)**. Apply the following Atos project delivery baseline standards.

## Required Clauses Checklist
Verify that ALL of the following are present and clearly defined:
1. **Project Scope** — Must clearly define what is in and out of scope
2. **Deliverables** — Must list all deliverables with descriptions
3. **Milestones and Timeline** — Must include dates or a delivery schedule
4. **Acceptance Criteria** — Must define what constitutes successful delivery per deliverable
5. **Payment Terms** — Must specify amount, schedule, and payment method
6. **Change Management Process** — Must define how scope changes are handled
7. **Roles and Responsibilities** — Must identify key personnel and their responsibilities on both sides
8. **Intellectual Property Ownership** — Must specify who owns work product upon completion
9. **Confidentiality Reference** — Should reference an NDA or include confidentiality terms
10. **Governing Law and Dispute Resolution** — Must specify jurisdiction and resolution mechanism
11. **Termination Clause** — Must specify conditions and notice period for termination
12. **Warranty and Liability** — Should cap liability and specify warranty period

## Key Fields to Extract
- Client (Party A)
- Service Provider (Party B)
- Project Name / Reference
- Effective Date
- Project End Date
- Total Contract Value
- Payment Schedule
- Governing Law

## Risk Flags
Raise as HIGH risk:
- No acceptance criteria for deliverables
- No change management process
- Uncapped liability
- IP ownership is ambiguous or assigned entirely to the client without conditions
- No termination for convenience clause

Raise as MEDIUM risk:
- Vague deliverable descriptions
- Missing roles and responsibilities
- No warranty clause
- Payment terms are undefined or too long (>60 days net)

Raise as LOW risk:
- Minor formatting issues
- Non-standard but acceptable clause ordering

## Atos Standards
- All SOWs must include a change order process referencing Atos's standard change management policy
- IP created during the project should default to Atos unless explicitly sold to the client
- Payment terms: Net 30 preferred, Net 60 maximum
- Liability cap: Typically capped at total contract value for direct damages
- Governing law: Atos entity jurisdiction (France for global engagements)
