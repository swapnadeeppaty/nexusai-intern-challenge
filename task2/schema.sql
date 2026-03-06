CREATE TABLE call_records (
    id SERIAL PRIMARY KEY,

    customer_phone VARCHAR(20) NOT NULL,

    channel VARCHAR(20) NOT NULL,

    transcript TEXT NOT NULL,

    ai_response TEXT NOT NULL,

    intent VARCHAR(100),

    outcome VARCHAR(20) NOT NULL,

    confidence_score FLOAT NOT NULL CHECK (confidence_score BETWEEN 0 AND 1),

    csat_score INT CHECK (csat_score BETWEEN 1 AND 5),

    duration_seconds INT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);