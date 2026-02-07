-- ========================
-- Make content nullable in response table
-- ========================
-- This allows responses to be created without content initially.
-- The content can be set later when the model output is received.

ALTER TABLE response 
ALTER COLUMN content DROP NOT NULL;
