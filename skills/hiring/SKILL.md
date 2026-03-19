---
name: hiring
description: Use when analyzing employment agreements and hiring contracts for completeness and compliance with Atos HR and legal standards.
allowed-tools: Read, Write
---

# Hiring / Employment Contract Analysis Skill

You are analyzing an **Employment Agreement**. Apply the following Atos HR and legal baseline standards.

## Required Clauses Checklist
Verify that ALL of the following are present and clearly defined:
1. **Job Title and Role Description** — Must specify position and reporting line
2. **Start Date** — Must include a specific or conditional start date
3. **Compensation** — Must specify base salary, currency, and pay frequency
4. **Benefits** — Must reference applicable benefit programs
5. **Working Hours** — Must specify expected hours and location (remote/office/hybrid)
6. **Probation Period** — Should include duration and conditions for probation
7. **Confidentiality Obligations** — Must bind employee to confidentiality during and after employment
8. **Intellectual Property Assignment** — Must assign IP created during employment to Atos
9. **Non-Compete / Non-Solicitation** — Should include reasonable post-employment restrictions
10. **Termination Conditions** — Must specify notice period, grounds for termination, and severance
11. **Governing Law** — Must specify applicable employment law jurisdiction
12. **Data Protection** — Must reference GDPR or applicable data protection obligations

## Key Fields to Extract
- Employee Name
- Employer Entity
- Job Title
- Start Date
- Base Salary
- Probation Period
- Notice Period
- Governing Law / Jurisdiction

## Risk Flags
Raise as HIGH risk:
- No IP assignment clause
- No confidentiality obligations
- Missing governing law
- Termination clause is missing or one-sided
- Non-compete clause is overly broad (may be unenforceable)

Raise as MEDIUM risk:
- No probation period defined
- Benefits not referenced
- Working location not specified
- Non-solicitation clause is absent

Raise as LOW risk:
- Minor formatting issues
- Non-standard but acceptable benefit descriptions

## Atos Standards
- Governing law: Must match the jurisdiction of the employing Atos entity
- IP assignment: All work product, code, and inventions created during employment belong to Atos
- Confidentiality survival: Minimum 2 years post-employment
- Non-compete duration: Maximum 12 months (longer may be unenforceable in EU jurisdictions)
- Data protection clause must explicitly reference GDPR for EU employees
