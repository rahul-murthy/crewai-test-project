```sql
-- This query finds the top 5 move types by total volume (number of moves)
-- It excludes the 'Unknown' move type category as per the business rules
-- and orders the results by the total number of moves in descending order

SELECT 
  movetypename,
  SUM(no_of_moves) AS total_moves
FROM move_type
WHERE movetypename <> 'Unknown'
GROUP BY movetypename
ORDER BY total_moves DESC
LIMIT 5;
```

This query accomplishes the following:

1. Selects the `movetypename` column and calculates the `total_moves` for each move type by summing the `no_of_moves` column.
2. Applies a `WHERE` clause to exclude the 'Unknown' move type category, as per the business rules.
3. Groups the results by `movetypename` to aggregate the move counts for each move type.
4. Orders the results by the `total_moves` column in descending order to get the top 5 move types.
5. Limits the output to the top 5 rows using the `LIMIT 5` clause.

This query provides the requested information about the top 5 move types by volume, while adhering to the provided business rules and schema constraints.