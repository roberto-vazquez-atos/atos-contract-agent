# Atos Contract Helper Agent

AI-powered contract analysis tool for the Atos Legal team.

## Quick Start

```bash
# 1. Install & set up
python setup.py

# 2. Add your API key
#    Edit .env and set ANTHROPIC_API_KEY=sk-ant-...

# 3. Run the app
streamlit run app.py
```

## Features

- **Analyze** Word contracts (NDA, SOW, Hiring) with Claude AI
- **Extract** key fields: parties, dates, governing law, value
- **Flag** risks and missing standard clauses
- **Compare** two contracts side by side
- **Analytics dashboard** powered by dbt + DuckDB

## Project Structure

```
atos-contract-agent/
├── app.py                    # Streamlit application
├── skills/
│   ├── nda/SKILL.md         # NDA analysis rules
│   ├── sow/SKILL.md         # SOW analysis rules
│   └── hiring/SKILL.md      # Hiring contract rules
├── dbt_project/              # dbt transformation models
│   └── models/
│       ├── staging/          # Normalized source tables
│       └── marts/            # Analytics-ready tables
├── utils/
│   ├── document_parser.py   # Word → text
│   ├── claude_client.py     # Claude API calls
│   └── database.py          # DuckDB persistence
├── sample_contracts/         # Demo contracts
└── data/contracts.duckdb    # Local database (auto-created)
```

## API Key

You need an Anthropic API key. Get one at [console.anthropic.com](https://console.anthropic.com).
This is separate from a Claude Pro subscription.

## Customizing Skills

Edit the `SKILL.md` files in `skills/` to adjust:
- Required clauses checklist
- Risk flag criteria
- Atos-specific standards

Each skill file is plain Markdown — no code changes needed.
