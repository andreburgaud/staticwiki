from markdown_it import MarkdownIt
from mdit_py_plugins.dollarmath import dollarmath_plugin
from mdit_py_plugins.footnote import footnote_plugin

from jinja2 import Environment, FileSystemLoader, select_autoescape

from pygments import highlight
from pygments.formatters import HtmlFormatter

from pygments.lexers import (get_lexer_by_name)

class CodeHtmlFormatter(HtmlFormatter):

    def wrap(self, source, outfile):
        return self._wrap_code(source)

    def _wrap_code(self, source):
        yield 0, '<div class="highlight">'
        for i, t in source:
            #if i == 1:
                # it's a line of formatted code
            #    t += '<br>'
            yield i, t
        yield 0, '</div>'

def highlight_code(code, lang, *attrs):
    #print(f"Debug >>> highlight_code {code=}, {lang=}")
    if lang:
        lexer = get_lexer_by_name(lang)
        #return highlight(code, lexer, CodeHtmlFormatter())
        return highlight(code, lexer, CodeHtmlFormatter())
    else:
        return code


# Markdown
md = MarkdownIt("commonmark", {"linkify": True, # Autoconvert URL-like texts to links
                               "typographer": True, # Used by smartquotes rule
                               "html": True, # Enable HTML tags in source
                               "breaks": False, # Convert '\n' in paragraphs into <br>
                               "highlight": highlight_code
                               }).use(dollarmath_plugin).use(footnote_plugin)

md.enable([
    "linkify",
    "replacements",
    "smartquotes"])


# Templates (from filesystem)
loader = FileSystemLoader(searchpath="./")
env = Environment(loader=loader)
template = env.get_template("page.html")

for md_file in ("crypt2go.md", "fold.md"):
    base = md_file.split(".")[0]
    with open(md_file) as f:
        data = f.read()

    content = md.render(data)

    with open(f"{base}.html", "w") as f:
        f.write(template.render(content=content, title=base.capitalize()))

