CREATE TABLE applicants (
  applicant_id        INTEGER PRIMARY KEY,                                        -- Unique applicant id
  sex                 TEXT CHECK (sex IN ('F','M')),                              -- Applicant sex
  age                 INTEGER,                                                    -- Age in years
  marital_status      TEXT CHECK (marital_status IN
                        ('single','married','cohabiting','divorced','widowed')),  -- Marital status
  post_code           CHAR(5),                                                    -- Home postal code
  dependents          INTEGER,                                                    -- Number of dependents
  employment_type     TEXT CHECK (employment_type IN
                        ('permanent','temporary','self_employed','unemployed')),  -- Employment type
  salary_monthly_sek  INTEGER,                                                    -- Gross monthly salary, SEK
  existing_debt_sek   INTEGER,                                                    -- Total existing debt, SEK
  loan_amount_sek     INTEGER,                                                    -- Requested loan, SEK
  loan_term_months    INTEGER,                                                    -- Loan term in months
  missed_payments_12m INTEGER                                                     -- Missed payments, last 12 months
);