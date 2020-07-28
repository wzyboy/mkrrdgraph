#!/usr/bin/env python

import sys
import itertools
from pathlib import Path

HEAD = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title></title>
<style>
.container {
    display: flex;
}

.col {
    padding: 1em;
}

.row {
    width: 25vw;
}

img {
    width: 100%;
}
</style>
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
    images = itertools.chain(Path(img_dir).glob('*.png'), Path(img_dir).glob('*.svg'))
    images = sorted(images, key=sort_by_period)

    html = HEAD
    for key, group in itertools.groupby(images, key=lambda x: Path(x).stem.rpartition('-')[0]):
        images = list(group)
        col_html = f'\n<div class="col">\n<p>{key}</p>'
        for image in images:
            col_html += gen_row(image)
        col_html += '</div>\n'
        html += col_html
    html += TAIL
    Path('index.html').write_text(html)


if __name__ == '__main__':
    main()
