"""CB01 black-box evaluation. No reference implementation is included.
Usage: python evaluate.py path/to/integrity.py
Runs 12 behavioral checks against original program via subprocess.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

if len(sys.argv) < 2:
    raise SystemExit('Usage: python evaluate.py path/to/integrity.py')
PROGRAM = Path(sys.argv.pop(1)).resolve()
if not PROGRAM.is_file():
    raise SystemExit(f'File not found: {PROGRAM}')


class IntegrityBlackBox(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='cb01_')
        self.addCleanup(self.tmp.cleanup)
        base = Path(self.tmp.name)
        self.root = base / 'source'
        self.root.mkdir()
        self.manifest = base / 'baseline.json'

    def write(self, relative, payload):
        p = self.root / relative
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(payload)
        return p

    def call(self, *parts):
        return subprocess.run([sys.executable, str(PROGRAM), *map(str, parts)],
                              capture_output=True, text=True, encoding='utf-8',
                              errors='replace', timeout=30)

    def snapshot(self, manifest=None):
        return self.call('snapshot', self.root, '--output', manifest or self.manifest)

    def compare(self, manifest=None):
        return self.call('compare', self.root, '--baseline', manifest or self.manifest)

    def assert_error(self, r):
        self.assertEqual(r.returncode, 2, f'rc={r.returncode}; stderr={r.stderr}; stdout={r.stdout}')
        self.assertTrue(r.stderr.strip(), 'no stderr diagnostic')
        self.assertNotIn('Traceback (most recent call last)', r.stderr)
        self.assertFalse(r.stdout.strip(), 'unexpected stdout output')

    def assert_manifest_entry(self, data, name, content):
        entry = data['files'][name]
        self.assertEqual(set(entry), {'size', 'sha256'})
        self.assertEqual(entry['size'], len(content))
        self.assertEqual(entry['sha256'], hashlib.sha256(content).hexdigest())

    def test_01_snapshot_content(self):
        self.write('nested/hello.txt', b'hello')
        self.write('.hidden', b'x')
        self.write('binary.dat', bytes(range(256)))
        self.write('empty', b'')
        self.assertEqual(self.snapshot().returncode, 0)
        data = json.loads(self.manifest.read_text(encoding='utf-8'))
        self.assertEqual(set(data), {'version', 'files'})
        self.assertEqual(data['version'], 1)
        self.assertEqual(set(data['files']), {'nested/hello.txt', '.hidden', 'binary.dat', 'empty'})
        for key, payload in [('nested/hello.txt', b'hello'), ('.hidden', b'x'),
                             ('binary.dat', bytes(range(256))), ('empty', b'')]:
            self.assert_manifest_entry(data, key, payload)

    def test_02_deterministic_snapshot(self):
        self.write('z.txt', b'z')
        self.write('a.txt', b'a')
        self.assertEqual(self.snapshot().returncode, 0)
        first = self.manifest.read_bytes()
        self.assertEqual(self.snapshot().returncode, 0)
        self.assertEqual(first, self.manifest.read_bytes())

    def test_03_compare_no_change(self):
        self.write('x.txt', b'123')
        self.assertEqual(self.snapshot().returncode, 0)
        r = self.compare()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout), {'added': [], 'modified': [], 'deleted': []})

    def test_04_compare_changed_and_sorted(self):
        self.write('d2', b'deleted')
        self.write('d1', b'deleted')
        self.write('m2', b'original')
        self.write('m1', b'original')
        self.assertEqual(self.snapshot().returncode, 0)
        (self.root / 'd1').unlink()
        (self.root / 'd2').unlink()
        self.write('m1', b'changed!')
        self.write('m2', b'changed!')
        self.write('a2', b'added')
        self.write('a1', b'added')
        r = self.compare()
        self.assertEqual(r.returncode, 1, r.stderr)
        self.assertEqual(json.loads(r.stdout), {
            'added': ['a1', 'a2'], 'modified': ['m1', 'm2'], 'deleted': ['d1', 'd2']})

    def test_05_same_size_change_hash(self):
        self.write('same.dat', b'abc')
        self.assertEqual(self.snapshot().returncode, 0)
        self.write('same.dat', b'xyz')
        r = self.compare()
        self.assertEqual(r.returncode, 1, r.stderr)
        self.assertEqual(json.loads(r.stdout), {'added': [], 'modified': ['same.dat'], 'deleted': []})

    def test_06_missing_root(self):
        missing = Path(self.tmp.name) / 'missing'
        r = self.call('snapshot', missing, '--output', self.manifest)
        self.assert_error(r)
        self.assertFalse(self.manifest.exists())

    def test_07_invalid_json(self):
        self.write('a', b'X')
        self.manifest.write_text('{broken', encoding='utf-8')
        self.assert_error(self.compare())

    def test_08_invalid_schema(self):
        self.write('a', b'X')
        malformed = [
            {},
            {'version': 99, 'files': {}},
            {'version': 1, 'files': []},
            {'version': 1, 'files': {'a': {'size': -1, 'sha256': '0' * 64}}},
            {'version': 1, 'files': {'../escape': {'size': 1, 'sha256': '0' * 64}}},
            {'version': 1, 'files': {'a': {'size': 1, 'sha256': 'NOT-A-HASH'}}},
            {'version': 1, 'files': {'a': {'size': 1, 'sha256': '0' * 64, 'extra': 3}}},
        ]
        for obj in malformed:
            with self.subTest(obj=obj):
                self.manifest.write_text(json.dumps(obj), encoding='utf-8')
                self.assert_error(self.compare())

    def test_09_reject_manifest_inside_root(self):
        self.write('file', b'data')
        inside = self.root / 'subfolder' / 'manifest.json'
        self.assert_error(self.snapshot(inside))
        self.assertFalse(inside.exists())
        self.manifest.write_text('{"version": 1, "files": {}}', encoding='utf-8')
        self.assert_error(self.compare(self.root / 'file'))

    def test_10_output_parent_created(self):
        self.write('a.txt', b'data')
        nested = Path(self.tmp.name) / 'new' / 'nested' / 'out.json'
        r = self.snapshot(nested)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assert_manifest_entry(json.loads(nested.read_text(encoding='utf-8')), 'a.txt', b'data')

    def test_11_unicode_names(self):
        self.write('каталог/文書😀.txt', 'Привет'.encode('utf-8'))
        self.assertEqual(self.snapshot().returncode, 0)
        obj = json.loads(self.manifest.read_text(encoding='utf-8'))
        self.assertIn('каталог/文書😀.txt', obj['files'])
        r = self.compare()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout), {'added': [], 'modified': [], 'deleted': []})

    def test_12_ignore_symlinks(self):
        self.write('original.txt', b'data')
        (self.root / 'real_dir').mkdir()
        self.write('real_dir/inside.txt', b'inside')
        try:
            (self.root / 'link_file').symlink_to(self.root / 'original.txt')
            (self.root / 'link_dir').symlink_to(self.root / 'real_dir', target_is_directory=True)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f'symlinks unavailable on this environment: {exc}')
        r = self.snapshot()
        self.assertEqual(r.returncode, 0, r.stderr)
        files = json.loads(self.manifest.read_text(encoding='utf-8'))['files']
        self.assertEqual(set(files), {'original.txt', 'real_dir/inside.txt'})


if __name__ == '__main__':
    unittest.main(verbosity=2)
