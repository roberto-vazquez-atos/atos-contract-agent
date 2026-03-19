{{
    config(materialized='table')
}}

-- For each contract, join its detected clauses against Atos approved standards.
-- This tells us which required clauses are missing and computes a compliance score.

with contracts as (
    select * from {{ ref('stg_contracts') }}
),

clauses as (
    select * from {{ ref('stg_clauses') }}
),

standards as (
    select * from {{ ref('approved_clauses') }}
),

-- Cross-join each contract with the required standards for its type
required_clauses as (
    select
        c.contract_id,
        c.filename,
        c.contract_type,
        s.clause_type         as required_clause,
        s.required,
        s.risk_level          as standard_risk_level,
        s.description         as standard_description
    from contracts c
    inner join standards s
        on c.contract_type = s.contract_type
       and s.required = true
),

-- Check which required clauses are actually present
compliance as (
    select
        r.contract_id,
        r.filename,
        r.contract_type,
        r.required_clause,
        r.standard_risk_level,
        r.standard_description,
        case when cl.clause_type is not null and cl.present = true
            then true
            else false
        end                   as clause_present
    from required_clauses r
    left join clauses cl
        on r.contract_id = cl.contract_id
       and lower(r.required_clause) = lower(cl.clause_type)
),

-- Aggregate to contract-level compliance score
scored as (
    select
        contract_id,
        filename,
        contract_type,
        count(*)                                                    as total_required_clauses,
        sum(case when clause_present then 1 else 0 end)            as clauses_present,
        sum(case when not clause_present then 1 else 0 end)        as clauses_missing,
        round(
            100.0 * sum(case when clause_present then 1 else 0 end) / count(*),
            1
        )                                                           as compliance_pct,
        -- Count missing by risk level
        sum(case when not clause_present and standard_risk_level = 'high'   then 1 else 0 end) as missing_high_risk,
        sum(case when not clause_present and standard_risk_level = 'medium' then 1 else 0 end) as missing_medium_risk,
        sum(case when not clause_present and standard_risk_level = 'low'    then 1 else 0 end) as missing_low_risk
    from compliance
    group by contract_id, filename, contract_type
)

select
    *,
    case
        when compliance_pct >= 90 then 'COMPLIANT'
        when compliance_pct >= 70 then 'NEEDS REVIEW'
        else 'NON-COMPLIANT'
    end as compliance_status
from scored
order by compliance_pct asc
