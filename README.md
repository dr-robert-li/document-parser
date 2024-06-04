# Document Parser with LlamaIndex and GPT-4

This Streamlit application allows users to upload various types of documents (PDF, TXT, DOC, DOCX, RTF, HTML) and query their content using LlamaIndex and OpenAI's GPT-4. The app retains the context of the conversation, allowing for follow-up questions, and references the page numbers in the responses.

## Features

- Upload and parse documents in various formats: PDF, TXT, DOC, DOCX, RTF, HTML.
- Query the content of the uploaded documents using OpenAI's GPT-4.
- Retain the context of the conversation for follow-up questions.
- Reference page numbers in the responses.
- Clear conversation history and query text field.

## Requirements

- Python 3.7 or higher
- Streamlit
- LlamaIndex
- OpenAI
- PyMuPDF
- python-docx
- html2text

## Installation

1. Clone the repository:

```bash
   git clone https://github.com/dr-robert-li/document-parser.git
   cd document-parser
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```


3. Install the required packages:

```
pip install -r requirements.txt
```

## Usage

1. Set up your OpenAI API key:
* Obtain your API key from OpenAI.
* You will need this key to use the app.

2. Run the Streamlit app:

```bash
streamlit run app.py
```

3. Open your web browser and go to http://localhost:8501 to access the app.

4. Enter your OpenAI API key in the provided input field.

5. Upload a document in one of the supported formats (PDF, TXT, DOC, DOCX, RTF, HTML).

6. Enter your query in the text input field and press Enter.

7. The app will display the response along with the page numbers referenced.

To clear the conversation history and query text field, click the "Clear History" button.

## License
This project is licensed under the MIT License.

### Acknowledgments

* Streamlit
* OpenAI
* LlamaIndex
* PyMuPDF
* python-docx
* html2text