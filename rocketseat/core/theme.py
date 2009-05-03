''''''


# Standard
import os.path
import re
# Related
import mako.template
# Local
import core.error


def find_theme_abs_path(theme_script_name):
    '''Find the themes absolute path, as found by os.path.abspath()

    @param theme_script_name: The script name of the theme.
    '''
    if os.path.exists('../user/themes/%s' % theme_script_name):
        return os.path.abspath('../themes/%s' % theme_script_name)
    elif os.path.exists('themes/%s' % theme_script_name):
        return os.path.abspath('themes/%s' % theme_script_name)
    else:
        raise core.error.ThemeNotFoundError(theme_script_name)

def find_theme_rel_path(theme_script_name):
    '''Find the themes relative path

    @param theme_script_name: The script name of the theme.
    '''
    if os.path.exists('../user/themes/%s' % theme_script_name):
        return '../themes/%s' % theme_script_name
    elif os.path.exists('themes/%s' % theme_script_name):
        return 'themes/%s' % theme_script_name
    else:
        raise core.error.ThemeNotFoundError(theme_script_name)

class CSSFile(object):
    '''An object L{the theme class <Theme>} can interact with more easily.
    '''


    def __init__(self, file_location, ie_only=False,
                 media='screen, projection'):
        '''
        '''
        self.file_location = file_location
        self.ie_only = ie_only
        self.media = media

    def render_html(self, base_theme_static_uri=None):
        '''
        @param base_theme_static_uri: If supplied, the uri for the css file
        will have this inserted before it.
        '''
        if base_theme_static_uri is not None:
            if not self.ie_only:
                return '''<link rel="stylesheet"
                href="%s/%s" type="text/css"
                media="%s" />''' % (base_theme_static_uri,
                                    self.file_location,
                                    self.media)
            else:
                return '''<!--[if IE]><link rel="stylesheet"
                href="%s/%s" type="text/css"
                media="%s" /><![endif]-->''' % (base_theme_static_uri,
                                                self.file_location,
                                                self.media)

class JSFile(object):
    '''
    '''

    def __init__(self):
        '''
        '''
        pass

