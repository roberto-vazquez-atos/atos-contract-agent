with source as (
    select * from {{ source('contract_db', 'raw_analyses') }}
),

parsed as (
    select
        id                                          as analysis_id,
        contract_id,
        party_a,
        party_b,
        effective_date,
        expiration_date,
        governing_law,
        contract_value,
        risk_score,
        summary,
        analyzed_at,
        -- Parse JSON arrays into countable lengths
        json_array_length(risk_flags)               as risk_flag_count,
        json_array_length(missing_clauses)          as missing_clause_count,
        json_array_length(key_obligations)          as obligation_count,
        -- Risk tier
        case
            when risk_score >= 70 then 'HIGH'
            when risk_score >= 40 then 'MEDIUM'
            else 'LOW'
        end                                         as risk_tier,
        risk_flags,
        missing_clauses,
        key_obligations
    from source
)

select * from parsed
