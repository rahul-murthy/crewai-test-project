Task Plan to Analyze Revenue Streams Over Time:

1. Metadata Agent: Retrieve the schema details for the `move_size` and `move_type` tables.
   - Deliverables: Table column names, data types, and descriptions.
   - Dependencies: None.

2. Knowledge Agent: Get the definitions and business context for the different move service types in the `move_type` table.
   - Deliverables: Explanations of each move service type, such as "Local" moves, "Long Distance" moves, "Labor Only" services, etc.
   - Dependencies: Task 1 (Metadata Agent).

3. Knowledge Agent: Understand how the company categorizes and reports on revenue streams.
   - Deliverables: Definitions of the primary revenue streams, how they are calculated, and any seasonality or trends in the data.
   - Dependencies: Task 2 (Knowledge Agent).

4. Query Builder Agent: Create SQL queries to analyze the revenue trends over time for the primary move service types.
   - Deliverables: SQL queries that aggregate revenue by move type and group by time period (e.g., month, quarter, year) to identify trends.
   - Dependencies: Tasks 1 (Metadata Agent) and 2 (Knowledge Agent).

5. Executor Agent: Run the SQL queries created in the previous step and provide the results.
   - Deliverables: Tabular or graphical results showing the revenue trends for the major move service types over time.
   - Dependencies: Task 4 (Query Builder Agent).

6. Synthesis: Summarize the key findings from the revenue trend analysis, including:
   - The primary revenue streams and their relative contributions
   - Significant trends or seasonality observed in the data
   - Any notable changes or shifts in the revenue mix over time
   - Recommendations for further analysis or potential business opportunities

The step-by-step plan ensures that the necessary context and data are gathered before performing the revenue analysis. By using the different agent roles, the tasks are executed in the most efficient and accurate manner, providing a comprehensive understanding of the company's revenue streams and their trends over time.