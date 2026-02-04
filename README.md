# CubeSat-Anomaly-MLOps-Mission-Control

A real-time monitoring and anomaly detection system for satellite telemetry. This project integrates a Python-based Data Producer, a Scikit-Learn Machine Learning Pipeline, Firebase Real-Time Database, and an MLflow Audit Layer, all visualized through a multi-page Streamlit Dashboard.

**Critical: Security & Firebase Setup**

The repository lacks a service_account.json file because users need to create the file themselves. The file contains private keys which need to be protected because they provide unauthorized access to your database.

**How to get your key:**

i. Access the Firebase Console.

ii. Proceed to Project Settings > Service Accounts section.

iii. Select Generate New Private Key option.

iv. You need to rename the downloaded file as service_account.json and then move it to the main directory of the project.

v. You must add service_account.json to your .gitignore file to protect your private keys from being exposed on GitHub.

**Project Directory**

i. **Root Directory:** sensor-anomaly-mlops The top-level folder contains your core execution scripts, configuration files, and environment settings.

ii. **Configuration & Security**

a. config.py: Central configuration for Firebase URLs and global settings.

b. service_account.json: (Critical) Your private Firebase credentials file.

c. .venv/: Your Python virtual environment folder.

iii. **Core Logic & AI Brain**

a. ml_engine.py: Defines the Isolation Forest model logic.

b. feature_processor.py: Handles rolling math and telemetry data cleaning.

c.ml_orchestrator.py: The automation script that retrains the AI every 30 seconds.

iv. **Data & Orchestration**

a. mock_telemetry.py: The satellite simulator pushing data to Firebase.

b. dockfile-compose.yml: Script for containerized deployment.

c. mlflow.db: The SQLite database tracking your model audit history.

d.requirements.txt: List of all required Python libraries.

v. Sub-Directories pages/: Contains the individual modules for your multi-page dashboard:

a. mission_control.py: Live telemetry and health gauges.

b. cluster_analysis.py: 3D visualization of anomaly detection.

c. mlops_lineage.py: MLflow training trend and audit logs.

d. data_explorer.py: Historical data ledger and CSV export.

e. models/: Stores the generated .pkl AI model files.

f.mlruns/: Default directory for MLflow tracking metadata.

vi. Entry Point

a. dashboard.py: The main file you run (streamlit run dashboard.py) to launch the UI and route between the different pages.

**Mission Launch Sequence**
To run the full stack, open four separate terminal windows and execute the following in order:

Terminal 1 (Installation Instructions):
You must execute the following commands into your terminal because they will guarantee proper operation of your virtual environment.

Activate your environment:

                       .\.venv\Scripts\activate
Install the requirements:

                      pip install -r requirements.txt
Terminal 2 (Data):

                python mock_telemetry.py
Terminal 3 (AI Brain):

                   python ml_orchestrator.py
Terminal 4 (Audit):

                  mlflow ui --port 5000
Terminal 5 (Mission Control UI):

                              streamlit run dashboard.py
**Dashboard Modules**

i. Live Status: The system provides both real-time altitude measurement and signal strength monitoring capabilities.

ii. 3D Clusters: Users can explore the AI detection area through an interactive Plotly 3D visualization.

iii. Model Audit: The high-resolution line graphs display MLOps training frequency according to MLflow data which shows training occurrence throughout the entire monitoring period.

iv. System Ledger: The system provides a historical data browser which allows users to export data in CSV format.

**Troubleshooting**

i. Refused to Connect: Users should attempt to load the dashboard using the alternative port streamlit run dashboard.py --server.port 8080 when the current port fails to display the dashboard.

ii. "Nothing" in Graphs: The graphing function requires ml_orchestrator.py to run because it creates models while recording their execution into MLflow.

![Dashboard2](https://github.com/user-attachments/assets/7a892177-40f9-476d-be1f-d6129eeab528)
