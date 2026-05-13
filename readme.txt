Auto Analytics Dashboard
========================

A desktop data analytics application built with Python that automatically 
generates charts and insights from any CSV file uploaded by the user.

Built to learn and practice Python, SQLite, Pandas and Matplotlib in a 
real world project context.


What It Does
------------
Upload any CSV file and the app automatically detects the type of data 
in each column and generates the most suitable charts without any manual 
configuration.


How It Works
------------
When a CSV is uploaded, the app reads it into a SQLite database using 
Pandas. It then scans each column and classifies it as numeric, 
categorical, date or boolean. Based on these types, it decides which 
charts to generate and displays them in a clean dashboard.


Charts Generated
----------------
Pie Chart       - for categorical columns like department or status
Bar Chart       - shows top categories by numeric value
Line Chart      - shows income, expenses and net flow over time
Histogram       - shows distribution of numeric values
Donut Chart     - for yes/no boolean columns
Stats Table     - shows count, average, min, max and total


Tech Stack
----------
Python          - core programming language
SQLite          - local database to store uploaded CSV data
Pandas          - reads CSV files and processes data
Matplotlib      - generates all charts
CustomTkinter   - builds the desktop UI


Project Structure
-----------------
database.py     - handles all data reading, storing and SQL queries
charts.py       - handles all chart creation using Matplotlib
main.py         - builds the UI and connects everything together


How To Run
----------
1. Install dependencies
   pip install pandas matplotlib customtkinter

2. Run the app
   python main.py

3. Click Upload CSV and select any CSV file

4. Charts generate automatically


What I Learned
--------------
- How to connect Python to a SQLite database
- How to read and clean CSV data using Pandas
- How to detect data types automatically using Pandas
- How to write SQL queries to fetch and aggregate data
- How to build desktop UI using CustomTkinter
- How to embed Matplotlib charts inside a Tkinter window
- How to structure a project across multiple files


Author
------
Ashvin Shiyani
Acadia University - Computer Science
