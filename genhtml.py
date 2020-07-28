#!/usr/bin/env python

import sys
from pathlib import Path
from itertools import chain

HEAD = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title></title>
</head>
<body>
    <main class="container">
'''

TAIL = '''
    </main>
</body>
</html>
'''


def gen_row(img_path):
    path = Path(img_path)
    filename = path.name
    return f'''
        <div class="row">
            <p>{filename}</p>
            <img src="{path}" />
        </div>
    '''


def sort_by_period(item):
    # memory-day.svg
    prefix, _, period = Path(item).stem.rpartition('-')
    sdict = {
        'hour': 1,
        'day': 2,
        'week': 3,
        'month': 4,
        'year': 5,
        'decade': 6
    }
    skey = (prefix, sdict.get(period, 0))
    return skey


def main():
    img_dir = sys.argv[1]
    images = chain(Path(img_dir).glob('*.png'), Path(img_dir).glob('*.svg'))
    html = HEAD
    for i in sorted(images, key=sort_by_period):
        html += gen_row(i)
    html += TAIL
    Path('index.html').write_text(html)


if __name__ == '__main__':
    main()
