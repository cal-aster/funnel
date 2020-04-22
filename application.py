# Author:  Meryll Dindin
# Date:    11 April 2020
# Project: Funnel

from imports import *

# Server instantiation
app = Flask(__name__)
app.secret_key = os.environ['FLASK_SECRET_KEY']
# Handle headers properly
CORS(app)

# Route to measure health response
@app.route('/health', methods=['GET'])
def health():

    arg = {'status': 200, 'mimetype': 'application/json'}
    return Response(json.dumps({'status': 'online'}), **arg)

# Decision Tree: Step 01
# Q: Bonjour, nos centres d'appels sont actuellement satures. Pour aider a la decongestion, 
# dites nous s'il s'agit d'un appel lie au coronavirus?
@app.route('/', methods=['POST'])
def step_01():

    src = request.values.get('SpeechResult').lower()
    src = re.sub('[^a-zA-Z]+', ' ', src)

    if 'non' in src.split():
        snd = 'https://calaster-funnel.s3.eu-west-3.amazonaws.com/divert-samu.mp3'
        xml = '<Response><Play>{}</Play></Response>'.format(snd)
        xml = etree.tostring(etree.XML(xml), method='xml')

    else:
        snd = 'https://calaster-funnel.s3.eu-west-3.amazonaws.com/classification.mp3'
        url = 'need-for-medical-assistance'
        with open('template.xml') as f: xml = "".join([e.strip() for e in f.readlines()])
        xml = etree.tostring(etree.XML(xml.format(snd, url)), method='xml')
    
    arg = {'status': 200, 'mimetype': 'text/xml'}
    return Response(xml, **arg)

# Decision Tree: Step 02
# Q: Avez vous, ou un membre de votre entourage, besoin d'une intervention medicale ?
@app.route('/need-for-medical-assistance', methods=['POST'])
def step_02():

    src = request.values.get('SpeechResult').lower()
    src = re.sub('[^a-zA-Z]+', ' ', src)

    if 'non' in src.split():
        snd = 'https://calaster-funnel.s3.eu-west-3.amazonaws.com/divert-green.mp3'
        xml = '<Response><Play>{}</Play></Response>'.format(snd)
        xml = etree.tostring(etree.XML(xml), method='xml')
    else:
        snd = 'https://calaster-funnel.s3.eu-west-3.amazonaws.com/question-01.mp3'
        url = 'symptom-1'    
        with open('template.xml') as f: xml = "".join([e.strip() for e in f.readlines()])
        xml = etree.tostring(etree.XML(xml.format(snd, url)), method='xml')

    arg = {'status': 200, 'mimetype': 'text/xml'}
    return Response(xml, **arg)

# Decision Tree: Step 03
# Q: Pour aider l'operateur qui va vous prendre en charge, veuillez repondre rapidement par 
# oui ou non a ces quelques questions: Vous est-il impossible de boire ou de vous alimenter ?
@app.route('/symptom-1', methods=['POST'])
def step_03():

    src = request.values.get('SpeechResult').lower()
    src = re.sub('[^a-zA-Z]+', ' ', src)

    if 'oui' in src.split():
        snd = 'https://calaster-funnel.s3.eu-west-3.amazonaws.com/divert-medical-urgent.mp3'
        xml = '<Response><Play>{}</Play></Response>'.format(snd)
        xml = etree.tostring(etree.XML(xml), method='xml')
    else:
        snd = 'https://calaster-funnel.s3.eu-west-3.amazonaws.com/question-02.mp3'
        url = 'symptom-2'
        with open('template.xml') as f: xml = "".join([e.strip() for e in f.readlines()])
        xml = etree.tostring(etree.XML(xml.format(snd, url)), method='xml')

    arg = {'status': 200, 'mimetype': 'text/xml'}
    return Response(xml, **arg)

# Decision Tree: Step 04
# Q: Ces derniers jours, avez vous souffert de troubles respiratoires ?
@app.route('/symptom-2', methods=['POST'])
def step_04():

    src = request.values.get('SpeechResult').lower()
    src = re.sub('[^a-zA-Z]+', ' ', src)

    if 'oui' in src.split():
        snd = 'https://calaster-funnel.s3.eu-west-3.amazonaws.com/divert-medical-urgent.mp3'
        xml = '<Response><Play>{}</Play></Response>'.format(snd)
        xml = etree.tostring(etree.XML(xml), method='xml')
    else:
        snd = 'https://calaster-funnel.s3.eu-west-3.amazonaws.com/question-03.mp3'
        url = 'symptom-3'
        with open('template.xml') as f: xml = "".join([e.strip() for e in f.readlines()])
        xml = etree.tostring(etree.XML(xml.format(snd, url)), method='xml')

    arg = {'status': 200, 'mimetype': 'text/xml'}
    return Response(xml, **arg)

# Decision Tree: Step 05
# Q: Ces derniers jours, avez vous observe une perte du gout et/ou de l'odorat ?
@app.route('/symptom-3', methods=['POST'])
def step_05():

    url = 'symptom-4'
    snd = 'https://calaster-funnel.s3.eu-west-3.amazonaws.com/question-04.mp3'

    with open('template.xml') as f: xml = "".join([e.strip() for e in f.readlines()])
    xml = etree.tostring(etree.XML(xml.format(snd, url)), method='xml')

    arg = {'status': 200, 'mimetype': 'text/xml'}
    return Response(xml, **arg)

# Decision Tree: Step 06
# Q: Ces derniers jours, avez vous developpe une fievre et/ou une toux seche?
@app.route('/symptom-4', methods=['POST'])
def step_06():

    url = 'symptom-5'
    snd = 'https://calaster-funnel.s3.eu-west-3.amazonaws.com/question-05.mp3'

    with open('template.xml') as f: xml = "".join([e.strip() for e in f.readlines()])
    xml = etree.tostring(etree.XML(xml.format(snd, url)), method='xml')

    arg = {'status': 200, 'mimetype': 'text/xml'}
    return Response(xml, **arg)

# Decision Tree: Step 07
# Q: Ces derniers jours, avez vous eu le nez congestionne, mal a la gorge, et/ou 
# des douleurs musculaires inhabituelles ?
@app.route('/symptom-5', methods=['POST'])
def step_07():

    url = 'redirect-medical'
    snd = 'https://calaster-funnel.s3.eu-west-3.amazonaws.com/question-06.mp3'

    with open('template.xml') as f: xml = "".join([e.strip() for e in f.readlines()])
    xml = etree.tostring(etree.XML(xml.format(snd, url)), method='xml')

    arg = {'status': 200, 'mimetype': 'text/xml'}
    return Response(xml, **arg)

# Decision Tree: Step 08
# Q: Ces derniers jours, avez vous eu la diarrhee ?
@app.route('/redirect-medical', methods=['POST'])
def step_08():

    snd = 'https://calaster-funnel.s3.eu-west-3.amazonaws.com/divert-medical.mp3'
    xml = '<Response><Play>{}</Play></Response>'.format(snd)
    xml = etree.tostring(etree.XML(xml), method='xml')

    arg = {'status': 200, 'mimetype': 'text/xml'}
    return Response(xml, **arg)

