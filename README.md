## Use the virtual env with all packages installed

### MacOS: <br>

```
source env/bin/activate
```

### Windows (should work?):

```
env/bin/activate
```

## Alternatively, install packages yourself

```
pip install -r requirements.txt
```

<br>

## Run the app:

This should open a new tab in your browser with the app

```
streamlit run assistant-gpt.py
```

## Use your API Keys:

Add secrets to file named `secrets.toml` in a folder named `.streamlit` in the root directory of the project.

```
openai_api_key = "YOUR_OPEN_AI_KEY"
azure_key = "YOUR_AZURE_KEY"
azure_region = "YOUR_AZURE_REGION"
```
