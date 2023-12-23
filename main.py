from flask import Flask, render_template
import pandas as pd
import numpy as np


app = Flask(__name__)

usecols = ['STAID', 'STANAME                                 ']
stations = pd.read_csv('data_small/stations.txt',
                       skiprows=17, usecols=usecols)


@app.route('/')
def home():
    return render_template('home.html', data=stations.to_html())


@app.route('/api/v1/<station>/<date>')
def about(station, date):
    try:
        filename = 'data_small/TG_STAID' + str(station).zfill(6) + '.txt'
        df = pd.read_csv(filename, skiprows=20, parse_dates=['    DATE'])
        df.columns = [column.strip() for column in df.columns]
        df['tg0'] = df['TG'].mask(df['TG']==-9999, np.nan)/10
        temperature = df.loc[df['DATE']==date]['tg0'].squeeze()
        result_dictionary = {'station': station,
                             'date': date,
                             'temperature': temperature}
        return result_dictionary
    except FileNotFoundError:
        return 'This station does not exist'


if __name__ == '__main__':
    app.run(debug=True, port=5001)