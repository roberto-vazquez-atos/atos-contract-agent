with analyses as (
    select * from {{ ref('stg_analyses') }}
),

contracts as (
    select * from {{ ref('stg_contracts') }}
),

joined as (
    select
        c.contract_type,
        a.party_b       as counterparty,
        a.governing_law
    from contracts c
    left join analyses a on c.contract_id = a.contract_id
    where a.party_b is not null and a.party_b != ''
),

aggregated as (
    select
        counterparty,
        count(*)                                    as total_contracts,
        count(case when contract_type = 'NDA'     then 1 end) as nda_count,
        count(case when contract_type = 'SOW'     then 1 end) as sow_count,
        count(case when contract_type = 'HIRING'  then 1 end) as hiring_count,
        listagg(distinct governing_law, ', ')       as governing_laws
    from joined
    group by counterparty
)

select * from aggregated
order by total_contracts desc
