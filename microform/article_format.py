import html
import re

from tomd import Tomd


class References(object):

    def __init__(self):
        self.references = []
        self.pattern = r'<a.*?href="(.*?)".*?>(.*?)<\/a>'
        self.content = ''
        self.endnotes = """
REFERENCES
==========\n\n
"""

    def process(self, content):
        new_string, n = re.subn(self.pattern,
                                self._get_ref,
                                content,
                                count=1)

        if n < 1:
            self._create_endnotes()
            return content

        return self.process(new_string)

    def _create_endnotes(self):

        endnotes = ''
        for i, ref in enumerate(self.references):
            num = i + 1
            endnotes += '[{}] {}\n'.format(num, ref)

        self.endnotes += endnotes

    def _get_ref(self, matchobj):

        url, text = matchobj.groups()

        self.references.append(url)

        return '{} [^{}]'.format(text, len(self.references))


class ArticleFormatter(object):

    def __init__(self, content, references=False):
        self.content = content
        self.refs = References() if references else None

    def render(self):

        if self.refs:
            self.content = self.refs.process(html.unescape(self.content))
            self.content += self.refs.endnotes

        return Tomd(self.content).markdown
