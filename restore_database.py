"""Restore a project dump to a separate, explicitly confirmed staging database."""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python restore_database.py backups/<backup-file>.dump")
        return 2
    if os.environ.get("KC_RESTORE_CONFIRM") != "non-production":
        print("Set KC_RESTORE_CONFIRM=non-production only after creating an empty staging Supabase project.", file=sys.stderr)
        return 2
    backup = Path(sys.argv[1]).resolve()
    if not backup.is_relative_to((ROOT / "backups").resolve()) or not backup.is_file():
        print("Choose an existing dump file inside this repository's ignored backups folder.", file=sys.stderr)
        return 2
    uri = (os.environ.get("SUPABASE_RESTORE_URL") or "").strip()
    if not uri:
        print("Set SUPABASE_RESTORE_URL in .env to the separate staging project's Direct or Session URI.", file=sys.stderr)
        return 2
    production_uri = (os.environ.get("DATABASE_URL") or "").strip()
    if not production_uri:
        print("Set DATABASE_URL to the configured production URI so the restore safety check can compare project identity.", file=sys.stderr)
        return 2
    target = urlparse(uri)
    production = urlparse(production_uri)
    if not target.hostname or target.scheme not in ("postgres", "postgresql"):
        print("SUPABASE_RESTORE_URL is not a valid PostgreSQL URI.", file=sys.stderr)
        return 2
    if target.port == 6543:
        print("Choose a Direct or Session connection; transaction pooling is not for pg_restore.", file=sys.stderr)
        return 2
    def project_ref(parsed):
        host=(parsed.hostname or "").split(".")
        if len(host)>=4 and host[0]=="db" and host[-2:]==["supabase","co"]:
            return host[1]
        user=unquote(parsed.username or "")
        if user.startswith("postgres."):
            return user.split(".",1)[1]
        return None
    prod_ref=project_ref(production)
    target_ref=project_ref(target)
    same_supabase_project=prod_ref and target_ref and prod_ref==target_ref
    same_generic_database=production.hostname and target.hostname==production.hostname and target.path==production.path
    if same_supabase_project or same_generic_database:
        print("Refusing to restore into the configured production database.", file=sys.stderr)
        return 2
    executable = shutil.which("pg_restore")
    if not executable:
        print("pg_restore is not installed. Install PostgreSQL command-line tools and reopen the terminal.", file=sys.stderr)
        return 2
    query = parse_qs(target.query)
    env = os.environ.copy()
    env["PGPASSWORD"] = unquote(target.password or "")
    sslmode = query.get("sslmode", ["require"])[0]
    env["PGSSLMODE"] = sslmode if sslmode in {"require", "verify-ca", "verify-full"} else "require"
    args = [
        executable, "--no-owner", "--no-acl", "--exit-on-error", "--single-transaction",
        "--host", target.hostname,
        "--port", str(target.port or 5432),
        "--username", unquote(target.username or "postgres"),
        "--dbname", unquote(target.path.lstrip("/")),
        str(backup),
    ]
    try:
        completed = subprocess.run(args, env=env, capture_output=True, text=True, timeout=1800, check=False)
    except subprocess.TimeoutExpired:
        print("Restore timed out. Check the staging database before trying again.", file=sys.stderr)
        return 1
    if completed.returncode != 0:
        print("Restore failed. Check the staging endpoint, permissions, and that the target project is empty; review local PostgreSQL diagnostics without sharing credentials.", file=sys.stderr)
        return 1
    print("Restore completed to the confirmed staging project. Verify the row counts and run the reviewer-builder-recipient journey there.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
