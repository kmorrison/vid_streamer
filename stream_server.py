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
    os.stat(filename)
    file_reader = FileApp(filename)
    return request.get_response(file_reader)

test_body = """
<html>
<head>
</head>

<body>
<video controls>
<source src="/srv/The.Walking.Dead.S04E05.HDTV.x264-2HD.mp4">
</video>
</body>
</html>
"""

@view_config(route_name='test_display')
def test_display(request):
    return Response(test_body)

def make_app():
    config = Configurator()

    config.add_route('test_stream', '/test')
    config.add_route('stream_file', '/srv/{file_to_serve}')
    config.add_route('test_display', '/test_display')

    config.scan()

    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    return server

if __name__ == '__main__':
    make_app().serve_forever()
