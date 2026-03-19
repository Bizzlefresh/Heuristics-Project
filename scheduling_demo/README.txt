Scheduling Demo - Streamlit App

Files:
- app.py
- pages/1_Configure_Jobs.py
- pages/2_Run_Demo.py
- pages/3_Results_and_Comparison.py
- utils/scheduler_core.py
- utils/visuals.py
- requirements.txt

How to run locally:
1. Open terminal in this folder.
2. Install requirements:
   pip install -r requirements.txt
3. Start the app:
   streamlit run app.py

Recommended presentation flow:
1. Open Configure Jobs.
2. Select configuration and seed.
3. Click Generate Job Set.
4. Open Run Demo and run one algorithm live.
5. Open Results & Comparison to show all metrics and the best algorithm.

Notes:
- Nothing runs automatically before Generate Job Set.
- The app uses the same project configurations as the original report:
  Configuration 1 = 20 jobs, 3 machines
  Configuration 2 = 50 jobs, 3 machines
  Configuration 3 = 50 jobs, 5 machines
