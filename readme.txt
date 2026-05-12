I started the project on 7th May
My aim is to learn to:
how to make a database file,
make its dataframe,
read csv file using sql which is sqllite3 in python instead of the application MySql,
learn how filter data,
how to use filtered data on how to make charts,
use all and practice all functions of matplot library in python
and learn the difference between Tkinter and customTkinter


I made a screen and gave its structure, which tells the user what will the app does.
I made a button which allows the user to uplaod the file, even  if uploades does nothing.

Created the logic behind the uplaod button, loading the csv file to the database which further feeds the info to main.py
Main.py fetching the information from the db_file created makes my first chart.
Main idea is to create mutliple charts, while filetring the data into different categories of data and then making smart decision on which 
chart would be best suited for which info 

Wrote logic to detect column types automatically. Dates are detected by trying to convert them, numbers 
by using pandas built in checker, yes/no columns by checking unique values, and categories by counting unique values using nunique() — if less than 20 it 
is categorical. Based on the type, the app picks the best chart automatically.