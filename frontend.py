from flask import Flask, render_template
from flask_bootstrap import Bootstrap

from modules.get_all import clustered_items

app = Flask(__name__)
Bootstrap(app)

import json

# [{'score': 0.091796, 'tone_name': 'Anger', 'tone_id': 'anger'}, {'score': 0.052257, 'tone_name': 'Disgust', 'tone_id': 'disgust'}, {'score': 0.147788, 'tone_name': 'Fear', 'tone_id': 'fear'}, {'score': 0.046793, 'tone_name': 'Joy', 'tone_id': 'joy'}, {'score': 0.522373, 'tone_name': 'Sadness', 'tone_id': 'sadness'

tone_mapping = {
    'disgust': 'success',
    'sadness': 'info',
    'anger': 'danger',
    'fear': 'warning',
    'joy': 'primary'
}


for cluster in list(clustered_items.values()):
    for item in cluster:
        tone_categories = item['item']['item'].get('sentiment', {}).get('document_tone', {}).get('tone_categories', False)

        if tone_categories:
            #print(tone_categories)
            for cat in tone_categories:
                if cat['category_id'] == 'emotion_tone':
                    item['tones'] = {}
                    for tone in cat['tones']:
                        item['tones'][tone_mapping[tone['tone_id']]] = int(tone['score'] * 10)

# disgustr -> grün
# sadness -> hellblau
# anger -> rot
# fear -> gelb
# joy -> dunkelblau

@app.route('/')
def clusters():
    return render_template('clusters.html', clusters=list(clustered_items.values()), mapping=tone_mapping)


if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
