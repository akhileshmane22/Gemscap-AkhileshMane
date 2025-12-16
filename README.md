Real-Time Pair Trading Analytics

A Python + Streamlit app that ingests live crypto ticks from Binance Futures and visualizes pair-trading analytics such as hedge ratio, spread, z-score, ADF test, and rolling correlation. Data is stored locally in SQLite (ticks.db).

Features
- Live tick ingestion for btcusdt, ethusdt, bnbusdt from Binance Futures websocket
- Local storage in SQLite with a simple schema
- Streamlit dashboard to select symbols and visualize:
	- Prices and spreads
	- Hedge ratio via OLS
	- Rolling z-score
	- ADF stationarity test
	- Rolling correlation
- Basic z-score alert helper
- CSV export from the UI

Project Structure
- ingest.py: Async websocket client that writes ticks into ticks.db
- app.py: Streamlit UI for interactive analytics and visualization
- analytics.py: Statistical utilities (OLS hedge ratio, spread, z-score, ADF, rolling correlation)
- storage.py: SQLite data loading and resampling helpers
- alerts.py: Simple alert check based on z-score threshold
- schema.sql: Table DDL for ticks
- requirements.txt: Python dependencies
- .gitignore: Excludes virtual envs, caches, and ticks.db

Requirements
- Python 3.9+
- Internet access (Binance Futures websocket)
- Windows, macOS, or Linux

Quick Start
1) Create and activate a virtual environment, then install dependencies.

Windows (PowerShell):
```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2) Initialize the database (optional; it is created on first write).
See schema.sql:
```sql
CREATE TABLE IF NOT EXISTS ticks (
		symbol TEXT,
		timestamp TIMESTAMP,
		price REAL,
		qty REAL
);
```

3) Start the ingestor (Terminal 1):
```powershell
py ingest.py
```

4) Start the Streamlit app (Terminal 2):
```powershell
streamlit run app.py
```

5) Open the browser link Streamlit prints (default http://localhost:8501). Choose symbols and window; charts update as trades arrive.

Useful Commands
- Verify data is flowing into SQLite:
```powershell
py -c "import sqlite3; c=sqlite3.connect('ticks.db'); print(c.execute('select count(*) from ticks').fetchone()); c.close()"
```

- Change Streamlit port if 8501 is busy:
```powershell
streamlit run app.py --server.port 8502
```

Notes & Caveats
- Binance websocket requires stable internet; brief disconnects may occur.
- Symbols should be lowercase (e.g., btcusdt).
- ticks.db is excluded by .gitignore to avoid committing local data.
- Educational project; not for live trading without proper risk controls.

License
Proprietary. All rights reserved.

