"""

Automatically re-build Sphinx docs while editing, serve docs on an
HTTP port, and also reload any browsers pointed to the docs.

"""

import glob

from livereload import Server, shell
from livereload.watcher import Watcher

sphinx = ".venv/bin/python3 .venv/bin/sphinx-build -E -b html docs docs/_build"
dist = "/usr/local/bin/npm run dist"
both = dist + '; ' + sphinx


class CustomWatcher(Watcher):
    """ Handle recursive globs with Python 3.5+ globbing  """

    def is_glob_changed(self, path, ignore=None):
        for f in glob.glob(path, recursive=True):
            if self.is_file_changed(f, ignore):
                return True
        return False


server = Server(watcher=CustomWatcher())
server.watch('docs/**', shell(sphinx, cwd='docs'),
             ignore=lambda s: '_build' in s)
# server.watch('docs/*.rst', shell(sphinx))
# server.watch('docs/*/*.rst', shell(sphinx))
server.watch('src/kaybee/**/*.html', shell(sphinx))
server.watch('src/kaybee/**.py', shell(sphinx))
server.watch('src/kaybee/**/index.js',
             shell(both, shell="/usr/local/bin/bash"),
             )
server.watch('src/kaybee/**/*.scss',
             shell(both, shell="/usr/local/bin/bash"),
             )
server.serve(root='docs/_build', live_css=False)
