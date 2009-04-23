''''''

# Standard
# Related
# Local
from core.theme import CSSFile, JSFile, Block, Page, Region

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

blocks = [
    Block(template_file='block-blog_post.html', name='blog_posts',
          uri_match='/blog*',
          inner_regions=(
              Region(template_file='region-blog.html',
                     name='blog_poster_avatar', uri_match='/blog*'),
          )
          )
]

pages = [
    Page(template_file='page.html'),
    Page(uri_match='/bio', template_file='page-bio.html'),
]

regions = [
    Region(template_file='region-contact.html', name='content',
           uri_match='/content*'),
    Region(template_file='region-blog.html', name='blog',
           uri_match='/blog*'),
    Region(template_file='region-menu.html', name='menu'),
    Region(template_file='region-navigation.html', name='navigation'),
    Region(template_file='region-footer.html', name='footer'),
]
