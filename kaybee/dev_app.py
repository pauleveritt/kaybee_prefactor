"""
Development server for hacking kaybee

This is a small Flask server which speeds up development of the 
theme. It is not bundled into the distribution. Its job is to 
replace the edit, run sphinx, reload browser cycle.

It provides:

- An instance of the context for use in the templates

- Some representative sample data

- A livereload-capable server

"""
from flask import Flask
from livereload import Server
from markupsafe import Markup

from kaybee.rms import CMS
from kaybee.sample_data import sample_site
from kaybee.resources import setup

app = Flask(
    __name__,
    static_url_path='/static',
    static_folder='./static',
    template_folder='./templates'
)
app.debug = True
cms = CMS(sample_site['title'],config={})


@app.route("/")
def index():
    resource = sample_site['items'][0]['resource']
    body = Markup(sample_site['items'][0]['body'])
    this_page = cms.render(
        body,
        resource
    )
    return this_page()


@app.route("/blog")
def blog():
    resource = sample_site['items'][1]['resource']
    body = Markup(sample_site['items'][1]['body'])
    this_page = cms.render(
        body,
        resource
    )
    return this_page()


if __name__ == "__main__":
    setup(sample_site['sphinx_config'])
    server = Server(app.wsgi_app)
    server.serve()
