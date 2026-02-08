-- Add meta JSONB column to prompt_version table
ALTER TABLE prompt_version ADD COLUMN meta JSONB;
