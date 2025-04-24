import os

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from services import process_text

app = Flask(__name__)
app.config['MEDIA_FOLDER'] = 'media/'


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')

        if file and file.filename.endswith('.txt'):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['MEDIA_FOLDER'], filename)
            file.save(filepath)

            with open(filepath, 'r', encoding='utf-8') as fl:
                content = fl.read()

            df = process_text(content)
            return render_template('table.html',
                                   table=df.to_dict(orient='records'))
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
