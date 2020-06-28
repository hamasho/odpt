import http.server
import socketserver

PORT = 3001

Handler = http.server.SimpleHTTPRequestHandler

Handler.extensions_map = {
    '.manifest': 'text/cache-manifest',
    '.html': 'text/html',
    '.png': 'image/png',
    '.jpg': 'image/jpg',
    '.svg': 'image/svg+xml',
    '.css': 'text/css',
    '.js': 'application/x-javascript',
    '.czml': 'text/event-stream',
    '': 'application/octet-stream', # Default
}

httpd = socketserver.TCPServer(("", PORT), Handler)

print("serving at port", PORT)
httpd.serve_forever()
