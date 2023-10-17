
from flask import Flask, render_template, url_for, request, send_file
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Получение загруженного файла из запроса
        file = request.files['file']

        # Проверка наличия файла
        if file.filename == '':
            return 'Файл не выбран'

        # Проверка расширения файла
        if file.filename.endswith('.xlsx'):
            # Обрабатываем содержимое файла
            numbers = []
            try:
                df = pd.read_excel(file)
                numbers = df['Numbers'].tolist()
                return str(numbers)
            except Exception as e:
                return f"Ошибка при обработке загруженного файла: {str(e)}"
        else:
            return 'Разрешены только файлы с расширением XLSX'

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)