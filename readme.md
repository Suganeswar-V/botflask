
## Usage

To run the app, you will need to have Python installed on your machine. You can install the required packages by running the following command in your terminal:

```bash
pip install -r requirements.txt
```
for python3 use pip3 in command instead of pip

To install and check the version of installed packages, use the following commands

-- pip3 install langchain
-- pip3 install langchain-openai
-- pip3 install streamlit
-- pip3 install python-dotenv
-- pip3 install mysql-connector-python

pip3 freeze | grep 'packagename'


Once you have installed the required packages, you can run the app by running the following command in your terminal:

```bash
streamlit run src/app.py
```

for python3, use command - python3 -m streamlit run src/app.py

This will start the Streamlit app, and you will be able to interact with the chatbot in your web browser.


## Contributing

This repository is intended only for educational purposes. The only contributions that will be accepted are those that fix typos or inconsistencies with the tutorial. 

## License

This repository is licensed under the MIT License. See the [LICENSE](./LICENCE.md) file for more information.