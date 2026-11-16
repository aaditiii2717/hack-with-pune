# Supabase backup and restore drill

The app stores handover text, structured records, and uploaded originals in PostgreSQL. A database dump therefore includes the app's uploaded originals. Keep dumps private: they may contain confidential project material.

## Create a backup on Windows

1. Install PostgreSQL command-line tools so `pg_dump` is available in PowerShell.
2. In Supabase, open **Connect** and copy a **Direct** connection URI. If Direct connectivity is unavailable on your network, use the **Session pooler** URI. Do not use the transaction pooler for `pg_dump` or `pg_restore`.
3. Put that URI in the ignored local `.env` as `SUPABASE_BACKUP_URL`. Never paste it into chat, GitHub, or a screenshot.
4. From the repository folder, run:

   ```powershell
   python backup_database.py
   ```

5. The script writes a timestamped custom-format dump under `backups/`, rejects transaction-pooler URLs, keeps the password out of command arguments and logs, and removes partial output after failure. The folder is Git-ignored.
6. Copy the dump to encrypted storage with restricted access. A PostgreSQL custom-format dump is compressed, **not encrypted**. Do not treat an ordinary synced folder as a protected backup unless that storage is encrypted and access-controlled.

## Restore drill (staging only)

1. Create a separate, empty Supabase staging project. Do not connect the app or Vercel production deployment to it.
2. Put its Direct or Session URI in `.env` as `SUPABASE_RESTORE_URL`.
3. Set `$env:KC_RESTORE_CONFIRM = "non-production"` in PowerShell. Verify the staging project URL and that the target database is empty.
4. Run `python restore_database.py backups\<dump-file>.dump`. The script refuses transaction-pooler URLs and refuses the configured production database. It does not drop existing objects; use a new, empty staging project.
5. Verify tables and representative handovers in the restored database, point a local app instance at staging, then complete reviewer → builder → recipient flows, including an original-file download.
6. Record the dump timestamp, restore timestamp, result, and any gaps. Delete the staging project and local test copy when the drill is complete.

## Hosted backup options

Check the Supabase plan in the Dashboard. Supabase documents daily managed database backups for Pro and higher plans; its Free plan guidance is to export regularly with the Supabase CLI and keep an off-site copy. Managed backups do not replace a restore drill. Database backups also do not include files stored separately through Supabase Storage; this app currently stores originals in PostgreSQL rows.

Supabase recommends a direct connection for native dump/restore commands. Vercel app traffic should continue using the transaction pooler, which is designed for short-lived serverless requests. See [Supabase backup guidance](https://supabase.com/docs/guides/platform/backups) and [connection-method guidance](https://supabase.com/docs/guides/database/connecting-to-postgres).

## Current status

Scripts and runbook are provided; no live backup or restore has been performed from this development environment. Mark the drill complete only after the staging restore and workflow check above succeed.
