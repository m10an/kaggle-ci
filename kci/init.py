import argparse
import json
import os
import sys
from pathlib import Path

SOLUTION_DIR = Path('solution')
METADATA_FILE = 'kernel-metadata.json'
EXT_DICT = {
    ('python', 'script'): '.py',
    ('python', 'notebook'): '.ipynb',
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', type=str, default=os.environ.get('KAGGLE_USERNAME'))
    parser.add_argument('-s', '--slug',  type=str, required=True)
    parser.add_argument('-r', '--revision', type=str)
    args = parser.parse_args()

    if args.username is None:
        sys.exit("username is not set")

    with (SOLUTION_DIR / METADATA_FILE).open('r') as m:
        metadata = json.load(m)

    code_file = metadata['kernel_type'] + EXT_DICT[metadata['language'], metadata['kernel_type']]
    with (SOLUTION_DIR / code_file).open('r') as c:
        code = c.read()
    code = code.replace("REVISION = None  # <", f"REVISION = '{args.revision}'", 1)

    metadata['id'] = args.username + '/' + args.slug
    metadata['code_file'] = code_file
    metadata['title'] = args.slug

    with (Path() / code_file).open('w') as c:
        c.write(code)

    with (Path() / METADATA_FILE).open('w') as m:
        json.dump(metadata, m)


if __name__ == '__main__':
    main()
