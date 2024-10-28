# Week 2, Day 8-9: SQL Fundamentals

## Learning Goals

By the end of Day 9, I aim to:
1. Write basic SQL queries confidently
2. Understand database relationships and joins
3. Use SQL with Python through SQLite
4. Create and manage simple databases
5. Perform data analysis using SQL

## My Progress

1. [`sql_basics.py`](./sql_basics.py): My first steps with SQLite and Python
2. [`queries.sql`](./queries.sql): Collection of SQL queries I'm practicing
3. [`database_ops.py`](./database_ops.py): My experiments with database operations
4. [`analysis_queries.py`](./analysis_queries.py): Combining SQL and Python for analysis

## Small Project: Clinical Trials Database

To apply my SQL skills in a practical context, I'm building a small database to track clinical trials data. This project will help me learn:

1. Database design
2. Data insertion and updates
3. Complex queries
4. Data analysis with SQL

## Key Concepts:

### Basic SQL Operations
```sql
-- My first SELECT query
SELECT patient_id, treatment_group, response_rate 
FROM trials 
WHERE completion_status = 'Completed';
```

### Table Relationships
```sql
-- Joining patient data with trial results
SELECT p.patient_id, p.age_group, t.treatment_response
FROM patients p
JOIN trial_results t ON p.patient_id = t.patient_id;
```

### Aggregation Functions
```sql
-- Analyzing treatment effectiveness
SELECT treatment_group, 
       AVG(response_rate) as avg_response,
       COUNT(*) as patient_count
FROM trial_results
GROUP BY treatment_group;
```

## Resources I'm Using

- [SQLite Tutorial](https://www.sqlitetutorial.net/)
- [Python SQLite3 Documentation](https://docs.python.org/3/library/sqlite3.html)
- [SQL Practice Exercises](https://www.w3schools.com/sql/sql_exercises.asp)
