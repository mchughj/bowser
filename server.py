
from flask import Flask, redirect, render_template, Response
from dotenv import dotenv_values
import os
import sys
import logging
import urllib.parse
from collections import defaultdict

from os.path import dirname, basename, isfile, join
import glob
import threading
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

app = Flask(__name__)

logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO, 
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

scriptDirectory = os.path.dirname(os.path.realpath(__file__))
envFilename = os.path.join(scriptDirectory, ".env")

config = {
    **dotenv_values(envFilename),
}
try:
    serverPort = config["ServerPort"]
    redirectionDirectory = config["RedirectionDirectory"]
except KeyError:
    logging.info(f"You must create a .env file ({envFilename}) in the server directory containing the keys described in this file")
    sys.exit(1)

redirections = defaultdict(lambda: None)
fullRedirectionsDirectory = join(dirname(__file__), redirectionDirectory)

def genAllRedirections():
    global redirections

    redirections = defaultdict(lambda: None)

    modules = glob.glob(join(fullRedirectionsDirectory, "*.py"))
    redirectionNames = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]

    logging.info( f"Found all modules and redirectionNames; modules: {modules}, redirectionNames: {redirectionNames}")
    for f in redirectionNames:
        # Bring in the redirectory file and then construct an instance of a
        # class that, by my convention, must be the same as the name of the
        # file.
        try:
            exec(f"import {redirectionDirectory}.{f}")
            x = eval(f"{redirectionDirectory}.{f}.{f}")
            redirections[x.shortName()] = x
        except:
            logging.error(f"Unable to read in redirections due to an error; f: {f}")

def find(redirectionShortForm):
    return redirections[redirectionShortForm]

def dispatchBare(redirectionElement):
    url = redirectionElement.bare()
    logging.info( f"dispatchBare done generated redirect; url: {url}")
    return redirect(url, code=302)

def dispatchArged(redirectionElement, components):
    result = redirectionElement.arged(components)
    if len(result) == 1:
        return redirect(result[0], code=302)
    else:
        url = result[0]
        args = urllib.parse.quote(' '.join(components[0:]))
        fullUrl = f"{url}{args}"
        logging.info( f"dispatchArged done generated redirect; components: {components}, url: {url}, args: {args}, fullUrl: {fullUrl}")
        return redirect(fullUrl, code=302)

@app.route('/install/')
def installRequest():
    return render_template("install.html")

@app.route('/help')
def showHelp():
    return render_template("help.html", r=list(filter(lambda x: x != None, redirections.values())))

@app.route('/<p>')
def redirectRequest(p):
    logging.info(f"Received a redirect request; raw: {p}")

    p = urllib.parse.unquote_plus(p)
    components = p.split(" ")

    logging.info(f"Going to look for redirection element; components[0]: {components[0]}")
    redirectionElement = find(components[0])

    if redirectionElement == None:
        return render_template("help.html", errorString=f"Unable to find shortcut '{components[0]}'", r=list(filter(lambda x: x != None, redirections.values())))
    elif len(components) == 1:
        return dispatchBare(redirectionElement)
    else:
        return dispatchArged(redirectionElement, components[1:])


# Simple handler that will ensure that our redirections are up to date
# with respect to the directory.  I cannot simply rely on Flask's 
# mechanism to watch for changes to python files as this doesn't handle
# when new redirectors are added to the underlying file system.
class RedirectionsWatchHandler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        # I only care about newly created files as the flask system will
        # automatically reload for existing files. 
        if event.event_type == 'created' or event.event_type == 'deleted':
            logging.info( f"detected change to redirections directory; event: {event}")
            genAllRedirections()


if __name__ == '__main__':
    # Create the initial list of all redirections
    genAllRedirections()

    # Setup a mechanism to watch for new ones or remove ones that have been
    # removed from the file system.
    redirectionsWatchHandler = RedirectionsWatchHandler()
    observer = Observer()
    observer.schedule(redirectionsWatchHandler, fullRedirectionsDirectory, recursive=True)
    observer.start()

    # Begin the flask application
    app.run(debug=True, host="0.0.0.0", port=serverPort)
