import os

from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from webob.static import FileApp
from wsgiref.simple_server import make_server


ROOT_FILE_DIR = '/Users/kyle/Movies'

@view_config(route_name='test_stream')
def stream_video(request):
    filename = os.path.join(
        ROOT_FILE_DIR,
        'Wire,_The_-_3x5_-_Straight_And_True.English.TOPAZ.DVD.avi',
    )
    file_reader = FileApp(filename)
    return request.get_response(file_reader)

@view_config(route_name='stream_file')
def stream_file(request):
    filename = os.path.join(
        ROOT_FILE_DIR,
        request.matchdict['file_to_serve'],
    )
    print filename
    file_reader = FileApp(filename)
    return request.get_response(file_reader)

def make_app():
    config = Configurator()

    config.add_route('test_stream', '/test')
    config.add_route('stream_file', '/srv/{file_to_serve}')

    config.scan()

    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    return server

if __name__ == '__main__':
    make_app().serve_forever()
