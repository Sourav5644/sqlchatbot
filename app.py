from pathlib import Path
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
import sqlite3
import google.generativeai as genai

# Load environment variables first
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model=genai.GenerativeModel('gemini-1.5-flash-latest')



def main():
    st.set_page_config(page_title='SQL Query Generator', page_icon=":robot:")
    st.markdown(
        """
            <div style="text-align: center;">
                <h1>SQL Query Generator</h1>
                <h3>I can generate SQL queries for you!</h3>
                <h4>With explanations as well!</h4>
                
            </div>    
        """,
        unsafe_allow_html=True,
    )

    text_input=st.text_area('Enter your query here in plain English Language')

    

    submit=st.button('Generate SQL Query')
    if submit:
        with st.spinner('Generating SQL Query...'):
            template="""
                Create a SQL query snippet using the below text:
                ```
                   {text_input}
                ```
                I just want a SQL Query
            """
            formatted_template=template.format(text_input=text_input)
            #st.write(formatted_template)
            response=model.generate_content(formatted_template)
            sql_query=response.text

            sql_query=sql_query.strip().lstrip("```sql").rstrip("```")
            #st.write(sql_query)

            expected_output="""
                What would be the expected response of this SQL query snippet:
                        ```
                        {sql_query}
                        ```
                Provide sample tabular Response with no explanation:         
            """
            expected_output_formatted=expected_output.format(sql_query=sql_query)
            eoutput=model.generate_content(expected_output_formatted)
            eoutput=eoutput.text
            #st.write(eoutput)

            explanation="""
                explain this sql Query:
                        ```
                        {sql_query}
                        ```
                Please provide with simplest of explanation:
                """
            explanation_formatted=explanation.format(sql_query=sql_query)   
            explanation=model.generate_content(explanation_formatted)
            explanation=explanation.text
            #st.write(explanation)

            with st.container():
                st.success('SQL Query Generated Successfully! Here is your Query Below:')
                st.code(sql_query, language="sql") 

                st.success('Excepted output of this sql Query will be:')
                st.markdown(eoutput)

                st.success('Explain of this sql Query:')
                st.markdown(explanation)
                     



        #response=model.generate_content(text_input)

        #print(response.text)
        #st.write(response.text)




main()    