import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
EXPECTED = {
    'base-verification.json': 'fe503a15f32d4caa824ab878cb815ca85b50b5d2046e91e668862aff4405b247',
    'prefix-verification.json': '2c9319cba6e80ac28f17cffe0297cb6695e08c762f37214ba601a6d20d7cd896',
    'independent-verification.json': '55377508bae480f68ca75530a45bb67a582f4a1c199cf63fd07f7aa353dd7227',
    'diagonal-verification.json': '436882f0900b55d4f163eca74f9486b32baee3f94816cba63ee2b3e05766cdf6',
}


def main():
    with (ROOT / 'base-verification.json').open('wb') as output:
        subprocess.run([sys.executable, str(ROOT / 'verify_base.py')], stdout=output, check=True)
    commands = [
        ('verify_prefix.py', '--maximum', '35', '--output', 'prefix-verification.json'),
        ('verify_independent.py', '--maximum', '16', '--output', 'independent-verification.json'),
        ('verify_diagonal.py', '--maximum-source', '18', '--output', 'diagonal-verification.json'),
    ]
    for command in commands:
        subprocess.run([sys.executable, *command], cwd=ROOT, stdout=subprocess.PIPE, check=True)
    outputs = []
    for name, expected in EXPECTED.items():
        content = (ROOT / name).read_bytes()
        actual = hashlib.sha256(content).hexdigest()
        assert actual == expected, name
        outputs.append({'name': name, 'bytes': len(content), 'sha256': actual})
    result = {'status': 'pass', 'arithmetic': 'exact integers and finite sets', 'outputs': outputs}
    (ROOT / 'verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
