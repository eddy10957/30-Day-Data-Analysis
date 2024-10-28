-- queries.sql - My collection of SQL practice queries for the clinical trials database

-- 1. Basic SELECT queries
-- Finding all patients with Type 1 Diabetes
SELECT patient_id, age, sex, enrollment_date
FROM patients
WHERE condition = 'Type 1 Diabetes';

-- Get all trials in Phase 3
SELECT *
FROM trials
WHERE phase = 3;

-- 2. Aggregation functions
-- Calculate average age by condition
SELECT condition,
       COUNT(*) as patient_count,
       AVG(age) as avg_age,
       MIN(age) as min_age,
       MAX(age) as max_age
FROM patients
GROUP BY condition;

-- Treatment response statistics
SELECT trial_id,
       COUNT(*) as total_patients,
       AVG(treatment_response) as avg_response,
       MIN(treatment_response) as min_response,
       MAX(treatment_response) as max_response
FROM trial_results
GROUP BY trial_id;

-- 3. JOIN operations
-- Get patient details with their trial results
SELECT p.patient_id,
       p.age,
       p.condition,
       t.treatment_name,
       tr.treatment_response,
       tr.completion_status
FROM patients p
JOIN trial_results tr ON p.patient_id = tr.patient_id
JOIN trials t ON tr.trial_id = t.trial_id;

-- 4. More complex queries
-- Find treatments with above-average response rates
WITH avg_response AS (
    SELECT AVG(treatment_response) as overall_avg
    FROM trial_results
)
SELECT t.treatment_name,
       AVG(tr.treatment_response) as avg_response,
       COUNT(*) as patient_count
FROM trials t
JOIN trial_results tr ON t.trial_id = tr.trial_id
GROUP BY t.treatment_name
HAVING AVG(tr.treatment_response) > (SELECT overall_avg FROM avg_response);

-- 5. Analysis queries
-- Success rate by age group
SELECT 
    CASE 
        WHEN age < 30 THEN '18-29'
        WHEN age < 50 THEN '30-49'
        ELSE '50+'
    END as age_group,
    COUNT(*) as patient_count,
    AVG(CASE WHEN tr.treatment_response > 0.7 THEN 1.0 ELSE 0.0 END) as success_rate
FROM patients p
JOIN trial_results tr ON p.patient_id = tr.patient_id
GROUP BY 
    CASE 
        WHEN age < 30 THEN '18-29'
        WHEN age < 50 THEN '30-49'
        ELSE '50+'
    END;

-- 6. Time-based analysis
-- Monthly enrollment counts
SELECT 
    strftime('%Y-%m', enrollment_date) as month,
    COUNT(*) as enrollments
FROM patients
GROUP BY strftime('%Y-%m', enrollment_date)
ORDER BY month;

-- 7. Safety analysis
-- Adverse events by treatment
SELECT t.treatment_name,
       COUNT(*) as total_patients,
       AVG(tr.adverse_events) as avg_adverse_events,
       SUM(CASE WHEN tr.adverse_events > 0 THEN 1 ELSE 0 END) as patients_with_events
FROM trials t
JOIN trial_results tr ON t.trial_id = tr.trial_id
GROUP BY t.treatment_name;

-- 8. Completion analysis
-- Completion rates by condition
SELECT p.condition,
       COUNT(*) as total_patients,
       SUM(CASE WHEN tr.completion_status = 'Completed' THEN 1 ELSE 0 END) as completed,
       ROUND(AVG(CASE WHEN tr.completion_status = 'Completed' THEN 1.0 ELSE 0.0 END) * 100, 2) as completion_rate
FROM patients p
JOIN trial_results tr ON p.patient_id = tr.patient_id
GROUP BY p.condition;