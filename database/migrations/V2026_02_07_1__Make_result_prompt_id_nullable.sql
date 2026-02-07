-- ========================
-- Make result_prompt_id nullable in run table
-- ========================
-- This allows runs to be created without a result_prompt_id initially.
-- The result_prompt_id can be set later when an improved prompt is generated.

ALTER TABLE run 
ALTER COLUMN result_prompt_id DROP NOT NULL;
