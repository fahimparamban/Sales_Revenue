import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------
# 1. Load dataset from Excel
# -------------------------
excel_file = "Retail_Sales_Data.xlsx"
df_excel = pd.read_excel(excel_file)

# Ensure column names match the table schema
# Expected columns: Date, Product, Category, Region, Sales Amount, Quantity Sold
df_excel.columns = [col.strip().lower().replace(" ", "_") for col in df_excel.columns]

# -------------------------
# 2. Create database & connect
# -------------------------
conn = sqlite3.connect("sales_data.db")
cursor = conn.cursor()

# -------------------------
# 3. Create sales table
# -------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    product TEXT NOT NULL,
    category TEXT NOT NULL,
    region TEXT NOT NULL,
    sales_amount REAL NOT NULL,
    quantity_sold INTEGER NOT NULL
)
""")

# -------------------------
# 4. Insert data from Excel
# -------------------------
df_excel.to_sql("sales", conn, if_exists="replace", index=False)

# -------------------------
# 5. Run SQL query
# -------------------------
query = """
SELECT 
    product, 
    SUM(quantity_sold) AS total_qty, 
    SUM(sales_amount) AS revenue
FROM sales
GROUP BY product
"""
df_summary = pd.read_sql_query(query, conn)

# -------------------------
# 6. Close connection
# -------------------------
conn.close()

# -------------------------
# 7. Print results
# -------------------------
print(df_summary)

# -------------------------
# 8. Plot bar chart
# -------------------------
df_summary.plot(kind='bar', x='product', y='revenue', legend=False, color='skyblue')
plt.title("Revenue by Product")
plt.xlabel("Product")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig("sales_chart.png", dpi=300)
plt.show()

