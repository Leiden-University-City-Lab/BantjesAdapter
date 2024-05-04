import dash
from dash import dcc, html, Input, Output, State
import json

# Sample JSON data
sample_json_data = {
  "first_name": "Joannes",
  "last_name": "LE FRANCA VAN BERKHEY",
  "birth_date": "23-01-1729",
  "birth_place": "Leiden",
  "death_date": "13-03-1812",
  "death_place": "Leiden",
  "education": [
    {
      "study": "School",
      "location": "Katwijk",
      "date": "1741",
      "source": "3,41"
    },
    {
      "study": "Stud. Leiden",
      "location": "Leiden",
      "date": "22-09-1747",
      "source": "14"
    },
    {
      "study": "Doct.Med. LLeiden",
      "location": None,
      "date": "12-12-1760",
      "source": "15"
    },
    {
      "study": "Stud.",
      "location": "Leiden",
      "date": "02-06-1764",
      "source": "14"
    }
  ],
  # More JSON data...
}

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    # Dropdown to select JSON file
    dcc.Dropdown(
        id='json-file-dropdown',
        options=[
            {'label': 'File 1', 'value': 'file1.json'},
            {'label': 'File 2', 'value': 'file2.json'},
            # Add more options for each JSON file in the directory
        ],
        value=None,
        placeholder="Select a JSON file",
        clearable=False
    ),
    # Textarea to display JSON data
    dcc.Textarea(id='json-textarea', style={'width': '100%', 'height': '300px'}),
    # Button to save changes
    html.Button('Save Changes', id='save-button', n_clicks=0),
    # Output for save confirmation message
    html.Div(id='save-confirm')
])

# Callback to update the textarea with JSON data when a file is selected
@app.callback(
    Output('json-textarea', 'value'),
    [Input('json-file-dropdown', 'value')]
)
def update_json_textarea(selected_file):
    if selected_file is not None:
        with open(selected_file, 'r') as file:
            data = json.load(file)
        return json.dumps(data, indent=4)

# Callback to save changes to the selected JSON file
@app.callback(
    Output('save-confirm', 'children'),
    [Input('save-button', 'n_clicks')],
    [State('json-file-dropdown', 'value'),
     State('json-textarea', 'value')]
)
def save_changes(n_clicks, selected_file, json_data):
    if n_clicks > 0 and selected_file is not None:
        with open(selected_file, 'w') as file:
            file.write(json_data)
        return html.Div('Changes saved successfully!')

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
