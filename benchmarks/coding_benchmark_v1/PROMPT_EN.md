# Local AI Workstation — Coding Benchmark CB01

**Frozen prompt v1.0 — SHA-256 recorded separately.**

Copy only the text between `PROMPT START` and `PROMPT END` into a fresh LM Studio chat. Do not add or remove instructions.

--- PROMPT START ---
You are a Python software engineer. Build a small, reliable command-line utility named "Directory Integrity Scanner" for Python 3.11+ on Windows or Linux.

Create exactly two source files: `integrity.py` (the program) and `test_integrity.py` (your own automated tests using only Python's standard library). Do not use third-party packages. The program must not modify or delete any scanned files.

COMMANDS
1. `python integrity.py snapshot ROOT --output MANIFEST`
2. `python integrity.py compare ROOT --baseline MANIFEST`

ROOT is an existing directory. Scan its regular files recursively, including hidden files, and compute SHA-256 of file content by reading in chunks. Ignore symbolic links completely (both symlinked files and symlinked directories); do not follow them. Do not include directory entries in the manifest. Use relative paths with forward slashes, regardless of operating system. Paths are case-sensitive identifiers in the manifest. The manifest must be located OUTSIDE ROOT. Reject either command if its manifest/baseline path resolves to a location inside ROOT (including ROOT itself). Do not create ROOT.

MANIFEST FORMAT
Snapshot writes valid UTF-8 JSON with exactly this structure (no extra top-level or per-file fields):
{
  "version": 1,
  "files": {
    "relative/path.txt": {"size": 3, "sha256": "<64 lowercase hexadecimal characters>"}
  }
}
`size` is the byte count, including for binary files. Empty folders do not appear. The output must be deterministic for identical directory contents: sort paths and JSON keys, use stable formatting, and do not include timestamps or machine-dependent absolute paths. The manifest may overwrite an existing file. Write it atomically: if creating the snapshot fails, do not leave a truncated/partially written destination manifest. Create parent directories for the output only when necessary.

COMPARE
Read and strictly validate the baseline JSON (top-level keys, version, files object, each relative path and its size/hash fields; reject malformed entries rather than silently ignoring them). Scan ROOT using the same rules as snapshot. Print exactly one JSON object to stdout, with exactly the keys `added`, `modified`, `deleted`, each containing a lexicographically sorted list of relative paths. A path is modified if its byte count OR SHA-256 differs. Example: {"added": ["new.txt"], "modified": ["a.txt"], "deleted": ["old.txt"]}. Do not change ROOT or the baseline during compare.

EXIT CODES AND ERRORS
- Snapshot success: 0.
- Compare with no changes: 0.
- Compare with any changes: 1.
- Any invalid arguments, missing ROOT, unreadable file, malformed baseline, unsafe manifest location, or other operational error: 2.
- On errors, print a useful message to stderr, never a Python traceback, and do not print a comparison JSON object to stdout.
- Do not suppress scanning errors or treat unreadable files as absent.

IMPLEMENTATION AND RESPONSE
- Keep code readable and logically separated (CLI, scanning/hashing, validation, comparison).
- Use streaming/chunked file hashing, not loading whole files into memory.
- Avoid unnecessary dependencies or elaborate frameworks.
- `test_integrity.py` must contain meaningful runnable `unittest` tests for normal operation and important edge cases, using temporary directories; tests must not need network access or administrator permissions.
- Return two complete code blocks, one headed `# integrity.py` and the other `# test_integrity.py`, followed by at most 120 words describing key design decisions and how to run the tests. Do not omit code or replace it with pseudocode.
--- PROMPT END ---
