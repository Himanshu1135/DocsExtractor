import nltk
import re,cv2
import spacy
from nltk import ne_chunk, pos_tag
from nltk.tokenize import word_tokenize
from nltk.tree import Tree
import keras_ocr
from PIL import Image
import pytesseract
import stanza
from flair.data import Sentence
from flair.models import SequenceTagger

file_path = 'name_corpus.txt'
# Open the file
with open(file_path, 'r') as file:
    # Read the contents of the file
    corpus_text = file.read()

def pytess_text(img_path):
    '''
    Input : img path
    working : Extract text from image using pytessract OCR
    return : extracted text
    '''

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    img = cv2.imread(img_path)
    # ----------- Converting to grey img for better text extraction
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    text = pytesseract.image_to_string(gray_image, lang = 'eng')
    return text

def keras_text(img_path):
    # keras-ocr will automatically download pretrained
    # weights for the detector and recognizer.
    pipeline = keras_ocr.pipeline.Pipeline()

    images = keras_ocr.tools.read(img_path)

    prediction_groups = pipeline.recognize([images])

    predictions = prediction_groups[0]
    predictions = [(word, tuple(bbox[::-1])) for word, bbox in predictions]


    text = []
    for word, bounding_box in predictions:
        text.append(word)
    # text = text[::-1]
    text = ' '.join(text)
    return text

def extract_names_nltk(text):

    names = []
    sentences = nltk.sent_tokenize(text)
    for sentence in sentences:
        words = nltk.word_tokenize(sentence)
        tagged_words = nltk.pos_tag(words)
        chunked_words = ne_chunk(tagged_words)
        for subtree in chunked_words.subtrees(filter=lambda t: t.label() == 'PERSON'):
            name = ""
            for leaf in subtree.leaves():
                name += leaf[0] + " "
            names.append(name.strip())
    return names
def extract_names_spacy(text):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    
    names = []
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            # confidence = ent.label_.confidence
            names.append((ent.text))
    
    return names

def extract_name_flair(text):
    tagger = SequenceTagger.load('ner')

    # text = "I met a person named John Smith yesterday."
    sentence = Sentence(text)

    tagger.predict(sentence)

    names = [entity.text for entity in sentence.get_spans('ner') if entity.tag == 'PER']

    return names

def extract_names_stanza(text):
    nlp = stanza.Pipeline(lang="en", processors="tokenize,ner")
    doc = nlp(text)
    names = []

    for sent in doc.sentences:
        for ent in sent.ents:
            if ent.type == "PERSON":
                names.append(ent.text)

    return names

def gender(text):
    exp = "MALE|FEMALE|Male|Female"
    x = re.findall(exp, text)

    if len(x) != 0:
        return x[0]    
    else:
        return None
def Aadhaar_no(text):
    exp = "\d{4}\s\d{4}\s\d{4}"
    x = re.findall(exp, text)
    if len(x) != 0:
        y = re.sub("\s","",x[0])
        return y    
    else:
        return None
    
def dob(text):
    exp = "\d{2}/\d{2}/\d{4}|\d{2}/\d{2}/\d \d{3}|\d{2}-\d{2}-\d{4}"
    x = re.findall(exp, text)
    if len(x) != 0:
        y = re.sub("\s","",x[0])
        return y    
    else:
        res = get_year_of_birth(text,"Year of Birth")
        return res
        
def get_year_of_birth(text, target_word):
    pattern = r'\b' + re.escape(target_word) + r'\b'
    match = re.search(pattern, text)
    if match:
        index = match.end()
        words = text[index:].split()
        txt = words[0]+ " " + words[1]
        pattern_2 = "\d{4}"
        match_2 = re.search(pattern_2, txt)
        if match_2:
            return match_2[0]
    else:    
        return None

def get_Aadhaar_name(text):
    
    '''
    input : text 
    working : find person name before target word {pattern}
    return : list of names
    '''
    
    target_word = "Year of Birth|DOB|D0B|Mother"
    # pattern = r'\b' + re.escape(target_word) + r'\b'
    pattern = r'\b' + target_word + r'\b'
    match = re.search(pattern, text)

