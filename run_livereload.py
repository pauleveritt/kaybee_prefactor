from livereload import Server, shell

sphinx = ".venv/bin/python3 .venv/bin/sphinx-build -E -b html docs docs/_build"
dist = "/usr/local/bin/npm run dist"
both = dist + '; ' + sphinx

server = Server()
server.watch('docs/*.rst', shell(sphinx))
server.watch('docs/*/*.rst', shell(sphinx))
server.watch('src/kaybee/templates/*.html', shell(sphinx))
server.watch('src/kaybee/index.js',
             shell(both, shell="/usr/local/bin/bash"),
             )
server.watch('src/kaybee/scss/*.scss',
             shell(both, shell="/usr/local/bin/bash"),
             )
server.serve(root='docs/_build', live_css=False)
