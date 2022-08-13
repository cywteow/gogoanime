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
import requests
from resolveurl.lib import helpers
from resolveurl import common
from resolveurl.resolver import ResolveUrl, ResolverError
from resolveurl.plugins.__resolve_generic__ import ResolveGeneric



class GogoCdnResolver(ResolveGeneric):
    name = "GoGoCdn"
    domains = ['gogoanime.gg', 'gogoanime.video']
    pattern = r'(?://|\.)(gogoanime\..*)/([a-zA-Z0-9-]+)'

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        response = requests.get(web_url)

        if response.status_code == 200:
            result = response.json()
            if "sources" in result and len(result["sources"]) > 0:
                return result["sources"][0]["url"]
        raise ResolverError('Video cannot be located.')

    def get_url(self, host, media_id):
        return self._default_get_url(host, media_id, template='https://consumet-api.herokuapp.com/anime/gogoanime/watch/{media_id}')


    @classmethod
    def _is_enabled(cls):
        return True
