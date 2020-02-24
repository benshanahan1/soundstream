from gevent import monkey
monkey.patch_all()  # monkey patch for gevent
from soundstream.app import create_app, run_server  # noqa: E401


def main():
    app = create_app()
    run_server(app)


if __name__ == '__main__':
    main()
