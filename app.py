from flask import Flask, render_template, request, send_file
import nltk
from nltk.corpus import stopwords
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import string
from io import BytesIO

app = Flask(__name__)

# Download stopwords dari NLTK
nltk.download('stopwords')

def remove_stopwords(text):
    # Mengambil stopwords bahasa Indonesia dari NLTK dan Sastrawi
    nltk_stopwords = set(stopwords.words('indonesian'))
    sastrawi_factory = StopWordRemoverFactory()
    sastrawi_stopwords = sastrawi_factory.get_stop_words()

    # Menggabungkan stopwords dari kedua sumber
    combined_stopwords = nltk_stopwords.union(sastrawi_stopwords)

    # Memisahkan teks menjadi paragraf
    paragraphs = text.split('\n')
    filtered_paragraphs = []

    for paragraph in paragraphs:
        # Mengubah teks menjadi lowercase dan menghapus tanda baca
        paragraph = paragraph.lower()
        paragraph = paragraph.translate(str.maketrans("", "", string.punctuation))

        # Memisahkan paragraf menjadi kata-kata
        words = paragraph.split()

        # Menghapus stopwords
        filtered_words = [word for word in words if word not in combined_stopwords]

        # Menggabungkan kata-kata yang tersisa dalam paragraf
        filtered_paragraph = " ".join(filtered_words)
        filtered_paragraphs.append(filtered_paragraph)

    # Menggabungkan paragraf yang telah difilter
    filtered_text = "\n".join(filtered_paragraphs)

    return filtered_text

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        input_text = request.form['input_text']
        result = remove_stopwords(input_text)
    return render_template('index.html', result=result)

@app.route('/download')
def download():
    result = request.args.get('result')
    if result:
        # Membuat file sementara di memori
        buffer = BytesIO()
        buffer.write(result.encode('utf-8'))
        buffer.seek(0)
        
        # Mengirim file untuk diunduh
        return send_file(buffer, 
                         as_attachment=True, 
                         download_name='hasil_filtering.txt', 
                         mimetype='text/plain')
    return "Tidak ada hasil untuk diunduh", 400

if __name__ == '__main__':
    app.run(debug=True)