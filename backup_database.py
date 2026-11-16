"""Create a private, compressed PostgreSQL dump for this project.

Uses pg_dump from PostgreSQL client tools and reads the connection URI from the
ignored local .env file. It intentionally rejects Supabase transaction-pooler
URIs because pg_dump needs a session-style database connection.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")


def main() -> int:
    uri = (os.environ.get("SUPABASE_BACKUP_URL") or "").strip()
    if not uri:
        print("Set SUPABASE_BACKUP_URL in your private .env to the Supabase direct or session connection URI.", file=sys.stderr)
        return 2
    executable = shutil.which("pg_dump")
    if not executable:
        print("pg_dump is not installed. Install PostgreSQL command-line tools and reopen the terminal.", file=sys.stderr)
        return 2
    parsed = urlparse(uri)
    if parsed.scheme not in ("postgres", "postgresql") or not parsed.hostname or not parsed.path.strip("/"):
        print("SUPABASE_BACKUP_URL is not a valid PostgreSQL connection URI.", file=sys.stderr)
        return 2
    if parsed.port == 6543:
        print("This is a transaction-pooler URI. Choose Supabase Direct or Session mode for pg_dump.", file=sys.stderr)
        return 2

    backup_dir = ROOT / "backups"
    backup_dir.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    target = backup_dir / f"knowledge-continuity-{stamp}.dump"
    query = parse_qs(parsed.query)
    env = os.environ.copy()
    env["PGPASSWORD"] = unquote(parsed.password or "")
    sslmode = query.get("sslmode", ["require"])[0]
    env["PGSSLMODE"] = sslmode if sslmode in {"require", "verify-ca", "verify-full"} else "require"
    args = [
        executable, "--format=custom", "--no-owner", "--no-acl", "--no-password",
        "--host", parsed.hostname,
        "--port", str(parsed.port or 5432),
        "--username", unquote(parsed.username or "postgres"),
        "--dbname", unquote(parsed.path.lstrip("/")),
        "--file", str(target),
    ]
    try:
        completed = subprocess.run(args, env=env, capture_output=True, text=True, timeout=900, check=False)
    except subprocess.TimeoutExpired:
        target.unlink(missing_ok=True)
        print("Backup timed out after 15 minutes; no usable backup was kept.", file=sys.stderr)
        return 1
    if completed.returncode != 0 or not target.is_file() or target.stat().st_size == 0:
        target.unlink(missing_ok=True)
        # pg_dump diagnostics can contain endpoint details; never echo them here.
        print("pg_dump failed. Check the Supabase backup URI, network access, and pg_dump version; no usable backup was kept.", file=sys.stderr)
        return 1
    print(f"Backup created: {target.relative_to(ROOT)} ({target.stat().st_size:,} bytes)")
    print("This file contains project data. Keep it encrypted and outside Git; test restore into a separate non-production database.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
