# X-Y Data Calculator

A small Streamlit app for basic X-Y data analysis: table generation, summations, correlation and simple linear regression calculations. Created by Mohit Kumar A.

## Features
- Curve Fitting Data Calculator: generates table columns (X, Y, X², X³, X⁴, X*Y, X²*Y) and plots.
- Co-Efficient Co-relation Data Calculator: computes mean, standard deviations, correlation coefficient, regression coefficient (slope) and intercept.

## Quick start
1. Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the app:

```powershell
streamlit run "c:\Users\mohit\PycharmProjects\PythonProject2\main.py"
```

Open http://localhost:8501 in your browser if it doesn't open automatically.

## Files
- `main.py` – Streamlit application source.
- `requirements.txt` – Python dependencies.

## Contributing
If you want CI, tests, or additional features (e.g., polynomial regression fit, scatter+fit plotting), open an issue or a PR.

## License
This project is available under the MIT License. See `LICENSE` for details.
