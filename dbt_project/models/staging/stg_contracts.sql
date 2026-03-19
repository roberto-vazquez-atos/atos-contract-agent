with source as (
    select * from {{ source('contract_db', 'raw_contracts') }}
),

renamed as (
    select
        id                                      as contract_id,
        filename,
        contract_type,
        file_size_bytes,
        analyzed_at,
        length(raw_text)                        as text_length_chars,
        date_trunc('day', analyzed_at)          as analyzed_date
    from source
)

select * from renamed
