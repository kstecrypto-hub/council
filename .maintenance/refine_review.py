"""Finish formatting after the approved, documentation-only amendment."""
from pathlib import Path
root = Path(__file__).resolve().parents[1]
for name in ('PART_5_TRANSACTIONS_IDEMPOTENCY_CONFLICTS.md', 'TYPED_INTERACTION_CONTRACTS.md'):
    path = root / 'docs' / name
    lines = path.read_text(encoding='utf-8').splitlines()
    path.write_text('\n'.join(line.rstrip() if line.startswith('**Status:** DESIGN AMENDED') else line for line in lines) + '\n', encoding='utf-8')
print('Amended status-line formatting corrected; no runtime completion claimed.')
