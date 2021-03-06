# this is the main program of the corpus builder tool
# it can be launched standalone, using a Flask server started here and calling localhost:5000/corpus
# or from the main tool with its Flask server, selecting the corresponding option

# argument '-d' makes button labels in the interface to show calls (routes) associated in the server,
# to be easier to understand the flow among interface and python server modules
 
# it depends on px_DB_Manager and px_aux modules of the main tool, as well as the 

import sys
from smart_open import open as SOpen

# this program has been launched in the Plethora/buildCorpus folder
# this is to search px_DB_Manager and px_aux in the Plethora folder
# such modules are not needed here, but in routesCorpus and routesCorpus2 modules loaded next
sys.path.append('../')

# functions to be executed when Flask requests are received 
from routesCorpus import getWikicatsFromText as _getWikicatsFromText
from routesCorpus2 import buildCorpus2 as _buildCorpus2
from aux import INITIAL_TEXT as _INITIAL_TEXT
import aux

# load the initial text shown at the beginning of the interface
initialTextFile = SOpen(_INITIAL_TEXT, "r")
initialText = initialTextFile.read()

pDebug = False
	
# the following is only executed if this is the main program, that is, if we launch the corpus tool directly from the 'buildCorpus' folder
# not executed if we launch the corpus tool from the main tool, as the 'app' object is already available from the main tool
if __name__ == '__main__':
	import os
	
	# Flask is a module to launch a web server. It permits to map a function for each request template 
	from flask import Flask, render_template, request, flash, json, jsonify, redirect, url_for, send_from_directory
	
	# templates dir is shared with the main tool because it is possible for this tool to be called from the main one
	template_dir = os.path.abspath('../templates')
	# Create the Flask app to manage the HTTP request  
	app = Flask(__name__, template_folder=template_dir)

	# only to serve style.js from the js folder of the main tool (also done in the main tool, so only necessary if standalone)
	@app.route('/css/<path:path>')
	def send_js(path):
		return send_from_directory('../css', path)
	
	arguments = len(sys.argv) - 1
	if arguments == 1:
		if sys.argv[1] == "-d":   # argument '-d' prints button labels with routes associated
			pDebug = True
		if sys.argv[1] == "-s":   # argument '-s' forces stop after every phase
			aux.PSTOP = True
			print("Force stop activated!!!")

# Flask routes binding for interface requests (not done in the main tool, so always necessary)
app.add_url_rule("/getWikicatsFromText", "getWikicatsFromText", _getWikicatsFromText, methods=["POST"])  # to send a text and request the wikicats in it
app.add_url_rule("/buildCorpus2", "buildCorpus2", _buildCorpus2, methods=["POST"])   # to send some wikicats and request to build the corpus

# this is the main entry point of the corpus builder tool (not done in the main tool, so always necessary)
@app.route('/corpus',  methods=["GET", "POST"])
def hello_world():
	return render_template('./template_corpus.html', parDefaultText=initialText, parDebug=pDebug) # parDebug=True prints button labels with routes associated


# start web server listening port 5000 by default if we have launched the corpus tool standalone

# the following is only executed if this is the main program, that is, if we launch the corpus tool directly from the 'buildCorpus' folder
# not executed if we launch the corpus tool from the main tool, as the 'app' object is already available from the main tool
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5060, threaded=True)
