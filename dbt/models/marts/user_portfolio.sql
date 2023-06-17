{{
    abstract_cte([
        ('users','stg_users')
    ])
}},


user_cart_summary AS (

    SELECT
        user_id,
        COUNT(DISTINCT product_id) AS unique_products_tried_out,
        SUM(quantity) AS lifetime_product_volume,
        COUNT(DISTINCT date) AS no_of_days_in_store

    FROM {{ source('fakestoreapi','carts')}}
    GROUP BY 1
    -- HAVING ((COUNT(DISTINCT date)) > 1 OR (COUNT(DISTINCT product_id))>1) -- have visisted the fakestore more than once
    
),


user_top_products AS (

    SELECT 
        a.user_id,
        c.full_name,
        c.email,
        b.title as top_product,
        a.quantity as top_product_quantity
    FROM(
            SELECT 
                user_id,
                product_id,
                quantity,
                ROW_NUMBER() OVER (PARTITION BY user_id ORDER by quantity DESC ) as rn
            FROM {{ source('fakestoreapi','carts')}}
    ) AS a
    LEFT JOIN {{ source('fakestoreapi','products')}} AS b
    ON a.product_id = b.id
    LEFT JOIN {{ ref('stg_users')}} c
    ON a.user_id = c.id
    WHERE a.rn = 1
)


SELECT
    a.user_id,
    a.full_name,
    a.email,
    b.lifetime_product_volume,
    b.unique_products_tried_out,
    b.no_of_days_in_store,
    a.top_product,
    a.top_product_quantity
FROM user_top_products a
LEFT JOIN user_cart_summary b
ON a.user_id = b.user_id