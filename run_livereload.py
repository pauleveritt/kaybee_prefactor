from livereload import Server, shell

cmd = ".venv/bin/python3 .venv/bin/sphinx-build -E -b html docs docs/_build"

server = Server()
delay = 1
server.watch('docs/*.rst', shell(cmd), delay=delay)
server.watch('docs/*/*.rst', shell(cmd), delay=delay)
server.watch('src/kaybee/templates/*.html', shell(cmd), delay=delay)
server.serve(root='docs/_build')

