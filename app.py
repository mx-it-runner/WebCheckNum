
from flask import Flask, render_template, request, send_file, session, url_for, redirect
import pandas as pd

app = Flask(__name__)

mapped_data = []
error_data = []

@app.route('/')
@app.route('/home')
def index():
    mapped_data.clear()
    error_data.clear()
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Получение загруженного файла из запроса
        numbers_data = request.files['file']
        
        # Проверка наличия файла
        if numbers_data.filename == '':
            return 'Файл не выбран'

        # Проверка расширения файла
        if numbers_data.filename.endswith('.xlsx'):
            # Обрабатываем содержимое файла
           
            non_number = 0
            complit_number = 0
            empty_string = 0
            
            try:
                df = pd.read_excel(numbers_data)
                def_data = pd.read_excel('Data.xlsx')
                
                for n in df['Numbers']:
                    x = str(n)
                    if (len(x)) == 11 and x[1] == "9":
                        complit_number += 1
                        kod_operatora = x[1:4]
                        nomer =  x[4:11]
                        
                        match = def_data[(def_data['АВС/ DEF'] == int(kod_operatora)) & (def_data['От'] <= int(nomer)) & (def_data['До'] >= int(nomer))]
                        
                        if not match.empty:
                            operator = match['Оператор'].iloc[0]
                            region = match['Регион'].iloc[0]
                            
                            mapped_data.append([n, operator, region])
                    
                    elif match.empty:
                        empty_string += 1
                        
                    else:
                        non_number += 1
                        error_data.append([n])
                
                return render_template('result.html', mapped_data=mapped_data, complit_number=complit_number, empty_string=empty_string, non_number=non_number, error_data=error_data)
            
            except Exception as e:
                return f"Ошибка при обработке загруженного файла: {str(e)}"
        else:
            return 'Разрешены только файлы с расширением XLSX'

    return render_template('upload.html')


@app.route('/download_processed', methods=['GET'])
def download_processed():
    # Код для загрузки обработанных номеров
    mapped_df = pd.DataFrame(mapped_data, columns=['Номер', 'Оператор сотовой связи', 'Регион'])
    mapped_df.to_excel('output.xlsx', index=False)
    return send_file('output.xlsx', as_attachment=True)

@app.route('/download_unprocessed', methods=['GET'])
def download_unprocessed():
    # Код для загрузки необработанных номеров
    error_data_df = pd.DataFrame(error_data, columns=['Номер'])
    error_data_df.to_excel('errornum.xlsx', index=False)
    return send_file('errornum.xlsx', as_attachment=True)

@app.route('/number', methods=['GET', 'POST'])
def check_num_bufer():
    
    return render_template('number.html')

if __name__ == '__main__':
    app.run(debug=True)