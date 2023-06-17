-- Top 10 products Model
SELECT 
    id,
    title as product_name,
    rating_rate as product_rating
FROM {{ source('fakestoreapi','products')}}
ORDER BY 3 DESC
LIMIT 10