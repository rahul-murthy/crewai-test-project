```sql
-- This query finds the top 5 move types by total number of moves
SELECT 
  movetypename, 
  no_of_moves,
  ROUND(no_of_moves * 100.0 / (SELECT SUM(no_of_moves) FROM move_type), 2) AS pct_of_total
FROM move_type
ORDER BY no_of_moves DESC
LIMIT 5;
```

This query first selects the `movetypename`, `no_of_moves`, and calculates the percentage of total moves for each move type. It orders the results by the `no_of_moves` column in descending order and limits the output to the top 5 rows.

The key steps are:

1. Select the relevant columns from the `move_type` table: `movetypename`, `no_of_moves`
2. Calculate the percentage of total moves for each move type by:
   - Getting the total number of moves by summing `no_of_moves` across all rows
   - Dividing each move type's `no_of_moves` by the total and rounding the percentage to 2 decimal places
3. Order the results by `no_of_moves` in descending order to put the top move types first
4. Limit the output to the top 5 rows

This gives us the top 5 move types by total volume (number of moves) and their percentage of the overall moves.