# Database Setup

This directory contains the database schema and migration files for the PrTune application.

## Structure

```
database/
├── flyway-6.3.1/          # Flyway migration tool
│   └── conf/
│       └── flyway.conf    # Flyway configuration for local development
├── migrations/            # SQL migration files
│   └── V2026_02_03_1__Initial.sql
└── README.md             # This file
```

## Database Schema

The PrTune database includes the following tables:

1. **entry** - Stores content entries for prompt testing
   - id (UUID, PK)
   - content (TEXT)
   - created_date (TIMESTAMPTZ)
   - updated_date (TIMESTAMPTZ)

2. **eval_prompt** - Stores evaluation prompts
   - id (UUID, PK)
   - content (TEXT)
   - created_date (TIMESTAMPTZ)
   - updated_date (TIMESTAMPTZ)

3. **prompt_version** - Stores different versions of prompts
   - id (UUID, PK)
   - content (TEXT)
   - created_date (TIMESTAMPTZ)
   - updated_date (TIMESTAMPTZ)

4. **run** - Stores test runs
   - id (UUID, PK)
   - initial_prompt_id (UUID, FK -> prompt_version)
   - result_prompt_id (UUID, FK -> prompt_version)
   - eval_prompt_id (UUID, FK -> eval_prompt)
   - created_date (TIMESTAMPTZ)
   - updated_date (TIMESTAMPTZ)

5. **response** - Stores responses for each run/entry combination
   - id (UUID, PK)
   - run_id (UUID, FK -> run)
   - entry_id (UUID, FK -> entry)
   - created_date (TIMESTAMPTZ)
   - updated_date (TIMESTAMPTZ)

6. **evaluation** - Stores evaluation scores
   - id (UUID, PK)
   - response_id (UUID, FK -> response)
   - score (JSONB)
   - created_date (TIMESTAMPTZ)
   - updated_date (TIMESTAMPTZ)

## Prerequisites

1. PostgreSQL 12 or higher installed and running
2. Java Runtime Environment (JRE) 8 or higher for Flyway
3. Database user with CREATE DATABASE privileges

## Setup Instructions

### 1. Create the Database

```sql
CREATE DATABASE "PrTune";
```

Or using psql:
```bash
psql -U postgres -c "CREATE DATABASE \"PrTune\";"
```

### 2. Configure Database Connection

Update the `.env` file in the project root with your database credentials:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=PrTune
DB_USER=postgres
DB_PASSWORD=postgres
```

### 3. Run Migrations

Navigate to the Flyway directory and run migrations:

**Windows (PowerShell):**
```powershell
cd database/flyway-6.3.1
.\flyway.cmd -configFiles=conf\flyway.conf migrate
```

**Windows (Command Prompt):**
```cmd
cd database\flyway-6.3.1
flyway.cmd -configFiles=conf\flyway.conf migrate
```

**Linux/Mac:**
```bash
cd database/flyway-6.3.1
./flyway -configFiles=conf/flyway.conf migrate
```

## Migration Naming Convention

All migration files follow the pattern:
```
V{YYYY}_{MM}_{DD}_{N}__{Description}.sql
```

Examples:
- `V2026_02_03_1__Initial.sql` - Initial schema
- `V2026_02_04_1__AddIndexes.sql` - Add indexes
- `V2026_02_04_2__AlterTable.sql` - Second migration on the same day

## Common Flyway Commands

- **Migrate**: Apply pending migrations
  ```
  flyway.cmd -configFiles=conf\flyway.conf migrate
  ```

- **Info**: Display migration status
  ```
  flyway.cmd -configFiles=conf\flyway.conf info
  ```

- **Validate**: Validate applied migrations
  ```
  flyway.cmd -configFiles=conf\flyway.conf validate
  ```

- **Clean**: Drop all objects in the schema (⚠️ USE WITH CAUTION)
  ```
  flyway.cmd -configFiles=conf\flyway.conf clean
  ```

## SQLAlchemy Models

The corresponding SQLAlchemy models are located in `src/models/`:
- `base.py` - Base model and timestamp mixin
- `entry.py` - Entry model
- `eval_prompt.py` - EvalPrompt model
- `prompt_version.py` - PromptVersion model
- `run.py` - Run model
- `response.py` - Response model
- `evaluation.py` - Evaluation model

## Development Workflow

1. Make changes to the database schema by creating a new migration file
2. Run `flyway migrate` to apply the migration
3. Update the corresponding SQLAlchemy models if needed
4. Test the changes locally before committing

## Troubleshooting

### Connection Refused
- Ensure PostgreSQL is running
- Check that the host and port in `flyway.conf` are correct
- Verify firewall settings allow connections to PostgreSQL

### Authentication Failed
- Verify the username and password in `flyway.conf`
- Ensure the user has necessary permissions

### Migration Checksum Mismatch
- Don't modify migration files after they've been applied
- Use `flyway repair` to fix metadata issues (use carefully)
