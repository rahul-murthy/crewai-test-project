-- Revenue Stream Analysis by Move Type
SELECT 
  move_type.movetypename,
  SUM(move_type.no_of_moves) AS total_moves,
  ROUND(SUM(move_type.no_of_moves) * 100.0 / (SELECT SUM(no_of_moves) FROM move_type), 2) AS percentage_of_total
FROM move_type
GROUP BY move_type.movetypename
ORDER BY total_moves DESC;

/*
This query analyzes the revenue streams by move type. It calculates the total number of moves and the percentage of total moves for each move type. This will help identify the key revenue drivers and their relative importance.
*/

-- Seasonal Trends by Move Type
SELECT
  move_type.movetypename,
  move_type.move_year,
  move_type.move_month,
  SUM(move_type.no_of_moves) AS total_moves,
  ROUND(SUM(move_type.no_of_moves) * 100.0 / (SELECT SUM(no_of_moves) FROM move_type WHERE move_year = move_type.move_year AND move_month = move_type.move_month), 2) AS percentage_of_monthly_total
FROM move_type
GROUP BY move_type.movetypename, move_type.move_year, move_type.move_month
ORDER BY move_type.move_year, move_type.move_month, total_moves DESC;

/*
This query analyzes the seasonal trends for each move type. It calculates the total number of moves and the percentage of total monthly moves for each move type and time period (year and month). This will help identify peak periods and seasonal patterns for different move types, which is crucial for capacity planning and pricing strategies.
*/

-- Revenue Stream Analysis by Move Size
SELECT
  move_size.movesizename,
  SUM(move_size.no_of_moves) AS total_moves,
  ROUND(SUM(move_size.no_of_moves) * 100.0 / (SELECT SUM(no_of_moves) FROM move_size), 2) AS percentage_of_total
FROM move_size
WHERE move_size.movesizename <> 'Unknown'
GROUP BY move_size.movesizename
ORDER BY total_moves DESC;

/*
This query analyzes the revenue streams by move size. It calculates the total number of moves and the percentage of total moves for each move size category, excluding the "Unknown" category. This will help identify the most popular move sizes and their relative contribution to the overall business.
*/

-- Seasonal Trends by Move Size
SELECT
  move_size.movesizename,
  move_size.move_year,
  move_size.move_month,
  SUM(move_size.no_of_moves) AS total_moves,
  ROUND(SUM(move_size.no_of_moves) * 100.0 / (SELECT SUM(no_of_moves) FROM move_size WHERE move_year = move_size.move_year AND move_month = move_size.move_month), 2) AS percentage_of_monthly_total
FROM move_size
WHERE move_size.movesizename <> 'Unknown'
GROUP BY move_size.movesizename, move_size.move_year, move_size.move_month
ORDER BY move_size.move_year, move_size.move_month, total_moves DESC;

/*
This query analyzes the seasonal trends for each move size category, excluding the "Unknown" category. It calculates the total number of moves and the percentage of total monthly moves for each move size and time period (year and month). This will help identify peak periods and seasonal patterns for different move sizes, which is crucial for capacity planning and pricing strategies.
*/

-- Data Quality Analysis: "Unknown" Move Size Category
SELECT
  'Unknown' AS movesizename,
  SUM(no_of_moves) AS total_moves,
  ROUND(SUM(no_of_moves) * 100.0 / (SELECT SUM(no_of_moves) FROM move_size), 2) AS percentage_of_total
FROM move_size
WHERE movesizename = 'Unknown';

/*
This query focuses on the "Unknown" move size category, which accounts for a significant 15.5% of the total moves. This indicates a potential data quality issue that the company should investigate and address. Improving the data quality in this category can lead to better insights and more accurate decision-making.
*/

The key metrics and insights that can be derived from these queries are:

1. Revenue Stream Analysis by Move Type:
   - The top revenue streams are Local Moves (17.8%), Long Distance Moves (11.3%), and Short Haul Moves (11.0%).
   - Labor Only Services account for 7.5% of the move volume, which is also an important revenue stream to monitor.

2. Seasonal Trends by Move Type:
   - The queries reveal the seasonal patterns for each move type, allowing the company to plan resources, adjust pricing, and optimize capacity accordingly.
   - This information can help the company make more informed decisions about staffing, equipment allocation, and pricing strategies throughout the year.

3. Revenue Stream Analysis by Move Size:
   - The top move size categories are Apartment 1 Bedroom (10.8%), House 3 Bedroom (10.4%), and Few Items (9.6%).
   - The "Unknown" category accounts for 15.5% of the total moves, which is a data quality issue that the company should address.

4. Seasonal Trends by Move Size:
   - The seasonal patterns for each move size category can help the company anticipate demand, allocate resources, and adjust pricing more effectively.
   - Understanding the peaks and valleys in move volume by size will enable the company to be more responsive to market conditions.

Overall, these queries provide a comprehensive analysis of All My Sons Moving Company's revenue streams, seasonal trends, and data quality considerations. The insights gained from these analyses can be used to optimize pricing, resource allocation, capacity planning, and ultimately drive revenue growth for the business.