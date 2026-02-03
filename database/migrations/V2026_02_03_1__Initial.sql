-- ========================
-- PRTUNE INITIAL SCHEMA
-- ========================

-- Entry table: stores content entries for prompt testing
CREATE TABLE entry (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    created_date TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Evaluation Prompt table: stores prompts used for evaluation
CREATE TABLE eval_prompt (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    created_date TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Prompt Version table: stores different versions of prompts
CREATE TABLE prompt_version (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    created_date TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Run table: stores test runs with initial prompt, result prompt, and eval prompt
CREATE TABLE run (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    initial_prompt_id UUID NOT NULL,
    result_prompt_id UUID NOT NULL,
    eval_prompt_id UUID NOT NULL,
    created_date TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_run_initial_prompt FOREIGN KEY (initial_prompt_id) REFERENCES prompt_version(id) ON DELETE CASCADE,
    CONSTRAINT fk_run_result_prompt FOREIGN KEY (result_prompt_id) REFERENCES prompt_version(id) ON DELETE CASCADE,
    CONSTRAINT fk_run_eval_prompt FOREIGN KEY (eval_prompt_id) REFERENCES eval_prompt(id) ON DELETE CASCADE
);

-- Response table: stores responses for each run and entry combination
CREATE TABLE response (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    run_id UUID NOT NULL,
    entry_id UUID NOT NULL,
    created_date TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_response_run FOREIGN KEY (run_id) REFERENCES run(id) ON DELETE CASCADE,
    CONSTRAINT fk_response_entry FOREIGN KEY (entry_id) REFERENCES entry(id) ON DELETE CASCADE
);

-- Evaluation table: stores evaluation scores for responses
CREATE TABLE evaluation (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    response_id UUID NOT NULL,
    score JSONB NOT NULL,
    created_date TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_evaluation_response FOREIGN KEY (response_id) REFERENCES response(id) ON DELETE CASCADE
);

-- ========================
-- INDEXES
-- ========================

CREATE INDEX idx_run_initial_prompt ON run(initial_prompt_id);
CREATE INDEX idx_run_result_prompt ON run(result_prompt_id);
CREATE INDEX idx_run_eval_prompt ON run(eval_prompt_id);
CREATE INDEX idx_response_run ON response(run_id);
CREATE INDEX idx_response_entry ON response(entry_id);
CREATE INDEX idx_evaluation_response ON evaluation(response_id);
