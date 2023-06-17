{% docs abstract_cte %}

### abstract_cte

This macro abstracts the need to write all your **select * ctes** explicitly and saves lines of code to be generated at compile time.

- #### tuple_list: An array containing one or more tuples of two elements as follows;

  - 1. the name to give the cte
  - 2. the name of the model to be referenced.
  - #### Example:

    {% raw %}
    ```
    {{ abstract_cte([
            ('system_a','system_a_daily_sales'),
            ('system_b','system_b_daily_sales')
        ])
    }}
    would be compiled as ;

    WITH system_a AS (
    SELECT *
    FROM {{ref('system_a_daily_sales')}}
    ),
    system_b AS (
    SELECT *
    FROM {{ref('system_b_daily_sales')}}
    ),
    ```
    {% endraw %}

- The Rest of the logic can then be implemented downstream.

{% enddocs %}