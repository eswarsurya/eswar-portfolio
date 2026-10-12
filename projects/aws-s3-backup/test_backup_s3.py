import tempfile
import unittest
from pathlib import Path
from backup_s3 import make_archive, safe_extract

class BackupTests(unittest.TestCase):
    def test_archive_and_restore(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); source = root / 'source'; source.mkdir()
            (source / 'hello.txt').write_text('hello')
            archive = root / 'archive.tar.gz'; make_archive(source, archive)
            output = root / 'output'; safe_extract(archive, output)
            self.assertEqual((output / 'source' / 'hello.txt').read_text(), 'hello')

    def test_missing_source_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                make_archive(Path(tmp) / 'missing', Path(tmp) / 'archive.tar.gz')

if __name__ == '__main__': unittest.main()