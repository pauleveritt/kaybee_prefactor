from kaybee import kb


@kb.core('postrenderer')
class Injector:
    def __call__(self, html):
        return html + '\n<div id="postrenderer-flag">987</div>'
