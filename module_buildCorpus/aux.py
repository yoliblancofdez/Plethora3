
from nltk.tokenize import RegexpTokenizer
import nltk
import re
import os

# folders and filenames involved in corpus construction

MODELS_FOLDER = "../MODELS"
LEE_D2V_MODEL = MODELS_FOLDER+"/model_d2v_lee.model"
OWN_D2V_MODEL = MODELS_FOLDER+"/model_d2v_own-t.model"

# initial text for corpus building
INITIAL_TEXT = 'initialText.txt'

CORPUS_FOLDER = os.getenv('HOME') + "/Google Drive/KORPUS"

# these are the files and folders created in the building of corpus

URLs_FOLDER = CORPUS_FOLDER+"/URLs"
SCRAPPED_TEXT_PAGES_FOLDER = CORPUS_FOLDER+"/SCRAPPED_TEXT_PAGES"
DISCARDED_PAGES_FILENAME = CORPUS_FOLDER+"/discarded_pages.txt"
UNRETRIEVED_PAGES_FILENAME = CORPUS_FOLDER+"/unretrieved_pages.txt"
SIMILARITIES_CSV_FILENAME = CORPUS_FOLDER+"/similarities.csv"
HTML_PAGES_FOLDER = CORPUS_FOLDER+"/HTML_PAGES"

CORPUS_MIN_TXT_SIZE = 300  # this is the minimum size of a file to be added to the corpus

PSTOP = False  # to control if sw must pause after each phase (change to True if argument -s)

# set of english stopwords
nltk_stopwords = nltk.corpus.stopwords.words('english')

# function to check if a word is in the English stopwords set (to be used in a filter)
def isNotStopWord (word):
	if word.lower() not in nltk_stopwords:
		return True
	return False


# to check if a dictionary has the field 'pt' (isPrimaryTopicOf), that is a dictionary that must contain the field 'value'
def hasFieldPT(x):
	try:
		x["pt"]["value"]
		return True
	except:
		return False
	


# no longer used
# function to get the N greatest elements in a list
def NmaxElements(list1, N):
	final_list = []
	
	for i in range(0, N):
		max1 = 0
		
		for j in range(len(list1)):
			if list1[j] > max1:
				max1 = list1[j];
				
		list1.remove(max1);
		final_list.append(max1)
	
	return final_list

def NmaxElements3T(list1, N):
	final_list = []
	try:
		for i in range(0, N):
			max1 = ("","",0)
			
			for j in range(len(list1)):
				if list1[j][2] > max1[2]:
					max1 = list1[j];
					
			if max1 != ("","",0):
				list1.remove(max1);
			else:
				return final_list
			final_list.append(max1)
	except Exception as e:
		print("Exception while computing NmaxElements3T:", e)
		print(list1)
	
	return final_list
###################### 			


# to reject simple wikicats, with only one component
def filterSimpleWikicats (wikicat):
	if (len(getWikicatComponents(wikicat)) == 1):
		return False
	else:
		return True
	
# to reject simple subjects, with only one component
def filterSimpleSubjects (subject):
	if (len(getSubjectComponents(subject)) == 1):
		return False
	else:
		return True
	




# Tokenize text, and returns a list of words (lowercase) after removing the stopwords
def myTokenizer (text):

	# Create a tokenizer
	tokenizer = RegexpTokenizer('\w+')

	# Tokenize text
	tokens = tokenizer.tokenize(text)

	# Get English stopwords from the NLTK (Natural Language Toolkit)
	nltk_stopwords = nltk.corpus.stopwords.words('english')

	# Change words to lower case
	text_words = list(map(lambda x: x.lower(), tokens))
	
	# remove the stopwords
	words_filtered = list(filter(isNotStopWord, text_words))

	return words_filtered


########   compute wikicat and subject components

# to transform some wikicats to unify for further comparison
# this inserts a dash between nth and century (it returns nth-century). the same for nd and st
def processCentury(cad):	
	pattern = re.compile(r"(\d)(th|st|nd)([cC]entury)")
	newcad = pattern.sub(r"\1\2-\3", cad)
	return newcad


# to get the relevant components of a wikicat 
def getWikicatComponents (wikicat):
	components = separateWikicatComponents(wikicat)   # get all the components
	#components_lower = list(map(lambda x: x.lower(), components))  # to lowercase
	
	components_filtered = list(filter(isNotStopWord, components))  # remove stopwords
	return components_filtered



# to get all the single components of a wikicat (format W1W2W3...Wn)
def separateWikicatComponents (wikicat):
	
	wikicat = processCentury(wikicat)  # change 6thcentury to 6th-century, and similars
	
	components = []
	word = ""
	
	long = len(wikicat)
	idx = 0
	
	while idx < long:
		l = wikicat[idx]
		idx += 1  # idx always marks the char following the current one
		
		if len(word) == 0:			# if len(word)==0, then idx==1, this is the first char, put it in the word and continue 
			word = word + str(l)
			continue
		
		if l == '(' or l == ')':
			components.append(word)
			word = ""
			continue
			
		if str(l).isdigit():    # l is a digit.   idx is 2 or higher, as the first char does not arrive here
			if not str(wikicat[idx-2]).isdigit():  # if the previous one is not a digit,
				components.append(word)  # the word was completed with the previous one
				word = str(l)   # and the current digit starts a new word
			else:
				word = word + str(l)   # if the previous one is also a digit, add this digit to the digit sequence
			continue
				
		if l.isupper():      # the new char is uppercase, probably a new word starts
			if wikicat[idx-2] == '-':   # if the previous one is hyphen, it is not a new word, but a composed one
				word = word + str(l)    # add char to this word
				continue
			
			if (idx == long):   # this is the last char of the word
				word = word + str(l)
				continue
			
			if word.isupper():  # this char is uppercase, and all the previous chars are too
				if wikicat[idx].islower():  # if the next one is lowercase, the current char is the start of a new word
					components.append(word)  # add completed word and start a new one
					word = str(l)
				else:
					word = word + str(l)
			else:  # this char is uppercase, but not all the previous chars are 
				if (l == 'B') and (wikicat[idx] == 'C'):  # check if the current char is the beginning of BC or AD
					word = word + "BC" 
					idx += 1
				else:
					if (l == 'A') and (wikicat[idx] == 'D'):
						word = word + "AD"
						idx += 1;
					else:  # current char is uppercase, and no special case, it marks end of word and beginning of a new one
						components.append(word)
						word = str(l)

		else:  # if current char is not uppercase nor digit, add to the current word
			word = word + str(l)
	
		
	if len(word) > 0:
		components.append(word)
	
	return components



# to get the relevant components of a subject 
def getSubjectComponents (subject):
	components = separateSubjectComponents(subject)   # get all the components
	components_lower = list(map(lambda x: x.lower(), components))  # to lowercase
	
	components_filtered = list(filter(isNotStopWord, components_lower))  # remove stopwords
	return components_filtered


# to get all the single components of a subject (format W1_W2_W3_..._Wn)
def separateSubjectComponents (subject):
	components = subject.split("_")
	return components
