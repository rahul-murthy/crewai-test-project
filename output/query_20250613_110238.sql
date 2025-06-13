-- Question: What are the top 5 move types by volume?
-- Generated on: 2025-06-13 11:02:38.753087

```sql
-- Query to get the top 5 move types by volume
SELECT
  movetypename,
  no_of_moves
FROM move_type
ORDER BY no_of_moves DESC
LIMIT 5;
```

This SQL query will return the top 5 move types by volume (number of moves). It selects the `movetypename` and `no_of_moves` columns from the `move_type` table, orders the results by the `no_of_moves` column in descending order, and limits the output to the top 5 rows.

The key steps are:

1. `SELECT movetypename, no_of_moves`: This specifies the columns we want to retrieve - the move type name and the number of moves.
2. `FROM move_type`: This indicates the table we are querying, which is `move_type` based on the schema information provided.
3. `ORDER BY no_of_moves DESC`: This sorts the results by the `no_of_moves` column in descending order, so the move types with the highest number of moves are listed first.
4. `LIMIT 5`: This limits the output to the top 5 rows, providing the top 5 move types by volume as required by the business rules.

The comments explain the purpose and logic of the query, making it easy to understand and maintain.