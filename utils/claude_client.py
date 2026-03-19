"""Claude API client with skill-aware contract analysis."""
import anthropic
import json
import os
from pathlib import Path


def load_skill(contract_type: str) -> str:
    """Load the skill prompt for a given contract type."""
    skill_map = {
        "NDA": "nda",
        "SOW": "sow",
        "HIRING": "hiring",
    }
    skill_dir = skill_map.get(contract_type, "nda")
    skill_path = Path(__file__).parent.parent / "skills" / skill_dir / "SKILL.md"
    if skill_path.exists():
        return skill_path.read_text()
    return ""


def analyze_contract(text: str, contract_type: str) -> dict:
    """Send contract text to Claude for structured analysis."""
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    skill_prompt = load_skill(contract_type)

    system_prompt = f"""You are an expert legal contract analyst at Atos.
Your task is to analyze contracts and return structured JSON.

{skill_prompt}

Always respond with valid JSON only — no markdown, no explanation outside the JSON.
Use this exact structure:
{{
  "party_a": "string",
  "party_b": "string",
  "effective_date": "string",
  "expiration_date": "string",
  "governing_law": "string",
  "contract_value": "string or N/A",
  "risk_score": 0-100,
  "summary": "2-3 sentence summary for Legal review",
  "risk_flags": ["list of identified risks"],
  "missing_clauses": ["list of standard clauses that are absent"],
  "key_obligations": ["list of key obligations per party"],
  "suggested_additions": ["list of recommended additions or corrections"],
  "clauses": [
    {{
      "type": "clause name",
      "text": "relevant excerpt or empty string",
      "present": true/false,
      "risk_level": "low/medium/high"
    }}
  ]
}}"""

    user_message = f"""Please analyze the following {contract_type} contract:

---
{text}
---"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )

    raw = message.content[0].text.strip()
    # Strip markdown code block if Claude wraps it
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw)


def compare_contracts(text_a: str, text_b: str, contract_type: str) -> dict:
    """Compare two contracts and return differences."""
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    system_prompt = """You are a legal contract comparison specialist at Atos.
Compare two contracts and return structured JSON only.
Use this structure:
{
  "key_differences": ["list of important differences"],
  "missing_in_a": ["clauses in B but not A"],
  "missing_in_b": ["clauses in A but not B"],
  "recommendation": "brief recommendation on which is more favorable"
}"""

    user_message = f"""Compare these two {contract_type} contracts:

CONTRACT A:
---
{text_a[:6000]}
---

CONTRACT B:
---
{text_b[:6000]}
---"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )

    raw = message.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw)
