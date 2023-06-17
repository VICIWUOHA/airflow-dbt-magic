{% snapshot fakestore_products_history%}

{{
    config(
        target_schema=env_var("DBT_LAGOS_MEETUP_SCHEMA"),
        unique_key='id',
        strategy='timestamp',
        updated_at='updated_at',
        invalidate_hard_deletes=True,
    )
}}

SELECT * FROM {{source('fakestoreapi','products')}}
--This would start tracking the changes on inventory items from the moment this model was created.
{% endsnapshot%}