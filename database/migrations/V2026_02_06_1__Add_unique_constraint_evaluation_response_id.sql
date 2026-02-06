-- Add unique constraint on evaluation.response_id
-- This ensures each response can have only one evaluation

ALTER TABLE evaluation
ADD CONSTRAINT uk_evaluation_response_id UNIQUE (response_id);
