sample_site = dict(
    sphinx_config={},
    title='My Kaybee Site',
    nav_menu=[
        dict(title='Home', url=''),
        dict(title='Blog', url='blog')
    ],
    items=[
        dict(
            resource=dict(
                title='Resource Page 1',
                subtitle='RP1 is subtitled',
                resource_type='Page',
                section='Home'
            ),
            body='<p>This is the body</p>'
        ),
        dict(
            resource=dict(
                title='Another Page',
                subtitle='Blog away',
                resource_type='Page',
                section='Blog'
            ),
            body='<p>Goes in the blog</p>'
        )
    ]
)
