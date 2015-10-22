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


"""Minimal Flask application example for development.

Make sure that ``elasticsearch`` server is running:

.. code-block:: console

   $ elasticsearch
   ... version[2.0.0] ...

Run example development server:

.. code-block:: console

   $ cd examples
   $ echo '{"title": "Test", "control_number": 1}' > record_1.json
   $ flask --app app index put records record -i 1 -b record_1.json
   $ flask --app app run

Try to perform some queries from browser:

.. code-block:: console

   $ open http://localhost:5000/?q=title:Test

"""

from __future__ import absolute_import, print_function

from flask import Flask, jsonify, request
from flask_cli import FlaskCLI

from invenio_search import InvenioSearch, current_search_client

# Create Flask application
app = Flask(__name__)
FlaskCLI(app)
InvenioSearch(app)


@app.route('/', methods=['GET', 'POST'])
@app.route('/<index_name>', methods=['GET', 'POST'])
def index(index_name='records'):
    query = request.values.get('q', '')
    response = current_search_client.search(
        index=index_name,
        doc_type='record',
        q=query,
    )
    return jsonify(**response)
