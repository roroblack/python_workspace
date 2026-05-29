import subprocess
from pathlib import Path
root = Path(r'C:\Users\playdata2\Documents\python_workspace')
with (root / 'tmp_git_action_output.txt').open('w', encoding='utf-8') as f:
    for cmd in [
        ['git', 'add', 'test_numpy', 'test_pandas'],
        ['git', 'commit', '-m', 'Update test_numpy and test_pandas'],
        ['git', 'push', 'origin', 'HEAD'],
        ['git', 'pull', 'origin', 'HEAD'],
    ]:
        f.write(f'$ {' '.join(cmd)}\n')
        try:
            out = subprocess.check_output(cmd, cwd=root, stderr=subprocess.STDOUT, text=True)
        except subprocess.CalledProcessError as e:
            out = e.output
        f.write(out)
        f.write('\n')
