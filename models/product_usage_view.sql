MODEL (
  name sqlmesh-495521.MyData_@{location}.product_usage_view,
  kind VIEW,
  grain (product_id, customer_id, last_usage_date),
  audits (
    unique_combination_of_columns(columns := (product_id, customer_id, last_usage_date))
  )
);

SELECT
    product_id,
    customer_id,
    DATE(last_usage_date) AS last_usage_date,
    usage_count,
    feature_utilization_score,
    user_segment
FROM
  sqlmesh-495521.MyData_@{location}.product_usage
  
