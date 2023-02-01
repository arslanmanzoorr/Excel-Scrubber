from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
import io
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def scrub_data():
    if request.method == 'POST':
        try:
            uploaded_file = request.files['file']
            # Save the uploaded file in the uploads directory
            uploaded_file.save(os.path.join('uploads', uploaded_file.filename))

            # Read the uploaded file into a pandas dataframe
            uploaded_df = pd.read_excel(os.path.join('uploads', uploaded_file.filename))

            # Read the main file into a pandas dataframe
            main_df = pd.read_excel('main_directory/main_file.xlsx')

            # Use Numpy to find the rows in the uploaded data that are not in the main data
            scrubbed_df = uploaded_df[~np.isin(uploaded_df, main_df).all(1)]

            # Write the scrubbed data to a new Excel file
            scrubbed_df.to_excel('scrubbed_data.xlsx', index=False)

            return 'Data scrubbed successfully'
        except Exception as e:
            app.logger.error(e)
            return 'An error occurred during data scrubbing'
    return render_template('index.html')

if __name__ == '__main__':
    app.run()