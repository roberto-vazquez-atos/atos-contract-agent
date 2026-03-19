with contracts as (
    select * from {{ ref('stg_contracts') }}
),

analyses as (
    select * from {{ ref('stg_analyses') }}
),

joined as (
    select
        c.contract_id,
        c.filename,
        c.contract_type,
        c.analyzed_date,
        a.party_a,
        a.party_b,
        a.effective_date,
        a.expiration_date,
        a.governing_law,
        a.contract_value,
        a.risk_score,
        a.risk_tier,
        a.risk_flag_count,
        a.missing_clause_count,
        a.summary,
        a.risk_flags,
        a.missing_clauses
    from contracts c
    left join analyses a on c.contract_id = a.contract_id
)

select * from joined
order by risk_score desc
