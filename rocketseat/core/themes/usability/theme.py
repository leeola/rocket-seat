''''''

# Standard
# Related
# Local
from core.theme import CSSFile, JSFile
from core.theme import BaseTemplateOverride as Base
from core.theme import BlockTemplateOverride as Block
from core.theme import PageTemplateOverride as Page
from core.theme import RegionTemplateOverride as Region

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

bases = [
]

blocks = [
]

pages = [
]

regions = [
]

# This is mostly test code. For now, i am letting the core themes be used.
#blocks = [
    #BlockHandler(
        #local_template_file='block-blog_post.html', name='blog_posts',
        #uri_match='/blog*',
        #inner_regions=[
            #RegionHandler(template_file='region-blog.html',
                          #name='blog_poster_avatar',
                          #uri_match='/blog*'),
        #]
    #),
#]

#pages = [
    #PageHandler(template_file='page.html'),
    #PageHandler(uri_match='/bio', template_file='page-bio.html'),
#]

#regions = [
    #RegionHandler(
        #local_template_file='region-content.html', name='content',
        #uri_match='/content*'),
    #RegionHandler(
        #local_template_file='region-blog.html', name='blog',
        #uri_match='/blog*'),
    #RegionHandler(
        #local_template_file='region-menu.html', name='menu'),
    #RegionHandler(
        #local_template_file='region-navigation.html', name='navigation'),
    #RegionHandler(
        #local_template_file='region-footer.html', name='footer'),
#]
