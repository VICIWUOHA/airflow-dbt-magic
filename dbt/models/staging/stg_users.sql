-- Staging Model for Users with only appropiate data

SELECT
    id,
    INITCAP(firstname) ||' '|| INITCAP(lastname) as full_name,
    email,
    phone,
    address_zipcode
FROM {{ source('fakestoreapi','users')}}