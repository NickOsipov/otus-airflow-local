"""
Module
"""

import sqlite3
import pandas as pd

conn = sqlite3.connect("./data/example.db")

print(pd.read_sql("SELECT * FROM dag_testing_table", conn))