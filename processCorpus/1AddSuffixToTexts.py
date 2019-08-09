#!/Library/Frameworks/Python.framework/Versions/Current/bin/python3

# This script is intended to process one or several files (parameter) to detect pairs "NAME romannumber" (event) and proceed to the following changes
# 1. change future ocurrences of NAME without romannumber to "NAME romannumber" (where 'romannumber' is the last event detected for NAME)   
# 2. change any ocurrence of NAME previous to a unique event forn NAME (NAME happens only once with a romannumber) to "NAME romannumber"  (being romannumber the one of the future event)
#
# input: a .txt file or folder received as parameter
#			if folder, folder/files_txt must exist, and all '.txt' files in folder/files_txt will be processed
# outputs:	several files will be created in folder/files_s_p_w
#			a file with the original name and the suffix '.s', for every processed file
#			a .s.html' file with the changes in green, for every processed file
#		In case of the '-g folder' modifier a new file 'folder/folder.s' will be created aggregating all the created '.s' files in folder/files_s_p_w.

# every file is read twice and stored in memory (could be a problem for large files)

import os
import sys
sys.path.append('../')

from px_aux import saveFile as _saveFile
from px_aux_add_suffix import processContent as _processContent

TXT_FOLDER = "/files_txt/"
SPW_FOLDER = "/files_s_p_w/"


# to process a file and store the result as file.s   
def processFile (filename):
	with open(filename, 'r') as content_file:
		content = content_file.read()  # the original content of file is read 
	
		# to process a textual content
		# returns a tupla (text changed, html text with highlighted changes, no changes report, HTML no changes report)
		result = _processContent(content)  
		
		if result == None:
			print("no change")
			_saveFile(filename+".s", content)    # store result without changes in a file with '.s' extension 
			_saveFile(filename+".s.html", content)  # store result without changes in an HTML report file
		else:
			print("changes")
			_saveFile(filename+".s", result[0])     # store result with changes in a file with '.s' extension 
			_saveFile(filename+".s.html", result[1])   # store result with changes in an HTML report file
			
			# store results reporting studied changes finally not done
			if result[2] != "":
				_saveFile(filename+".s.nr", result[2])
				_saveFile(filename+".s.nr.html", result[3])
	return


def processFolder (foldername):
	txt_folder = foldername + TXT_FOLDER
	if not os.path.exists(txt_folder):
		printf(txt_folder, "not found!")
		exit()
	spw_folder = foldername + SPW_FOLDER
	if not os.path.exists(spw_folder):
		os.makedirs(spw_folder)
	
	numFiles = 0
	for filename in sorted(os.listdir(txt_folder)):
		if not filename.endswith(".txt"):
			continue
		else:
			numFiles += 1
			print("\n", numFiles, " **************** Processing file ", txt_folder+filename+"...\n")
			
			with open(txt_folder+filename, 'r') as content_file:
				content = content_file.read()  # the original content of file is read 
	
				# to process a textual content
				# returns a tupla (text changed, html text with highlighted changes, no changes report, HTML no changes report)
				result = _processContent(content)  
		
				if result == None:
					print("no change")
					_saveFile(spw_folder+filename+".s", content)    # store result without changes in a file with '.s' extension 
					_saveFile(spw_folder+filename+".s.html", content)  # store result without changes in an HTML report file
				else:
					print("changes")
					_saveFile(spw_folder+filename+".s", result[0])     # store result with changes in a file with '.s' extension 
					_saveFile(spw_folder+filename+".s.html", result[1])   # store result with changes in an HTML report file
			
					# store results reporting studied changes finally not done
					if result[2] != "":
						_saveFile(spw_folder+filename+".s.nr", result[2])
						_saveFile(spw_folder+filename+".s.nr.html", result[3])
	return




# to aggregate in a global file (folder.s) all resulting files in a folder 
# files are joined following alphabetic order of the file names   
def generateAgregate (foldername):
	print("\nCreating aggregation "+foldername+".s...")
	numFiles = 0
	global_content = ""
	
	spw_folder = foldername + SPW_FOLDER
	
	for filename in sorted(os.listdir(spw_folder)):   # files are ordered by alphabetic file name 
		if not filename.endswith(".s"):
			continue
		else:
			numFiles += 1
			print(numFiles, "====================", filename)
			with open(spw_folder+"/"+filename, 'r') as content_file:
				content = content_file.read()
				global_content += content
				
	_saveFile(foldername+"/"+foldername+".s", global_content)
	return

# end of aux functions 


# start script execution

# variable to control if aggregation must be created     
join = False

# one parameter is required  
if len(sys.argv) < 2:
	print("Use: "+sys.argv[0]+" [-g] file|folder")
	exit(-1)


if len(sys.argv) == 2:
	param = sys.argv[1]
	
# if two parameters, the first one must be '-g'
elif len(sys.argv) == 3:
	if sys.argv[1] == "-g":
		join = True
		param = sys.argv[2]
	else:
		print("Use: "+sys.argv[0]+" [-g] file|folder")
		exit(-1)
# more than two parameters is not permitted
else:
	print("Use: "+sys.argv[0]+" [-g] file|folder")
	exit(-1)

	
	
# start processing

# it is a file
if os.path.isfile(param):
	if not param.endswith(".txt"):
		print("The file "+param+" is not '.txt'")
		exit(-1)
	print("Processing file "+param+"...\n")
	processFile(param)
	
# it is a folder: all '.txt' files inside are processed 
elif os.path.isdir(param):
	if not os.path.exists(param):
		printf(param, "not found!")
		exit()
	print("Processing folder "+param+"...")
	processFolder(param)
	
	# if -g, all resulting files are aggregated
	if join:
		generateAgregate(param)
	
else:
	print("param is neither a file nor a folder")
	


	