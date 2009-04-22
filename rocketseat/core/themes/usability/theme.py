''''''

# Standard
# Related
# Local
from core.theme import CSSFile, JSFile

js_files = (
)

css_files = (
    CSSFile('css/blueprint/screen.css'),
    CSSFile('css/blueprint/print.css', media='print'),
    CSSFile('css/blueprint/ie.css', ie_only=True),
    CSSFile('css/layout.css'),
    CSSFile('css/style.css'),
)

humane_name = 'Usability'

theme_graphic = None

blocks = (
    Block(name='blog_posts', uri_match='/blog*', template='block.html',
          inner_regions=(
              Region('blog_poster_avatar', url_match='/blog*', 
                     template='region-blog.html'),
          )
          )
)

pages = (
    Page(template='page.html'),
    Page(uri_match='/bio', template='page-bio.html'),
)

regions = (
    Region(name='content', url_match='/content*',
           template='region-contact.html'),
    Region(name='blog', url_match='/blog*', template='region-blog.html'),
    Region(name='menu', template='region-menu.html'),
    Region(name='navigation', template='region-menu.html'),
    Region(name='footer', template='region-menu.html'),
)
