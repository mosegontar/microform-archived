#!/usr/bin/env python
import html
import os
import pydoc
import re
import sys
import shlex
import tempfile
from subprocess import call

from tomd import Tomd

from mercury import Mercury



class References(object):

    def __init__(self):
        self.references = []
        self.pattern = r'<a.*?href="(.*?)".*?>(.*?)<\/a>'

    def process(self, content):

        new_string, n = re.subn(self.pattern,
                                self._get_ref,
                                content,
                                count=1)

        if n < 1:
            return Tomd(content).markdown

        return self.process(new_string)

    def get_endnotes(self):
        header = """## REFERENCES\n"""
        header += '=' * len(header)
        header += '\n\n'

        endnotes = ''
        for i, ref in enumerate(self.references):
            num = i + 1
            endnotes += '[{}] {}\n'.format(num, ref)

        return header + endnotes


    def _get_ref(self, matchobj):

        url, text = matchobj.groups()

        self.references.append(url)

        return '{} [^{}]'.format(text, len(self.references))




class Reader(object):

    def __init__(self, api_key):
        self.parser = Mercury(api_key)
        self.pager = self._create_pager_args()

    def read(self, url):
        result = self.parser.get(url)
        if not result.get('content'):
            print('No content')
            return

        article = self._format(result['content'])

        self._display(article)

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

    def _format(self, content):

        ref = References()
        content =  ref.process(html.unescape(content))
        endotes = ref.get_endnotes()
        return content + '\n' + endotes


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