class Theme(object):
    '''A class representing the instance of the loaded theme.'''


    def __init__(self, theme_script_name):
        '''
        '''
        self.theme_script_name = theme_script_name
        #self.core_event_controller = core_event_controller

        if os.path.exists('../user/themes/%s' % theme_script_name):
            self.user_theme = True
            self.theme_rel_path = '../user/themes/%s' % theme_script_name
            self.theme_py_path = 'user.themes.%s' % theme_script_name
            self.theme_static_uri = '/static/themes/user/%s' % theme_script_name
        elif os.path.exists('themes/%s' % theme_script_name):
            self.user_theme = False
            self.theme_rel_path = 'themes/%s' % theme_script_name
            self.theme_py_path = 'core.themes.%s' % theme_script_name
            self.theme_static_uri = '/static/themes/core/%s' % theme_script_name
        else:
            raise core.error.ThemeNotFoundError(theme_script_name)

        # Import the user theme module, and grab the settings from it.
        theme_module = __import__('%s.theme' % self.theme_py_path,
                                  fromlist=['a'])

        #: A list of L{css file <CSSFile>} like objects.
        self.css_files = list(theme_module.css_files)
        #: A list of L{js file <JSFile>} like objects.
        self.js_files = list(theme_module.js_files)

        self._rendered_css_html = None
        self._rendered_js_html = None
        self._rendered_blocks_html = ''

        ## Trigger the event, so other plugins can add to the css.
        #plugin_css = event_controller.call_listeners(
            #'core_p', 'add_plugin_css')

        # To make sure atleast 1 handler works (and thus, avoiding a key error)
        # we append the generic, base, block, region, and page handlers to 
        # theme module lists.
        theme_module.bases.append(
            BaseTemplateOverride(template_text=(
                '<?xml version="1.0" encoding="UTF-8"?>'
                '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"'
                '    "DTD/xhtml1-strict.dtd">'
                '<html xmlns="http://www.w3.org/1999/xhtml"'
                '    xml:lang="en" lang="en">'
                '<head>'
                '    <title>${page_title} - ${site_name}</title>'
                '    ${site_js}'
                '    ${site_css}'
                '</head>'
                '<body>'
                '    ${base_body}'
                '</body>'
                '</html>'
            ))
        )
        theme_module.blocks.append(
            BlockTemplateOverride(template_text=(
                '<div class="${block_css_classes}">'
                '    <h3>${block_title}</h3>'
                '    <div>'
                '        ${block_content}'
                '    </div>'
                '</div>'
            ))
        )
        theme_module.pages.append(
            PageTemplateOverride(template_text=(
                '<div class="container grid">'
                '    ${region_menu}'
                '    <div class="">'
                '    </div>'
                '</div>'
            ))
        )
        theme_module.regions.append(
            RegionTemplateOverride(template_text=(
                '<div class="${region_css_classes}">'
                '    ${blocks}'
                '</div>'
            ))
        )

        # For the sake of speed on cached loads, we will sort the overrides
        # on a few criteria now, so that later consecutive cached page loads
        # can benefit from this sorting. What we do is group types of overrides
        # based on what information they have to match the page load, and the
        # data loading.
        # 
        # The following is the possible groups we will sort all the overrides
        # into:
        # - Overrides with only names (Direct Matches by Name)
        # - Overrides with only uri (Requires regex matching on every item,
        #   costly.)
        # - An override with no name or uri (Only the first instance of this
        #   will match, seeing as the first occurance will _always_ match, the
        #   following ones can be ignore.)

        # The keys are the uri regex string.
        base_overrides_by_uri = {}
        # The first occurance of a "match all" override. All others ignored.
        base_override_matching_all = None
        for base in theme_module.bases:
            if base.uri_match is not None:
                base_overrides_by_uri[base.uri_match] = base
            elif base_override_matching_all is None:
                base_override_matching_all = base

        self.base_overrides_by_uri = base_overrides_by_uri
        self.base_override_matching_all = base_override_matching_all

        # The keys are the block names
        block_overrides_by_name = {}
        # The keys are the block override's uri regex string
        block_overrides_by_uri = {}
        # The first occurance of a "match all" override. All others are ignored.
        block_override_matching_all = None

        for block_override in theme_module.blocks:
            if block_override.name is not None:
                block_overrides_by_name[block_override.name] = block_override

            elif block_override.uri_match is not None:
                block_overrides_by_uri[
                    block_override.uri_match] = block_override

            elif block_override_matching_all is None:
                # If there is no match all block override, assign it now.
                block_override_matching_all = block
            # If the code path makes it here, it is a match all, but match
            # all has already been assigned, so ignore it.
        # Now assign the built groups of block overrides into self.
        self.block_overrides_by_name = block_overrides_by_name
        self.block_overrides_by_uri = block_overrides_by_uri
        self.block_override_matching_all = block_override_matching_all

        # The keys are the uri regex string.
        page_overrides_by_uri = {}
        # The first occurance of a "match all" override. All others ignored.
        page_override_matching_all = None
        for page in theme_module.pages:
            if page.uri_match is not None:
                page_overrides_by_uri[page.uri_match] = page

            elif page_override_matching_all is None:
                page_override_matching_all = page

        self.page_overrides_by_uri = page_overrides_by_uri
        self.page_override_matching_all = page_override_matching_all

        # The keys are the region names
        region_overrides_by_name = {}
        # The keys are the region override's uri regex string
        region_overrides_by_uri = {}
        # The first occurance of a "match all" override. All others are ignored.
        region_override_matching_all = None

        for region_override in theme_module.regions:
            if region_override.name is not None:
                region_overrides_by_name[region.name] = region_override

            elif region.uri_match is not None:
                region_overrides_by_uri[block.uri_match] = region_override

            elif region_override_matching_all is None:
                region_override_matching_all = region_override

        self.region_overrides_by_name = region_overrides_by_name
        self.region_overrides_by_uri = region_overrides_by_uri
        self.region_override_matching_all = region_override_matching_all


    def render(self):
        '''Render the entire page, through a cascading series of calls to
        this class and render listeners.
        '''

        # Make some fake data here, and pretend this came from plugins for now.
        fakedata = {
            'spam_block_one':{
                'block_title':'Spam Block One',
                'block_content':'Look, I\'m spam!',
                'spam_index':0,
                },
            'spam_block_two':{
                'block_title':'Spam Block Two',
                'block_content':'Look, I\'m spam!',
                'spam_index':1,
                },
        }

        # The db knows which block goes in what region. Here we fake it
        block_region_assignments = {
            'spam_block_one':'content',
            'spam_block_two':'footer',
        }

        # Store each region's rendered results here so it can then be fed to
        # the page template.
        rendered_region_contents = {}

        # Store these locally for speed.
        block_overrides_by_name = self.block_overrides_by_name
        block_overrides_by_uri = self.block_overrides_by_uri

        for block_name, region_name in block_region_assignments.items():
            # Loop through each block and its assigned region.

            if not rendered_region_contents.has_key(region_name):
                # If the rendered_region_contents doesn't have the region_name
                # key, we add a default value to it here. This way, later when
                # it is added to, we don't have to check it there. Which will
                # be checked more often than here.
                
                rendered_region_contents[region_name] = ''
            
            if block_overrides_by_name.has_key(block_name):
                # Check if this region has a name-only match

                for block_matched_by_name in block_overrides_by_name[
                    block_name]:
                    # Loop through all the overrides matching that name

                    if block_matched_by_name.uri_match is None:
                        # if the block has no uri_match, use it.

                        block_override = block_matched_by_name
                        break
                    elif (re.compile(block_matched_by_name.uri_match).
                          match(ahhhh_im_not_real) is not None):
                        # If there is a url_match, and it matches the current
                        # url, use it.

                        block_override = block_matched_by_name
                        break
            else:
                # If we get here, there is no name matching the override, but
                # there is a uri 

                for block_override_by_uri in block_overrides_by_uri:
                    # As slow as it is, here we have to loop through all of the
                    # uri_match strings to find the first one that matches.

                    # Create a regex pattern from the uri_match string.
                    # if there isn't one.. somehow... things are bad.
                    regex_pattern = re.compile(block_override_by_uri.uri_match)

                    if regex_pattern.match(ahhhh_im_not_real) is not None:
                        block_override = block_override_by_uri
                        break
                else:
                    # If we loop through all the uri overrides and no match
                    # has been found (if one is found, the loop is broken), we
                    # then assign the block_override to the match-alloverride.
                    block_override = self.block_override_matching_all

            # Create the block mako template
            if block_override.template_file is not None:
                block_template = mako.template.Template(
                    filename=block_override.template_file)
            else:
                block_template = mako.template.Template(
                    text=block_override.template_file)

            # render the block template by exploding the dict into the
            # function.
            rendered_region_contents[region_name] += block_template.render(
                **fakedata[block_name])

        template = mako.template.Template(
            filename='%s/base.html' % self.theme_rel_path)
        return template.render(
            base_body='Nothing',
            page_title='Rocket Seat CMS',
            site_name='Dont crash me',
            site_js='',
            site_css=self.rendered_css_html,
        )

    def add_block_content(self):
        '''
        '''
        pass

    def render_css_html(self):
        '''Render the html for the css files stored in this theme.

        @returns: A string of the rendered css links, eg:
        	<link rel="stylesheet" 
                href="/static/themes/core/usability/css/style.css"
                type="text/css" media="screen, projection" />

        '''
        # Store it locally for speed.
        theme_static_uri = self.theme_static_uri

        def render_css(css_file):
            return css_file.render_html(base_theme_static_uri=theme_static_uri)

        rendered_css_list = map(render_css, self.css_files)
        return ''.join(rendered_css_list)

    def render_js_html(self):
        '''
        '''
        pass

    def _get_rendered_css_html(self):
        '''Get self._rendered_css_html.
        '''
        if self._rendered_css_html is None:
            self._rendered_css_html = self.render_css_html()
        return self._rendered_css_html

    rendered_css_html = property(_get_rendered_css_html)

    def _get_rendered_js_html(self):
        '''Get self._rendered_js_html.
        '''
        if self._rendered_js_html is None:
            self._rendered_js_html = self.render_js_html()
        return self._rendered_js_html

    rendered_js_html = property(_get_rendered_js_html)


