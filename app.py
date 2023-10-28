
from flask import Flask, render_template, request, send_file, url_for, redirect
import pandas as pd
import re

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
    mapped_data.clear()
    error_data.clear()
    if request.method == 'POST':
        # Получение загруженного файла из запроса
        numbers_data = request.files['file']
        
        # Проверка наличия файла
        if numbers_data.filename == '':
            return render_template('upload.html')

        # Проверка расширения файла
        if numbers_data.filename.endswith('.xlsx'):

            non_number = 0
            complit_number = 0
            empty_string = 0
            
            try:
                df = pd.read_excel(numbers_data, header=None)
                def_data = pd.read_excel('Data.xlsx')
                
                for n in df[0]:
                    str_num = str(n)
                    
                    if str_num != "" and str_num != "nan":
                        digits = "".join(filter(str.isdigit, str_num))
                                        
                        if (len(digits)) == 11:
                        
                            kod_operatora = digits[1:4]
                            nomer =  digits[4:11]
                        
                            match = def_data[(def_data['АВС/ DEF'] == int(kod_operatora)) & (def_data['От'] <= int(nomer)) & (def_data['До'] >= int(nomer))]
                        
                            if not match.empty:
                                operator = match['Оператор'].iloc[0]
                                region = match['Регион'].iloc[0]
                                complit_number += 1
                            
                                mapped_data.append([n, operator, region])
                        
                            else:
                                non_number += 1
                                error_data.append([n])
                    
                        elif (len(digits)) == 10:
                            digits = "7" + digits
                        
                            kod_operatora = digits[1:4]
                            nomer =  digits[4:11]
                        
                            match = def_data[(def_data['АВС/ DEF'] == int(kod_operatora)) & (def_data['От'] <= int(nomer)) & (def_data['До'] >= int(nomer))]
                        
                            if not match.empty:
                                operator = match['Оператор'].iloc[0]
                                region = match['Регион'].iloc[0]
                                complit_number += 1
                            
                                mapped_data.append([n, operator, region])
                        
                        else:
                            non_number += 1
                            error_data.append([n])
                        
                    else:
                        empty_string += 1
                           
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


 # Отдать файл на скачавания необработанных номеров
@app.route('/download_unprocessed', methods=['GET'])
def download_unprocessed():
    # Код для загрузки необработанных номеров
    error_data_df = pd.DataFrame(error_data, columns=['Номер'])
    error_data_df.to_excel('errornum.xlsx', index=False)
    return send_file('errornum.xlsx', as_attachment=True)


@app.route('/number', methods=['GET', 'POST'])
def check_num_bufer():
    mapped_data.clear()
    error_data.clear()

    def_data = pd.read_excel('Data.xlsx')
    non_number = 0
    complit_number = 0
    
    if request.method == 'POST':
        numbers = request.form.get('numbers')
        separator = request.form['radio']
        if separator == "":
            numbers_array = numbers.split('\n')
        else:
            numbers_array = numbers.split(separator)
            
        cleaned_array = []
        
        for item in numbers_array:
            cleaned_item = re.sub(r'\D', '', item)
            cleaned_array.append(cleaned_item)
        
        for com_num in cleaned_array:
            if (len(com_num)) == 11:
                kod_operatora = com_num[1:4]
                nomer =  com_num[4:11]
                        
                match = def_data[(def_data['АВС/ DEF'] == int(kod_operatora)) & (def_data['От'] <= int(nomer)) & (def_data['До'] >= int(nomer))]
                        
                if not match.empty:
                    operator = match['Оператор'].iloc[0]
                    region = match['Регион'].iloc[0]
                    complit_number += 1
                            
                    mapped_data.append([com_num, operator, region])
                        
                else:
                    non_number += 1
                    error_data.append([com_num])
            
            elif (len(com_num)) == 10:
                com_num = "7" + com_num
                        
                kod_operatora = com_num[1:4]
                nomer =  com_num[4:11]
                        
                match = def_data[(def_data['АВС/ DEF'] == int(kod_operatora)) & (def_data['От'] <= int(nomer)) & (def_data['До'] >= int(nomer))]
                        
                if not match.empty:
                    operator = match['Оператор'].iloc[0]
                    region = match['Регион'].iloc[0]
                    complit_number += 1
                            
                    mapped_data.append([com_num, operator, region])
                        
            else:
                non_number += 1
                error_data.append([com_num])
        
        return render_template('bufercomplit.html', mapped_data=mapped_data, complit_number=complit_number, non_number=non_number, error_data=error_data)
            
    return render_template('number.html')


    
if __name__ == '__main__':
    app.run(debug=True)