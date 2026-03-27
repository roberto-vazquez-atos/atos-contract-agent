{{
    config(materialized='table')
}}

-- Portfolio-level clause gap analysis.
-- Starting point is the Atos REQUIRED clauses (approved_clauses seed), not
-- what Claude detected.  For every required clause we ask: across all contracts
-- of that type, how many are missing it?  This catches clauses that are so
-- consistently absent that they never even appear in raw_clauses at all.

with standards as (
    select * from {{ ref('approved_clauses') }}
    where required = true
),

contracts as (
    select * from {{ ref('stg_contracts') }}
),

clauses as (
    select * from {{ ref('stg_clauses') }}
),

-- Every (contract, required_clause) combination that should exist
required_pairs as (
    select
        c.contract_id,
        c.filename,
        c.contract_type,
        s.clause_type       as required_clause,
        s.risk_level,
        s.description
    from contracts c
    inner join standards s
        on c.contract_type = s.contract_type
),

-- Flag each pair as present or missing
presence as (
    select
        rp.contract_id,
        rp.contract_type,
        rp.required_clause,
        rp.risk_level,
        rp.description,
        case
            when cl.clause_type is not null and cl.present = true then true
            else false
        end as clause_present
    from required_pairs rp
    left join clauses cl
        on rp.contract_id = cl.contract_id
       and lower(rp.required_clause) = lower(cl.clause_type)
),

-- Aggregate across the entire portfolio per (contract_type, required_clause)
aggregated as (
    select
        contract_type,
        required_clause,
        risk_level,
        description,
        count(*)                                                    as contracts_total,
        sum(case when clause_present     then 1 else 0 end)        as contracts_with_clause,
        sum(case when not clause_present then 1 else 0 end)        as contracts_missing,
        round(
            100.0 * sum(case when not clause_present then 1 else 0 end) / count(*),
            1
        )                                                           as gap_pct
    from presence
    group by contract_type, required_clause, risk_level, description
)

select
    contract_type,
    required_clause,
    risk_level,
    description,
    contracts_total,
    contracts_with_clause,
    contracts_missing,
    gap_pct,
    -- Rank within each contract type: 1 = most commonly missing
    row_number() over (
        partition by contract_type
        order by gap_pct desc, risk_level desc
    ) as gap_rank
from aggregated
order by contract_type, gap_pct desc
