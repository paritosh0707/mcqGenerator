import os
import PyPDF2
import json
import traceback

def read_file(file):
    if(file.name.endswith('.pdf')):
        try:
            pdf_reader = PyPDF2.PdfFileReader(file)
            text = ""
            for page in pdf_reader.pages:
                text+=page.extract_text()
            return text
        except Exception as e:
            raise Exception("error reading file")
        
    elif(file.name.endswith('.txt')):
        try:
            text = file.read().decode('utf-8')
            return text
        except Exception as e:
            raise Exception("error reading file")
        
    else:
        raise Exception("undupproted file format only .pdf and .txt are supported")
    

def get_table_data(quiz_str):
    try:
        quiz_dict = json.loads(quiz_str)
        quiz_data_table = []

        for key, value in quiz_dict.items():
            mcq = value['mcq']
            options = " || ".join(
                [
                    f"{option}-> {option_value}" for option, option_value in value['options'].items()
                ]
            )

            correct = value["correct"]
            quiz_data_table.append({"MCQ": mcq, "Choices": options, "correct": correct})

        return quiz_data_table
    except Exception as e:
        traceback.print_exception(type(e),e,e.__traceback__)
        return False