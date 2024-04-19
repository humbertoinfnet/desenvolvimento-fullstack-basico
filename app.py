#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.external_interfaces.flask_server.app import create_app
from src.external_interfaces.flask_server.register_route import register_route
from src.log.log import format_logger
from src.external_interfaces.database.config.config import init_database, insert_elements



if __name__ == '__main__':
    
    init_database()
    insert_elements()
    app = create_app()
    register_route(app)
    app.run(debug=False)
    format_logger()
  
