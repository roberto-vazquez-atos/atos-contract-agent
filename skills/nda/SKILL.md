---
name: nda
description: Use when analyzing Non-Disclosure Agreements (NDAs) for completeness, risk, and compliance with Atos standards.
allowed-tools: Read, Write
---

# NDA Analysis Skill

You are analyzing a **Non-Disclosure Agreement (NDA)**. Apply the following Atos legal baseline standards.

## Required Clauses Checklist
Verify that ALL of the following clauses are present and adequately defined:
1. **Definition of Confidential Information** — Must clearly scope what is and is not confidential
2. **Obligations of Receiving Party** — Must specify duties to protect confidential information
3. **Exclusions from Confidentiality** — Must list standard exclusions (public domain, prior knowledge, independently developed, required by law)
4. **Term and Duration** — Must specify agreement duration and survival period post-termination (standard: 2–5 years)
5. **Return or Destruction of Information** — Must require return or certified destruction upon termination
6. **No License Granted** — Must state that disclosure does not grant IP rights
7. **Governing Law and Jurisdiction** — Must specify applicable law and courts
8. **Mutual vs. Unilateral** — Must clearly identify directionality
9. **Permitted Disclosures** — Must specify authorized recipients (employees, advisors, need-to-know basis)
10. **Remedies / Injunctive Relief** — Should acknowledge that breach may cause irreparable harm

## Key Fields to Extract
- Party A (Disclosing Party)
- Party B (Receiving Party)
- Effective Date
- Expiration / Termination Date
- Survival Period
- Governing Law
- Mutual or Unilateral

## Risk Flags
Raise as HIGH risk:
- No duration or survival clause
- Overly broad definition of confidential information with no exclusions
- No governing law
- Missing return/destruction clause

Raise as MEDIUM risk:
- Survival period under 2 years
- No injunctive relief clause
- Vague permitted disclosures
- Missing "no license granted" clause

Raise as LOW risk:
- Minor formatting or labeling issues
- Non-standard but acceptable clause ordering

## Atos Standards
- Atos preferred governing law: French law or English law (depending on counterparty jurisdiction)
- Minimum confidentiality survival: 3 years post-termination
- Mutual NDAs are preferred for partnerships; unilateral is acceptable for vendor relationships
- All NDAs must include a data protection addendum reference if personal data may be shared
