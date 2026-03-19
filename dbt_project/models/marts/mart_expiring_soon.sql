with analyses as (
    select * from {{ ref('stg_analyses') }}
),

contracts as (
    select * from {{ ref('stg_contracts') }}
),

joined as (
    select
        c.contract_id,
        c.filename,
        c.contract_type,
        a.party_a,
        a.party_b,
        a.expiration_date,
        a.risk_score,
        a.risk_tier,
        -- Flag contracts expiring within 90 days (where date is parseable)
        try_cast(a.expiration_date as date)             as expiration_parsed,
        case
            when try_cast(a.expiration_date as date) is not null
             and try_cast(a.expiration_date as date) <= current_date + interval '90 days'
             and try_cast(a.expiration_date as date) >= current_date
            then true
            else false
        end                                             as expiring_within_90_days,
        case
            when try_cast(a.expiration_date as date) is not null
             and try_cast(a.expiration_date as date) < current_date
            then true
            else false
        end                                             as already_expired
    from contracts c
    left join analyses a on c.contract_id = a.contract_id
    where a.expiration_date is not null
      and a.expiration_date != ''
      and a.expiration_date != 'N/A'
)

select * from joined
order by expiration_parsed asc
