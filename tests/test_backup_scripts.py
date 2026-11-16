"""Safety checks for backup tooling (no remote database is contacted)."""
from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import backup_database
import restore_database


class BackupToolSafetyTests(unittest.TestCase):
    def test_backup_refuses_transaction_pooler_before_running_pg_dump(self) -> None:
        with patch.dict(os.environ, {"SUPABASE_BACKUP_URL":"postgresql://postgres.ref:pw@aws.pooler.supabase.com:6543/postgres"}, clear=False), \
             patch.object(backup_database.shutil, "which", return_value="pg_dump"), \
             patch.object(backup_database.subprocess, "run") as run:
            self.assertEqual(backup_database.main(), 2)
            run.assert_not_called()

    def test_restore_refuses_same_supabase_project_even_via_different_hosts(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            backup_dir=root/"backups"
            backup_dir.mkdir()
            dump=backup_dir/"sample.dump"
            dump.write_bytes(b"synthetic placeholder")
            production="postgresql://postgres.projectref:pw@aws.pooler.supabase.com:6543/postgres"
            direct_same_project="postgresql://postgres:pw@db.projectref.supabase.co:5432/postgres"
            env={"DATABASE_URL":production,"SUPABASE_RESTORE_URL":direct_same_project,"KC_RESTORE_CONFIRM":"non-production"}
            with patch.object(restore_database, "ROOT", root), patch.dict(os.environ, env, clear=False), \
                 patch.object(restore_database.shutil, "which", return_value="pg_restore"), \
                 patch.object(restore_database.subprocess, "run") as run, patch("sys.argv", ["restore_database.py", str(dump)]):
                self.assertEqual(restore_database.main(), 2)
                run.assert_not_called()

    def test_restore_requires_nonproduction_confirmation(self) -> None:
        with patch.dict(os.environ, {"KC_RESTORE_CONFIRM":""}, clear=False), patch("sys.argv", ["restore_database.py"]):
            self.assertEqual(restore_database.main(), 2)


if __name__ == "__main__":
    unittest.main()
