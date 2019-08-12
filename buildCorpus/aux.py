

# folders and filenames involved in corpus construction

MODELS_FOLDER = "../MODELS"
LEE_D2V_MODEL = MODELS_FOLDER+"/model_d2v_lee.model"
OWN_D2V_MODEL = MODELS_FOLDER+"/model_d2v_own-t.model"

# initial text for corpus building
INITIAL_TEXT = 'initialText.txt'

CORPUS_FOLDER = "KORPUS"

# All these files and folders will be created inside CORPUS_FOLDER

WIKICAT_LIST_FILENAME = "WIKICAT_LIST.txt"  # to save the set of wikicats from text
SELECTED_WIKICAT_LIST_FILENAME = "SELECTED_WIKICAT_LIST.txt"   # to save the last set of selected wikicats to initially be marked in the interface

# these are the files and folders created in the building of corpus

URLs_FOLDER = CORPUS_FOLDER+"/URLs"
SCRAPPED_TEXT_PAGES_FOLDER = CORPUS_FOLDER+"/SCRAPPED_TEXT_PAGES"
DISCARDED_PAGES_FILENAME = CORPUS_FOLDER+"/discarded_list.txt"
UNRETRIEVED_PAGES_FILENAME = CORPUS_FOLDER+"/unretrieved_pages.txt"
SIMILARITIES_CSV_FILENAME = CORPUS_FOLDER+"/similarity.csv"
HTML_PAGES_FOLDER = CORPUS_FOLDER+"/HTML_PAGES"


# to check if a dictionary has the field 'pt' (isPrimaryTopicOf), that is a dictionary that must contain the field 'value'
def hasFieldPT(x):
	try:
		x["pt"]["value"]
		return True
	except:
		return False