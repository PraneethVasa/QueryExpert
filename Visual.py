import streamlit as st
from dotenv import load_dotenv
import os
import mysql.connector
import pandas as pd
import google.generativeai as genai
import matplotlib.pyplot as plt

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("API"))

# Connect to MySQL and execute query
def read_db(sql):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ems"
        )
        cur = conn.cursor()
        cur.execute(sql)
        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return pd.DataFrame(rows, columns=columns)
    except Exception as e:
        return f"❌ DB Error: {e}"

# Validate SQL query
def validate_query(sql):
    blocked_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'TRUNCATE']
    upper_sql = sql.upper()
    for keyword in blocked_keywords:
        if keyword in upper_sql:
            return f"❌ Blocked dangerous SQL keyword detected: `{keyword}`"
    return "VALID"

# Gemini response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    res = model.generate_content([prompt, question])
    return res.text.strip()

# Prompt
def get_base_prompt():
    return """
You are an expert in converting natural language questions into MySQL SQL queries.
Given a user's question and the database schema below, generate the correct SQL query.

Always use the correct column names and respect data types.
Use filters based on given data examples when possible.
Do not add any explanation or formatting.
Just return the SQL query as plain text.

Database Schema:
Table: sales
- sale_id: INT, PRIMARY KEY, AUTO_INCREMENT
- customer_name: VARCHAR(255)
- customer_email: VARCHAR(255)
- customer_phone: VARCHAR(20)
- product_name: VARCHAR(255)
- category: VARCHAR(255)
- quantity: INT
- unit_price: DOUBLE
- total_price: DOUBLE
- sale_date: DATE
- payment_method: VARCHAR(50)
- store_location: VARCHAR(255)
- salesperson_id: INT

Examples:
Input: Show all sales records.
Output: SELECT * FROM sales;
Input: What is the total revenue from Electronics category?
Output: SELECT SUM(total_price) FROM sales WHERE category = 'Electronics';
Input: Show total revenue by store location.
Output: SELECT store_location, SUM(total_price) AS total_revenue FROM sales GROUP BY store_location;
"""

# Refine on error
def refine_sql_on_error(original_question, failed_query, error_msg, attempts=5):
    retry_prompt = get_base_prompt() + f"""
The previous SQL query failed.
Original Question: {original_question}
Previous SQL: {failed_query}
Error: {error_msg}
Return only the corrected SQL query.
"""
    for attempt in range(attempts):
        refined_query = get_gemini_response(original_question, retry_prompt)
        validation = validate_query(refined_query)
        if validation != "VALID":
            return refined_query, validation
        result = read_db(refined_query)
        if isinstance(result, pd.DataFrame):
            return refined_query, result
        else:
            retry_prompt += f"\nAttempt {attempt+1} failed: {result}\n"
    return failed_query, result

# Streamlit UI
st.set_page_config(page_title="Text-to-SQL Chatbot - Sales DB")
st.title("Text-to-SQL Chatbot - Sales DB")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.chat_input("Ask something like: 'Show revenue by store location'")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    sql_query = get_gemini_response(user_input, get_base_prompt())
    validation = validate_query(sql_query)
    if validation != "VALID":
        result_data = validation
    else:
        result_data = read_db(sql_query)
    if isinstance(result_data, str) and result_data.startswith("❌"):
        sql_query, result_data = refine_sql_on_error(user_input, sql_query, result_data)
    st.session_state.messages.append({"role": "bot", "content": sql_query})

for msg in st.session_state.messages:
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        if msg["role"] == "bot":
            st.markdown(f"**SQL:** `{msg['content']}`")
            validation = validate_query(msg['content'])
            if validation != "VALID":
                st.error(validation)
            else:
                result_df = read_db(msg['content'])
                if isinstance(result_df, str):
                    st.error(result_df)
                elif result_df.empty:
                    st.warning("No results found.")
                else:
                    st.dataframe(result_df, use_container_width=True)

                    # Visualization logic
                    try:
                        if result_df.shape[1] == 2:
                            x_col, y_col = result_df.columns
                            if pd.api.types.is_numeric_dtype(result_df[y_col]):
                                st.markdown("### 📊 Visualization")
                                chart_type = "bar"
                                if "date" in x_col.lower() or "time" in x_col.lower():
                                    chart_type = "line"
                                elif result_df[y_col].nunique() <= 10:
                                    chart_type = "pie"

                                if chart_type == "bar":
                                    st.bar_chart(result_df.set_index(x_col))
                                elif chart_type == "line":
                                    st.line_chart(result_df.set_index(x_col))
                                elif chart_type == "pie":
                                    fig, ax = plt.subplots()
                                    ax.pie(result_df[y_col], labels=result_df[x_col], autopct='%1.1f%%')
                                    ax.set_title(f"{y_col} by {x_col}")
                                    st.pyplot(fig)
                    except Exception as e:
                        st.warning(f"Could not generate chart: {e}")
        else:
            st.markdown(msg["content"])

