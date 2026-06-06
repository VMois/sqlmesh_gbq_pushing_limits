MODEL (
  name sqlmesh-495521.MyData_@{location}.product_usage_tvf,
  kind CUSTOM (
    materialization 'bigquery_tvf',
    materialization_properties (
      'tvf_params' = 'start_date DATE, end_date DATE'
    )
  )
);

SELECT
  product_id,
  customer_id,
  usage_count
FROM sqlmesh-495521.MyData_@{location}.product_usage
WHERE DATE(last_usage_date) BETWEEN @start_date AND @end_date
