import sqlite3
import pandas as pd

conn = sqlite3.connect("cells.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS cell(
    sample TEXT PRIMARY KEY,
    project TEXT,
    subject TEXT,
    condition TEXT,
    age INTEGER,
    sex TEXT,
    treatment TEXT,
    response TEXT,
    sample_type TEXT,
    time_from_treatment_start INTEGER,
    b_cell INTEGER,
    cd8_t_cell INTEGER,
    cd4_t_cell INTEGER,
    nk_cell INTEGER,
    monocyte INTEGER
)
""")


conn.commit()


df = pd.read_csv("cell-count.csv")
# load cell-count.csv into the database
for _, row in df.iterrows():
    cursor.execute("""
    INSERT INTO cell (
        sample,
        project,
        subject,
        condition,
        age,
        sex,
        treatment,
        response,
        sample_type,
        time_from_treatment_start,
        b_cell,
        cd8_t_cell,
        cd4_t_cell,
        nk_cell,
        monocyte
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        row["sample"],
        row["project"],
        row["subject"],
        row["condition"],
        int(row["age"]),
        row["sex"],
        row["treatment"],
        row["response"],
        row["sample_type"],
        int(row["time_from_treatment_start"]),
        int(row["b_cell"]),
        int(row["cd8_t_cell"]),
        int(row["cd4_t_cell"]),
        int(row["nk_cell"]),
        int(row["monocyte"])
    ))

conn.commit()
conn.close()
print("Cell table created")