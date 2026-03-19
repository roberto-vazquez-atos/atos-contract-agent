with source as (
    select * from {{ source('contract_db', 'raw_clauses') }}
),

renamed as (
    select
        id              as clause_id,
        contract_id,
        clause_type,
        clause_text,
        present,
        risk_level,
        case risk_level
            when 'high'   then 3
            when 'medium' then 2
            when 'low'    then 1
            else 0
        end             as risk_weight
    from source
)

select * from renamed
