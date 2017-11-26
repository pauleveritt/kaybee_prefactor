import os
from sphinx.application import Sphinx
from werkzeug.contrib.atom import AtomFeed

import kaybee
from kaybee import kb


@kb.event('html-collect-pages', 'feeds')
def generate_feeds(kb: kb, app: Sphinx):
    site = app.env.site
    feed_url = site.config.feed_url
    if feed_url:
        website_url = 'the website url'
        feed_title = 'Some Site'
        feed_filename = os.path.join(app.builder.outdir, 'atom.xml')
        feed_posts = site.filter_resources(
            sort_value='published',
            order=-1,
            limit=99
        )

        def os_path_join(path, *paths):

            return os.path.join(path, *paths).replace(os.path.sep, '/')

        feed = AtomFeed(feed_title,
                        title_type='text',
                        url=website_url,
                        feed_url=feed_url,
                        generator=(
                            'Kaybee', 'https://pypi.python.org/pypi/kaybee',
                            kaybee.__version__))

        for i, post in enumerate(feed_posts):
            post_url = os_path_join(
                website_url, app.builder.get_target_uri(post.docname))

            # content = post.to_html(pagename, fulltext=feed_fulltext)
            content = post.props.excerpt
            feed.add(post.title,
                     content=content,
                     title_type='text',
                     content_type='text',
                     # author=', '.join(a.name for a in post.author),
                     url=post_url,
                     id=post_url,
                     updated=post.props.published,
                     published=post.props.published
                     )

        with open(feed_filename, 'w') as out:
            feed_str = feed.to_string()
            try:
                out.write(feed_str.encode('utf-8'))
            except TypeError:
                out.write(feed_str)

    if 0:
        yield
