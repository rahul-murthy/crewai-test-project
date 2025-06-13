-- Question: What are the top 5 move types by volume?
-- Generated on: 2025-06-12 21:27:46.295228

```sql
-- Get the top 5 move types by total number of moves
WITH move_type_summary AS (
  SELECT 
    movetypename,
    SUM(no_of_moves) AS total_moves
  FROM move_type
  GROUP BY movetypename
  ORDER BY total_moves DESC
  LIMIT 5
)
SELECT 
  mt.movetypename,
  mts.total_moves,
  ROUND(mts.total_moves * 100.0 / (SELECT SUM(total_moves) FROM move_type_summary), 2) AS percentage_of_total
FROM move_type_summary mts
JOIN move_type mt ON mts.movetypename = mt.movetypename
ORDER BY mts.total_moves DESC;
```

Explanation:
1. The query starts with a CTE (Common Table Expression) called `move_type_summary` that calculates the total number of moves for each move type and orders the results by the total moves in descending order, limiting to the top 5 results.
2. The main query then joins the `move_type_summary` CTE with the `move_type` table to retrieve the actual move type names and calculates the percentage of total moves each of the top 5 move types represents.
3. The percentage is calculated by summing the total moves across all move types and dividing each move type's total by the overall total.
4. The results are ordered by the total moves in descending order to show the top 5 move types by volume.

This query is optimized for performance by:
- Using a CTE to perform the initial aggregation and sorting, reducing the amount of processing required in the main query
- Joining only the top 5 move types from the CTE to the main `move_type` table, reducing the number of rows that need to be processed
- Calculating the percentage of total moves in the main query rather than as a separate step, reducing the number of queries required
- Rounding the percentage values to 2 decimal places to improve readability

The query is also designed to be reusable and maintainable, with clear comments explaining the logic and calculations being performed.