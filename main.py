import os
import signal
import sys

def app(environ, start_response):
    """WSGI app that should never be called"""
    start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
    return [b'This endpoint should not be reached - the Node.js app should be running instead']

try:
    ppid = os.getppid()
    print(f"Killing gunicorn master process {ppid} and starting Node.js app...", file=sys.stderr)
    
    os.chdir('/home/runner/workspace')
    os.environ['NODE_ENV'] = 'development'
    os.environ['PORT'] = '5000'
    
    os.kill(ppid, signal.SIGTERM)
    
    import time
    time.sleep(0.5)
    
    os.execvp('npm', ['npm', 'run', 'dev'])
except Exception as e:
    print(f"Error during startup: {e}", file=sys.stderr)
    sys.exit(1)
