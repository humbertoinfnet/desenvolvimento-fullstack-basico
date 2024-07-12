#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dotenv import load_dotenv
from src.external_interfaces.flask_server.app import create_app
from src.external_interfaces.flask_server.register_route import register_route
from src.log.log import format_logger
from src.external_interfaces.database.config.config import init_database, insert_elements



if __name__ == '__main__':
    load_dotenv()
    app = create_app()
    register_route(app)
    format_logger()
    init_database()
    insert_elements()
    app.run(debug=False, host='0.0.0.0', port=5000)