class CoreTemplateOverride(object):
    '''The base class for theme core template overrides such as 
    L{pages <PageTemplateOverride>}, L{regions <RegionTemplateOverride>}, and 
    L{blocks <BlockTemplateOverride>}.
    '''

    def __init__(self, local_template_file=None, rel_template_file=None,
                 template_text=None, uri_match=None):
        '''
        @param local_template_file: The filename of a template file, absolute
        from the active theme directory.
        Eg:
         - block-user_login.html
         - admin/block-login.html
         - forum/blocks/new_post.html
        This is basically only used by the theme developers, for plugin
        template overrides, see the rel_template_file param.
        @type local_template_file: A string path.

        @param rel_template_file: The filename of the template file, relative
        to rocketseat's core dir.
        Eg:
         - ../user/plugins/some_plugin/theme/block.html
         - plugins/admin/theme/block-admin_login.html
        This is to be used by plugins mainly, as it allows them to give a path
        to any template file found in rocketseat.

        @param template_text: If supplied, the handler will render from this
        and _not_ the template_file.

        @param uri_match: If the uri does not match the regex supplied here,
        the block will not be shown.
        @type uri_match: A regex string or None.
        '''

        if (local_template_file is None and rel_template_file is None
            and template_text is None):
            raise core.error.MissingTemplateInOverride()

        self.local_template_file = local_template_file
        self.rel_template_file = rel_template_file
        self.template_text = template_text
        self.uri_match = uri_match

    def get_template(self):
        '''Return the mako template object for this 
        '''
        # If template text is defined, use that.
        if self.template_text is not None:
            return mako.template.Template(
                text=self.template_text)

        # If we make it here, no template text was defined.. and there
        # _better_ be a template file... or all hell breaks loose.
        return mako.template.Template(
            text=self.template_text)

