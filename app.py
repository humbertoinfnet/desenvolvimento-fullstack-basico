#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.external_interfaces.flask_server.app import create_app
from src.external_interfaces.database.config.config import init_database

if __name__ == '__main__':
    init_database()
    app = create_app()
    app.run(debug=True)
