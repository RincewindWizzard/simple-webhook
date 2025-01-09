import multiprocessing

import gunicorn.app.base


from simple_webhook import config
from .server import app


class StandaloneApplication(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def main():
    options = {
        'bind': config.http.listen,
        'workers': 4,
        'certfile': config.ssl.cert,
        'keyfile': config.ssl.key,
    }
    StandaloneApplication(app, options).run()


# def main():
#     app.run(host='0.0.0.0', port=8000, ssl_context=(config.ssl.cert, config.ssl.key))


if __name__ == '__main__':
    main()
