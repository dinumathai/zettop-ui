from gevent.select import select
import flask
import json
import itertools
from datetime import datetime
import subprocess
import time
import math
import tempfile

app = flask.Flask(__name__)

# To test the streaming in UI
@app.route( '/stream/<configFileName>/' )
def stream(configFileName):
    def events():
        for i, c in enumerate(itertools.cycle('\|/-')):
            yield "data: %s %d\n\n" % (c, i)
            time.sleep(2)  # an artificial delay
    return flask.Response(events(), content_type='text/event-stream')

@app.route('/saveconf', methods=["POST"])
def saveconf():
    fileName =  str(math.floor( time.mktime(time.gmtime()) ))
    fullPath = tempfile.gettempdir() + '/' + fileName
    file = open(fullPath,"w")
    file.write(json.dumps(flask.request.json))
    file.close() 
    return flask.Response('{"tmpFile": "' + fileName +'"}', content_type='text/json')

def executesubprocess(command):
    proc = subprocess.Popen(
            [command],
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
            )
    # pass data until client disconnects, then terminate
    try:
        awaiting = [proc.stdout, proc.stderr]
        while awaiting:
            # wait for output on one or more pipes, or for proc to close a pipe
            ready, _, _ = select(awaiting, [], [])
            for pipe in ready:
                line = pipe.readline()
                if line:
                    yield "data: %s\n\n" % line.rstrip()
                else:
                    # EOF, pipe was closed by proc
                    awaiting.remove(pipe)
        if proc.poll() is None:
            proc.terminate()

    except GeneratorExit:
        # occurs when new output is yielded to a disconnected client
        proc.terminate()

    # wait for proc to finish and get return code
    proc.wait()

@app.route('/executecmd/<configFileName>/')
def executecmd(configFileName):
    # fullFilePath = tempfile.gettempdir() + '/' + configFileName
	# TODO: Move/rename fullFilePath to ignore the reties from UI - os.rename(fullFilePath, fullFilePath + ".json")
    command = "ping api.stg-status.ccp.t-mobile.com"
    return flask.Response(executesubprocess(command), content_type='text/event-stream')


@app.route('/<path:page_name>')
def render_static(page_name):
    if page_name == "":
        page_name = 'index.html'
    return flask.send_file(page_name)

@app.route('/')
def render_index():
    return flask.send_file('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
