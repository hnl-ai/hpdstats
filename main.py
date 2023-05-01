# -*- coding: utf-8 -*-
"""Create an application instance."""
from app.app import create_app

app = create_app()

if __name__ == "__main__":
    # https://stackoverflow.com/a/43606759/6482196
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()
