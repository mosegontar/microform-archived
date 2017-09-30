#!/usr/bin/env python
import os
import pydoc
import re
import sys
import shlex
import tempfile
from subprocess import call


from article_format import ArticleFormatter
from mercury import Mercury


class Reader(object):

    def __init__(self, api_key):
        self.parser = Mercury(api_key)
        self.pager = self._create_pager_args()

    def read(self, url):
        result = self.parser.get(url)
        if not result.get('content'):
            print('No content')
            return

        article = ArticleFormatter(result['content'], True)

        self._display(article.render())

    def _display(self, article):
        if self.pager:
            with tempfile.NamedTemporaryFile(suffix='.markdown') as tf:
                tf.write(bytes(article, 'utf-8'))
                tf.flush()
                call(self.pager+[tf.name])

                tf.seek(0)
                tf.read()
        else:
            print(article)

    def _create_pager_args(self):
        pager = os.environ.get('MICROFORM_PAGER')
        if not pager:
            return None
        return shlex.split(pager)


def main():
    api_key = os.environ.get('MERCURY_API_KEY')

    if not api_key:
        print('You need to set an Mercury Parser API key as an environment variable\n',
              'E.g., on Bash: "export MERCURY_API_KEY=XXXXXXXXXXXXX"')
        return

    args = sys.argv[1:]
    if args:
        url = args[-1]
    else:
        print('No URL supplied')
        return

    reader = Reader(api_key).read(url)

if __name__ == '__main__':
    main()
