"""
    Plugin for ResolveUrl
    Copyright (C) 2020 cywteow

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import re
from resolveurl.plugins.lib import helpers
from resolveurl import common
from resolveurl.resolver import ResolveUrl, ResolverError
from resolveurl.plugins.__resolve_generic__ import ResolveGeneric


class SteamaniResolver(ResolveGeneric):
    name = "streamani"
    domains = ['streamani.net']
    pattern = r'(?://|\.)(streamani\.net)/(?:streaming)\.php\?id=([a-zA-Z0-9]+)'

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        headers = {'User-Agent': common.FF_USER_AGENT,
                   'Referer': 'https://{0}/'.format(host)}
        r = self.net.http_GET(web_url, headers=headers)
        src = re.search(r'href="(https://storage.googleapis.com/(.*))" download>Download', r.content)
        if src:
            return src.group(1)
        raise ResolverError('Video cannot be located.')

    def get_url(self, host, media_id):
        return self._default_get_url(host, media_id, template='https://{host}/download?id={media_id}')


    @classmethod
    def _is_enabled(cls):
        return True
