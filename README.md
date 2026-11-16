# MatchaTrail · IM2 Account Feature

This milestone implements Explorer registration, login/logout, and role-based Explorer and Café Owner dashboards with Django templates, Django authentication, and PostgreSQL.

## Local setup

For local development without PostgreSQL credentials, set `DJANGO_USE_SQLITE=1` in `.env`, together with a generated `DJANGO_SECRET_KEY` and `DJANGO_DEBUG=1`. This uses an ignored local `db.sqlite3` file. Install dependencies, then run `python manage.py migrate` and `python manage.py runserver`. Set `DJANGO_USE_SQLITE=0` to use the PostgreSQL configuration below; the two databases keep separate data.

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

## Role-based dashboards

Visit `/login/` after registering. Login always redirects to `/dashboard/`, which sends Explorers to `/dashboard/explorer/` and Café Owners to `/dashboard/owner/` based on their stored account role. Each dashboard has role-specific content and navigation. Anonymous visitors must log in; accessing another role's dashboard returns HTTP 403. Logout uses a CSRF-protected POST form.

Public registration always creates Explorers. To prepare a Café Owner for a demo, register a second account and assign its role from the trusted Django shell:

```text
python manage.py shell
```

```python
from accounts.models import User
owner = User.objects.get(username="your_owner_username")
owner.role = User.Role.OWNER
owner.save(update_fields=["role"])
```

Sign in as each account in separate browser sessions to compare dashboards and try opening the other dashboard's URL. Café discovery, saved places, listings, and menu management are marked as planned features; this milestone provides the account dashboards and access controls.

The test suite covers registration validation, role assignment, login routing, role-specific rendering, cross-role access denial, invalid credentials, and logout.
