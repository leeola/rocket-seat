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

regions = (
    'content',
    'menu',
    'navigation',
    'footer'
)

page_templates = (
    'page.html',
)

region_templates = (
)

block_templates = (
)
