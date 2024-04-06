import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.utilities import SQLDatabase
from langchain_core.runnables import RunnablePassthrough
from flask import Flask
from flask import request
from waitress import serve


import json
import os
import sys
import boto3
import botocore

boto3_bedrock = boto3.client('bedrock-runtime')


app = Flask(__name__)


load_dotenv()

# mysql_uri = 'mysql+mysqlconnector://root:mysql321@localhost:3306/searchbotimpldb'
mysql_uri = 'mysql+mysqlconnector://admin:Password0987@searchbottest.craqoyqamc2f.ap-south-1.rds.amazonaws.com:3306/searchbotimpldb'
db = SQLDatabase.from_uri(mysql_uri)

# app config
st.set_page_config(page_title="Streaming search bot", page_icon="🤖")
st.title("Streaming bot")



def get_schema():
    schema = db.get_table_info()
    schema_str = str(schema)
    return schema_str

    # return schema

def run_query(query):
    return db.run(query)


def sql_chain(user_query):
        
    prompt = "Human: Based on the table schema below, write a syntactically correct MySQL query that would answer the user's question correctly, Understand the context and intention of the user question and choose/predict the corresponding database tables which is related to question while generating SQL query, also sql code should not have ''' in the beginning or end and only sql code should be returned as a result" + \
    "\nSchema: " + get_schema() + "\n\nQuestion: " + user_query + "\nAssistant:"
 
    body = json.dumps({"prompt": prompt,
            "max_tokens_to_sample":4096,
            "temperature":0.5,
            "top_k":250,
            "top_p":0.5,
            "stop_sequences":[],
            "anthropic_version": "bedrock-2023-05-31"
            })
    

    modelId = 'anthropic.claude-v2'
    accept = 'application/json'
    contentType = 'application/json'

    response = boto3_bedrock.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)

    response_body = json.loads(response.get('body').read())

    responseval = response_body.get('completion')

    
    sql_chain_value = str(responseval)
    print("******* SQL Schema ******")
    print(get_schema())
    print("******* SQL QUERY ******")
    print(sql_chain_value)

    return sql_chain_value
    

def full_chain(user_query):
    
    query_value = sql_chain(user_query)
    
    run_query_val=None
    
    try:
        run_query_val= db.run(query_value)
    except:
        run_query_val = "Something went wrong" 
        

        
    # template = \
    # "Generate natural language response from SQL output given below based on the user question. Refer schema" + \
    # "\Schema: " + get_schema() + "\n" + \
    # "\nQuestion: " + user_query + "\n" + \
    # "\nSQL Output: " + run_query_val + "\n\n\n" + \
    # "Your generated Answer: "
    
    # prompt = "Human: Write a natural language response for the below user question considering table schema, SQL Query, and SQL Output given below. The response should be short and precise and you can mention list with bulletin points" + \
    # "\nSchema: " + get_schema() + "\n\nQuestion: " + user_query + "\n\nSQL Query: " + query_value + "\n\nSQL Output: " + run_query_val + "\nAssistant:"
    
    # prompt = "Human: Write a natural language response for the below user question considering table schema, SQL Query, and SQL Output given below. The response should be short and precise and you can mention list with bulletin points" + \
    # "\nSchema: " + get_schema() + "\n\nQuestion: " + user_query + "\n\nSQL Query: " + query_value + "\n\nSQL Output: " + run_query_val + "\nAssistant:"

    # prompt = "Human: Generate natural language response from SQL output for the user question. You can refer schema" + \
    # "\nSchema: " + get_schema() + "\n\nQuestion: " + user_query + "\n\nSQL Output: " + run_query_val + "\nAssistant:"
    
    # prompt = "Human: " + \
    # "\n\nUser Query: " + user_query + "\n\nSQL Output: " + run_query_val + "\nAssistant:"
    
    # prompt = "Human: Convert SQL output to natural response for the user question'" + \
    # "\nSchema: " + get_schema() + "\n\nQuestion: " + user_query + "\n\nSQL Output: " + run_query_val + "\nAssistant:"
    
    prompt = "Human: write a response to user question based on SQL output."+ \
    "\nImportant note: response should be short and precise, for list of data you can mention with bulletin points" + \
    "For Example : sampleuserquestion - Get an employee email id of Abhishek, sampleresponse - abhisek@wipro.com" + \
    "\nSchema: " + get_schema() + "\n\nQuestion: " + user_query + "\n\nSQL Query: " + query_value + "\n\nSQL Output: " + run_query_val + "\nAssistant:"
    
    body = json.dumps({"prompt": prompt,
            "max_tokens_to_sample":4096,
            "temperature":0.5,
            "top_k":250,
            "top_p":0.5,
            "stop_sequences":[],
            "anthropic_version": "bedrock-2023-05-31"
            })
    

    modelId = 'anthropic.claude-v2'
    accept = 'application/json'
    contentType = 'application/json'

    response = boto3_bedrock.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)

    response_body = json.loads(response.get('body').read())

    responseval = response_body.get('completion')

    
    full_chain_value = str(responseval)
    
    print(full_chain_value)
    
    return full_chain_value
    


def get_response(user_query, chat_history):
    return full_chain(chat_history)


# def stream_data(response_val):
#     for word in response_val.split(" "):
#         yield word + " "
#         time.sleep(0.01)
        

            
            
def testfunction(inputuser):
    return 'test app - %s' % inputuser

@app.route('/')
def exampletest():
    return "Welcome to Flask"


@app.route('/checkquery', methods=['GET', 'POST'])
def check_radar_problem_access():
    
    user_query = request.json.get('query')
    return user_query
    
    
@app.route('/successapp', methods=['GET', 'POST'])
def success():
    
    user_query = request.json.get('query')
    output_response = full_chain(user_query)
    return output_response
    # if user_query is not None and user_query != "":
        # output_response = full_chain(user_query)
    #     output_response = full_chain(user_query)
    #     # return "%s" % user_query
    #     return output_response
    # else:
    #     return "Please enter question"
    
            
# @app.route('/success/<user_query>')
# def success(user_query):
    
#     if user_query is not None and user_query != "":
#         # output_response = full_chain(user_query)
#         output_response = full_chain(user_query)
#         # return "%s" % user_query
#         return output_response
#     else:
#         return "Please enter question"
    


if __name__ == '__main__':
    
        # app.run(host='localhost.apple.com', port=5000, debug=True)
    # serve(app, host="0.0.0.0", port=8080)
    app.run()



