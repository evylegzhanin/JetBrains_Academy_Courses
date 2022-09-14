from flask import Flask
import sys

app = Flask('weather_app')


@app.route('/')
def hello_world():
    return 'Hello, world!'


# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()



