
from flask import Flask, render_template, url_for, request, send_file
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
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
            numbers = []
            mapped_data = []
            error_data = []
            
            non_number = 0
            complit_number = 0
            empty_string = 0
            
            try:
                df = pd.read_excel(numbers_data)
                def_data = pd.read_excel('Data.xlsx')
                
                for n in df['Numbers']:
                    x = str(n)
                    if (len(x)) == 11:
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
                
                output = ""
                
                output += f"Количество чисел, содержащих 11 символов: {complit_number}<br>"
                output += f"Количество чисел с пустыми значениями: {empty_string}<br>"
                output += f"Количество чисел, не являющихся числами: {non_number}<br>"

                output += f"Сопоставленные данные:<br>"
                output += '<br>'.join('<br>'.join(map(str, data)) for data in mapped_data)
                output += "<br>"
                
                output += f"Несопоставленные данные:<br>"
                output += '<br>'.join(str(data) for data in error_data)
                
                return output
            
            except Exception as e:
                return f"Ошибка при обработке загруженного файла: {str(e)}"
        else:
            return 'Разрешены только файлы с расширением XLSX'

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)