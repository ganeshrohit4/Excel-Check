# Import necessary libraries
from flask import Flask, render_template, request, send_file
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Get the uploaded files
    original_excel = request.files['original_excel']
    duplicate_excel = request.files['duplicate_excel']

    # Load data from the uploaded files
    original_df = pd.read_excel(original_excel)
    duplicate_df = pd.read_excel(duplicate_excel)

    # Remove duplicates based on the 'id' column
    cleaned_df = original_df.merge(duplicate_df[['id']], how='left', indicator=True).query('_merge == "left_only"').drop('_merge', axis=1)

    # Save the cleaned data to a new Excel file
    cleaned_df.to_excel('cleaned_excel.xlsx', index=False)

    return render_template('download.html')

@app.route('/download')
def download():
    
    # Provide the cleaned Excel file for download
    return send_file('cleaned_excel.xlsx', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
