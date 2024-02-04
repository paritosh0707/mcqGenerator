import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from mcqGenerator.utils import read_file, get_table_data 
from mcqGenerator import logger
import streamlit as st
from langchain.callbacks import get_openai_callback
from mcqGenerator import mcq_generator


## load the response json file
with open('response.json','r') as file:
    RESPONSE_JSON = json.load(file)

st.title("MCQ Generator App langchain 🔗 🦜")

with st.form("user input"):
    uploaded_file = st.file_uploader("upload a pdf or text file")

    mcq_count = st.number_input("No' of MCQs", min_value=3, max_value=15)

    subject = st.text_input("Topic of the Quiz", max_chars=20)

    tone = st.text_input("Complexity of the Quiz", max_chars=20, placeholder='Simple')

    button = st.form_submit_button("Create MCQs")

    if button and uploaded_file and mcq_count and subject and tone is not None:
        with st.spinner('...loading !!'):
            try:
                text = read_file(uploaded_file)

                with get_openai_callback() as cb:
                    response = mcq_generator.final_integerated_chain(
                        {
                            "text": text,
                            "number": mcq_count,
                            "subject": subject,
                            "tone": tone,
                            "response_json": json.dumps(RESPONSE_JSON)
                        }
                    )
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error('Error in MCQ generation')

            else:
                print(f"Total Tokens:{cb.total_tokens}")
                print(f"Prompt Tokens:{cb.prompt_tokens}")
                print(f"Completion Tokens:{cb.completion_tokens}")
                print(f"Total Cost:{cb.total_cost}")
                if isinstance(response, dict):
                    quiz = response.get('quiz',None)
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            # df.to_csv('result_mcq.csv').encode("utf-8")
                            df.index = df.index+1
                            st.table(df)

                            st.text_area(label='Review',value=response['review'])
                        else:
                            st.error("Error in the table")
                else:
                    st.write(response)
# if(button):
#     download_data = pd.read_csv('result_mcq.csv')
#     st.download_button(
#                                     label="Download data as CSV",
#                                     data=download_data,
#                                     file_name='mcq.csv',
#                                     mime='text/csv',
#                                 )