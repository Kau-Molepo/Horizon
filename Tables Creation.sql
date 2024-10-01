-- Create Users Table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    hashed_firebase_uid CHAR(64) NOT NULL UNIQUE,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    role VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create Payroll Table with Generated Column for total_salary
CREATE TABLE payroll (
    payroll_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    base_salary DECIMAL(12, 2) NOT NULL,
    bonuses DECIMAL(12, 2) DEFAULT 0,
    deductions DECIMAL(12, 2) DEFAULT 0,
    total_salary DECIMAL(12, 2) GENERATED ALWAYS AS (base_salary + bonuses - deductions) STORED,
    pay_period DATE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);


-- Create Recruitment Table
CREATE TABLE recruitment (
    recruitment_id SERIAL PRIMARY KEY,
    job_title VARCHAR(100) NOT NULL,
    job_description TEXT,
    recruiter_id INT REFERENCES users(user_id) ON DELETE SET NULL,
    posting_date TIMESTAMP DEFAULT NOW(),
    closing_date TIMESTAMP,
    status VARCHAR(50) DEFAULT 'open', -- e.g., 'open', 'closed'
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create Applications Table
CREATE TABLE applications (
    application_id SERIAL PRIMARY KEY,
    recruitment_id INT REFERENCES recruitment(recruitment_id) ON DELETE CASCADE,
    applicant_name VARCHAR(100) NOT NULL,
    applicant_email VARCHAR(100) NOT NULL,
    resume TEXT, -- Link to resume file or base64 encoded
    status VARCHAR(50) DEFAULT 'applied', -- e.g., 'applied', 'interviewed', 'hired', 'rejected'
    applied_on TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create AI Analytics Table
CREATE TABLE ai_analytics (
    ai_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    model_type VARCHAR(50), -- e.g., 'chatbot', 'payroll_prediction'
    input_data TEXT,  -- Can be JSON or text logs of the interaction
    output_data TEXT, -- Result of the AI model, could also be JSON
    confidence_level DECIMAL(5, 4), -- Confidence of the prediction
    interaction_date TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create Audit Logs Table
CREATE TABLE audit_logs (
    audit_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    action VARCHAR(255) NOT NULL, -- e.g., 'INSERT', 'UPDATE', 'DELETE'
    table_name VARCHAR(50) NOT NULL, -- The table affected
    record_id INT NOT NULL, -- ID of the record affected
    changes TEXT, -- JSON field to store the before and after values
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create Roles Table
CREATE TABLE roles (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) UNIQUE NOT NULL
);

-- Create Permissions Table
CREATE TABLE permissions (
    permission_id SERIAL PRIMARY KEY,
    permission_name VARCHAR(50) UNIQUE NOT NULL
);

-- Create Role Permissions Table
CREATE TABLE role_permissions (
    role_id INT REFERENCES roles(role_id) ON DELETE CASCADE,
    permission_id INT REFERENCES permissions(permission_id) ON DELETE CASCADE,
    PRIMARY KEY (role_id, permission_id)
);

-- Create User Roles Table
CREATE TABLE user_roles (
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    role_id INT REFERENCES roles(role_id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, role_id)
);

-- Create Notifications Table
CREATE TABLE notifications (
    notification_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    sent_at TIMESTAMP DEFAULT NOW()
);

-- Create Departments Table
CREATE TABLE departments (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create Employee Departments Table
CREATE TABLE employee_departments (
    employee_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    department_id INT REFERENCES departments(department_id) ON DELETE CASCADE,
    PRIMARY KEY (employee_id, department_id),
    assigned_at TIMESTAMP DEFAULT NOW()
);

-- Create Files Table
CREATE TABLE files (
    file_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    file_name VARCHAR(255) NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    file_size INT,
    uploaded_at TIMESTAMP DEFAULT NOW()
);

-- Create Leave Requests Table
CREATE TABLE leave_requests (
    leave_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    leave_type VARCHAR(50) NOT NULL, -- e.g., 'sick', 'vacation'
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status VARCHAR(50) DEFAULT 'pending', -- e.g., 'approved', 'rejected', 'pending'
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
