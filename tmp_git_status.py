import subprocess
from pathlib import Path
root = Path(r'C:\Users\playdata2\Documents\python_workspace')
with (root / 'tmp_git_output.txt').open('w', encoding='utf-8') as f:
    for cmd in [
        ['git', 'status', '--short', '--', 'test_numpy', 'test_pandas'],
        ['git', 'remote', '-v'],
    ]:
        f.write(f'$ {' '.join(cmd)}\n')
        try:
            out = subprocess.check_output(cmd, cwd=root, stderr=subprocess.STDOUT, text=True)
        except subprocess.CalledProcessError as e:
            out = e.output
        f.write(out)
        f.write('\n')
