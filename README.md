# QuickCart Assessment

QuickCart is an end-to-end data science project covering SQL analytics, MongoDB, exploratory data analysis (EDA), delivery-time regression, customer churn prediction, neural networks, LLM-based ticket triage, and an interactive Streamlit application.

## Project Repository

**GitHub:** [QuickCart Repository](https://github.com/chauhankeval33/QuickCart)

## Project Structure

```text
QuickCart/
├── app/
│   ├── models/
│   ├── pages/
│   │   ├── 1_Delivery_estimator.py
│   │   ├── 2_Churn_scorer.py
│   │   └── 3_Ticket_triage.py
│   ├── app.py
│   └── requirements.txt
├── mongo/                 # MongoDB queries
├── notebooks/             # EDA and machine learning notebooks
├── outputs/               # Generated results and evaluation outputs
├── powerbi/               # Power BI dashboard and PDF export
├── sql/                   # SQL queries
├── src/                   # Supporting Python source code
├── .streamlit/             # Streamlit configuration
├── AI_USAGE.md             # AI assistance disclosure
├── REPORT.md               # Assessment findings and written answers
├── requirements.txt        # Python dependencies
└── README.md
```

## Setup

### Prerequisites

- Python 3.11 recommended
- Git
- Assessment dataset files
- MongoDB, if running the MongoDB tasks

### Windows (PowerShell)

Run these commands from the directory where you want to store the project:

```powershell
git clone https://github.com/chauhankeval33/QuickCart.git
cd QuickCart
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

These are five setup commands, including cloning the repository. To launch the Streamlit application locally, run:

```powershell
python -m streamlit run app/app.py
```

If PowerShell blocks virtual-environment activation, use the virtual environment's Python executable directly:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app/app.py
```

### Linux / macOS

```bash
git clone https://github.com/chauhankeval33/QuickCart.git
cd QuickCart
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Run the application:

```bash
python -m streamlit run app/app.py
```

## Where the Data Goes

Place the assessment data directory named `quickcart_data/` in the repository root, alongside the `app/`, `notebooks/`, `sql/`, and `src/` directories.

Expected location:

```text
QuickCart/
├── quickcart_data/
├── app/
├── notebooks/
├── sql/
├── mongo/
└── src/
```

Use the original assessment-provided dataset files and preserve their expected filenames and directory structure. If a notebook or script expects a different location, use the path configured in that file.

The dataset is not included in the repository if excluded by `.gitignore`. Obtain the data using the instructions provided with the assessment.

## How to Run Each Part

| Part | Description | Location / Command |
|---|---|---|
| A — SQL | SQL analytics and query optimization | Run the `.sql` files in `sql/` using the database or SQL client specified by the assessment. |
| B — MongoDB | Aggregation pipelines, funnel analysis, and indexing | Run the `.js` files in `mongo/` against the configured MongoDB database. |
| C — EDA | Data quality, visualizations, and customer features | `notebooks/01_eda.ipynb` |
| D — Regression | Delivery-time prediction and model evaluation | `notebooks/02_delivery_regression.ipynb` |
| E — Churn | Customer churn classification and evaluation | `notebooks/03_churn.ipynb` |
| F — Neural Net | Neural-network training and evaluation | `notebooks/04_neural_net.ipynb` |
| G — LLM Triage | Ticket classification, prompt evaluation, and baseline comparison | Supporting code in `src/` and evaluation results in `outputs/` |
| H — Streamlit | Delivery estimator, churn scorer, and ticket triage interface | `python -m streamlit run app/app.py` |

### Running Notebooks

Activate the project virtual environment first. If Jupyter is not installed, run:

```bash
python -m pip install jupyter
python -m jupyter notebook
```

Open the required notebook from `notebooks/` and execute its cells in order.

Some tasks require the assessment dataset, database access, trained model files, or external API credentials.

## Streamlit Application

The Streamlit application includes three pages:

- **Delivery Estimator:** Predicts delivery time.
- **Churn Scorer:** Estimates customer churn.
- **Ticket Triage:** Classifies customer support tickets.

Run the application locally:

```bash
python -m streamlit run app/app.py
```

**Public application URL:** Not deployed yet.

Once deployed, replace this status with the public Streamlit Community Cloud URL.

## Power BI Dashboard

The Power BI deliverables are available in the `powerbi/` directory.

- [Power BI dashboard PDF](powerbi/quickcart.pdf)
- [Power BI dashboard file](powerbi/QuickCart.pbix)

