import argparse
import json
import os
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', type=str, default=os.environ.get('KAGGLE_USERNAME'))
    parser.add_argument('-s', '--slug',  type=str, required=True)
    parser.add_argument('-m', '--metadata', type=Path, default=Path('./kernel-metadata.json'))
    parser.add_argument('-r', '--revision', type=str)
    args = parser.parse_args()

    if args.username is None:
        sys.exit("username is not set")

    with args.metadata.open('r') as m:
        metadata = json.load(m)

    code_file = Path(metadata['code_file'])
    with code_file.open('r') as c:
        code = c.read()
    code = code.replace("REVISION = None  # <", f"REVISION = '{args.revision}'", 1)

    metadata['id'] = args.username + '/' + args.slug
    metadata['title'] = args.slug

    with code_file.open('w') as c:
        c.write(code)

    with args.metadata.open('w') as m:
        json.dump(metadata, m)


if __name__ == '__main__':
    main()
