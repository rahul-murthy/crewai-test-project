The two key tables for analyzing All My Sons Moving Company's revenue streams are:

1. move_size:
   - Contains 14 move size categories like "Apt 1 Bedroom", "House 3 Bedroom", "Few Items", etc.
   - Includes monthly counts (no_of_moves) for each size category from 1900-2070.
   - Provides insight into the volume and composition of move sizes, which impacts crew allocation, pricing, and resource planning.
   - Key insight: The "Unknown" category accounts for 15.5% of moves, indicating a data quality opportunity.

2. move_type: 
   - Contains 24 move service types like "Local", "Long Distance", "Short Haul", "Labor Only", etc.
   - Includes monthly counts (no_of_moves) for each service type from 1900-2070.
   - Enables analysis of the primary revenue streams, such as Local moves (17.8% of volume) and Long Distance moves (11.3% of volume).
   - Long Distance moves typically have premium pricing, so this is a key revenue stream to monitor.
   - The data supports revenue optimization, pricing differentiation, and route planning.

Both tables have a consistent schema with columns for move_year, move_month, size/type codes, names, and volume counts. The data is stored in S3 at s3://ams-ai-dl-curated-dev-v2.

This comprehensive metadata provides the necessary foundation to perform detailed analyses of All My Sons Moving Company's revenue streams and their trends over time. With this information, downstream agents can build effective SQL queries, identify key insights, and make informed recommendations to the business.