class BaseTemplateOverride(CoreTemplateOverride):
    '''
    '''

    def __init__(self, local_template_file=None, rel_template_file=None,
                 template_text=None, uri_match=None):
        '''
        '''
        super(BaseTemplateOverride, self).__init__(
            local_template_file, rel_template_file, template_text, uri_match)

class BlockTemplateOverride(CoreTemplateOverride):
    '''This object allows the user to define a block template, specific uri
    requirements, and any regions that exist inside of it.
    '''

    def __init__(self, local_template_file=None, rel_template_file=None,
                 template_text=None, name=None, uri_match=None,
                 inner_regions=None):
        '''
        @param name: The name of the block. When plugins submit content, they
        do so planning that it will be put into a block with a specific name.
        So as you might guess, naming this correctly is very important.
        @type name: A string or None.

        @param inner_regions: If defined, the block will render the region(s)
        inside of it, along with any blocks the region(s) may contain
        @type inner_regions: A list or tuple or L{regions <Region>}.

        @important: If both name and uri_match are None, all blocks that reach
        this instance will use it because the name matches (U{None is
        essentially a wildcard}), and the uri matches (U{Again, None is
        a wildcard}). This is useful if you want all blocks, no matter name or
        uri, to use a specific template.

        Usually you put this "wildcard block" at the end of the blocks list, so
        that you can match any blocks you need, and if none of those match,
        your wildcard is chosen.
        '''
        super(BlockTemplateOverride, self).__init__(
            local_template_file, rel_template_file, template_text, uri_match)

        self.name = name
        if inner_regions is not None:
            self.inner_regions = inner_regions

class PageTemplateOverride(CoreTemplateOverride):
    '''
    '''

    def __init__(self, local_template_file=None, rel_template_file=None,
                 template_text=None, uri_match=None):
        '''
        '''
        super(PageTemplateOverride, self).__init__(
            local_template_file, rel_template_file, uri_match)

class RegionTemplateOverride(CoreTemplateOverride):
    '''
    '''

    def __init__(self, local_template_file=None, rel_template_file=None,
                 template_text=None, name=None, uri_match=None):
        '''
        '''
        super(RegionTemplateOverride, self).__init__(
            local_template_file, rel_template_file, template_text, uri_match)

        self.name = name

