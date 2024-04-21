#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.external_interfaces.flask_server.app import create_app
from src.external_interfaces.flask_server.register_route import register_route
from src.log.log import format_logger
from src.external_interfaces.database.config.config import init_database, insert_elements



if __name__ == '__main__':
    
    app = create_app()
    register_route(app)
    format_logger()
    app.run(debug=False)
    init_database()
    insert_elements()
