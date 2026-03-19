with clauses as (
    select * from {{ ref('stg_clauses') }}
),

contracts as (
    select * from {{ ref('stg_contracts') }}
),

joined as (
    select
        c.contract_type,
        cl.clause_type,
        count(*)                                    as total_occurrences,
        sum(case when cl.present then 1 else 0 end) as present_count,
        sum(case when not cl.present then 1 else 0 end) as missing_count,
        round(
            100.0 * sum(case when cl.present then 1 else 0 end) / count(*),
            1
        )                                           as coverage_pct,
        count(case when cl.risk_level = 'high'   then 1 end) as high_risk_count,
        count(case when cl.risk_level = 'medium' then 1 end) as medium_risk_count
    from clauses cl
    left join contracts c on cl.contract_id = c.contract_id
    group by c.contract_type, cl.clause_type
)

select * from joined
order by contract_type, coverage_pct asc
