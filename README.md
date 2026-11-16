# MatchaTrail · IM2 Account Feature

This milestone implements Explorer registration with Django templates, Django password hashing, and PostgreSQL.

## Local setup

1. Install Python 3.10+ and PostgreSQL 14+. Create a PostgreSQL database and a login role that owns it. For example, in `psql` as a PostgreSQL administrator:

   ```sql
   CREATE ROLE matchatrail LOGIN;
   \password matchatrail
   CREATE DATABASE matchatrail OWNER matchatrail;
   ```

2. Open the extracted `MatchaTrail` directory and create a virtual environment.

   ```text
   python -m venv .venv
   ```

   Activate it with `.venv\Scripts\Activate.ps1` in PowerShell or `source .venv/bin/activate` in Bash. Then run:

   ```text
   python -m pip install -r requirements.txt
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

3. Copy `.env.example` to `.env`. Set the generated value as a double-quoted `DJANGO_SECRET_KEY` and enter your database credentials. For Supabase, use the PostgreSQL connection details from the direct connection or session pooler and set `POSTGRES_SSLMODE=require`.

4. Run `python manage.py migrate` and `python manage.py runserver`.
5. Open http://127.0.0.1:8000/register/ and create an Explorer account.

Run `python manage.py test` with a PostgreSQL role that can create test databases.
