#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.external_interfaces.flask_server.app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