#----- first match target word to split text

    if match:
        index = match.end()
        words = text[:index].split()
        
        if words:
            ext_txt = ' '.join(words)

            # names = extract_names_nltk(ext_txt)  #----------------For name extraction from nltk------------#
            
#---------- using extract name corpus function
            names = extract_name_corpus(ext_txt,corpus_text)
            if names != None:
                return names
            else:
                return None
    else:
        names = extract_name_corpus(text,corpus_text)
        if names != None:
            return names 
        else:
                return None

def pan_No(text):
    exp = "[\d|\w]\w{4}\d{4}\w"
    x = re.findall(exp, text)
    if len(x) != 0:
        y = re.sub("\s","",x[0])
        return y    
    else:
        return None

# def get_next_word(text, target_word):

#     pattern = r'\b' + re.escape(target_word) + r'\b'
#     match = re.search(pattern, text)
    
#     if match:
#         index = match.end()
#         words = text[index:].split()
        
#         if words:
#             return words[0]+ " " + words[1]
    
#     return None

def pan_names_person(text):
    '''
    input : text 
    working : find person name before target word {pattern}
    return : list of names
    '''
    pattern = "Father|Father's"
    match = re.search(pattern, text)
#----- first match target word to split text for seprating name with father name
    if match:
        index = match.end()
        words = text[:index].split()
        if words:
            words = ' '.join(words)
            names = extract_name_corpus(words,corpus_text)
            return names
    else:
        names = extract_name_corpus(text,corpus_text)
#-------------- if names contain more then 3 element then search for surname
        if len(names) > 3:  
            duplicates = surname_duplicates(names)
            if duplicates != None:
                return names[:duplicates+1]
            else:
                return names[:2]
        else:
            return names
    
def pan_names_father(text):
    pattern = "Father|Father's"
    match = re.search(pattern, text)
    
    if match:
        index = match.end()
        words = text[index:].split()
        if words:
            words = ' '.join(words)
            names = extract_name_corpus(words,corpus_text)
            return names
    else:
        names = extract_name_corpus(text,corpus_text)

        if len(names) > 3:
            duplicates = surname_duplicates(names)
            if duplicates != None:
                return names[duplicates+1:]
            else:
                return names[2:]
        else:
            return []   

def extract_name_corpus(txt,corpus_text):
    '''
    input : text 
    input2 : corpus text from which it will match names
    working : finds human names by match text in corpus text names 
    return : list of names 
    '''
    arr = []
    txt = txt.strip().replace('\n', ' ').replace('  ', ' ')
    txt = re.sub(r'\s+', ' ', txt) 
    words = txt.split()

    for word_to_match in words:
        matches = re.findall(r'\b' + re.escape(word_to_match) + r'\b', corpus_text, re.IGNORECASE)
        if len(matches) !=0 :
            arr.append(matches[0])
    return arr

def surname_duplicates(arr):
    duplicates = []
    seen = set()
    for i, item in enumerate(arr):
        if item in seen:
            duplicates.append(i)
        else:
            seen.add(item)
    if len(duplicates) !=0:
        idx = duplicates[0]
        val = arr[idx]
        count = 0
        for j in arr:
            if j == val:
                return count
            count += 1
    else:
        return None

##---------------------------------------- JSON ---------------------------------------------------##
#     data = {
#     "Name :": get_Aadhaar_name(text),
#     "Gender: ":gender(text),
#     "Aadhaar No: ":Aadhaar_no(text),
#     "Date of Birth: ":dob(text),
#     "Text":text
# }
#     file_path = r"D:\Stractmine\image\res_adh/" + filename  # Replace with the desired directory path

#     with open(file_path, "w") as json_file:
#         json.dump(data, json_file)

##---------------------------------------for corpus manupulation -------------------------##
# with open('name_corpus.txt', 'r') as file:
#     corpus_content = file.read()

# text = corpus_content.split()

# sorted_words = sorted(text)

# # filtered_words = [word for word in text if len(word) >= 3]

# updated_corpus = '\n'.join(sorted_words)

# with open('name_corpus.txt', 'w') as file:
#     file.write(updated_corpus)