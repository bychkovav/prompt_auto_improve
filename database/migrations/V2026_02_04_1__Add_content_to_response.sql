-- Add content column to response table
ALTER TABLE response ADD COLUMN content TEXT NOT NULL DEFAULT '';

-- Remove the default after adding the column (so new rows require explicit content)
ALTER TABLE response ALTER COLUMN content DROP DEFAULT;
