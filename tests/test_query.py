# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.


"""Module tests."""

from __future__ import absolute_import, print_function

from invenio_search import InvenioSearch
from invenio_search.api import Query as Q


def test_empty_query(app):
    """Test building an empty query."""
    InvenioSearch(app)
    app.config['SEARCH_QUERY_PARSER'] = None

    with app.app_context():
        q = Q()
        assert q.body['query'] == ''

        q = Q('')
        assert q.body['query'] == ''

        q = Q()[10]
        assert q.body['from'] == 10
        assert q.body['size'] == 1

        q = q[10:20]
        assert q.body['from'] == 10
        assert q.body['size'] == 10

        q = q.sort('field1')
        assert q.body['sort'][0] == {'field1': {'order': 'asc'}}

        q = q.sort()
        assert 'sort' not in q.body

        q = q.sort('-field1')
        assert q.body['sort'][0] == {'field1': {'order': 'desc'}}

        q = q.sort('field2', {'field3': {'order': 'asc'}})
        assert q.body['sort'][0] == {'field1': {'order': 'desc'}}
        assert q.body['sort'][1] == {'field2': {'order': 'asc'}}
        assert q.body['sort'][2] == {'field3': {'order': 'asc'}}
        q.sort()
