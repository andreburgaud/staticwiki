# README


# Development


```
$ python3 -m venv .venv --prompt staticwiki
$ . .venv/bin/activate
$ pip install -r requirements.txt
$ pip install -e .
$ make test
$ deactivate
```

## Dependencies

### Markdown

* `markdown-it-py`
* PyPI: https://pypi.org/project/markdown-it-py/
* GitHub: https://github.com/executablebooks/markdown-it-py
* Documentation: https://markdown-it-py.readthedocs.io/en/latest/
* CommonMark Spec: https://spec.commonmark.org/0.30/
* `mdit-py-plugins`: https://mdit-py-plugins.readthedocs.io/en/latest/
  * Footnotes
  * Front-Matter
  * Word-count
  * Math
* `linkify-it-py`: allows to write raw URL in Markdown that will be properly wrapped up in the resulting HTML.

**Note**: The package `mdit-py-plugins` requires `markdown-it-py` so `markdown-it-py` does not show up in the top-level package requirements when running `pip-chill`. Installing `mdit-py-plugins` automatically installs `markdown-it-py`


## Styles

### Bulma


```css
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.3/css/bulma.min.css" integrity="sha256-UDtbUHqpVVfXmdJcQVU/bfDEr9xldf3Dbd0ShD0Uf/Y=" crossorigin="anonymous">
```

### Pure CSS

```css
<link rel="stylesheet" href="https://unpkg.com/purecss@2.0.6/build/pure-min.css" integrity="sha384-Uu6IeWbM+gzNVXJcM9XV3SohHtmWE+3VGi496jvgX1jyvDTXfdK+rfZc8C1Aehk5" crossorigin="anonymous">
```