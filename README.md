# QueryExpert - AI-Powered Text-to-SQL Chatbot

## Overview
QueryExpert is an AI-powered Text-to-SQL chatbot that allows users to interact with a MySQL database using natural language queries. Leveraging **Google Gemini Gen API, Streamlit, and Python**, it translates user prompts into SQL queries, executes them, and returns results in a structured format. Additionally, it supports **data visualization** for enhanced insights.

## Features
- 🔹 **Natural Language to SQL** – Converts user prompts into MySQL queries using LLMs.
- 🔹 **Automated Query Execution** – Executes generated queries on a MySQL database.
- 🔹 **Query Validation & Error Handling** – Detects and blocks unsafe SQL commands.
- 🔹 **Auto-Correction on Failure** – Refines and retries queries up to 5 times.
- 🔹 **Data Visualization** – Generates **bar, line, and pie charts** for numerical data.

## Technologies Used
- **Google Gemini Gen API** – AI-powered natural language processing
- **Streamlit** – Interactive UI for chatbot functionality
- **Python** – Backend development and database interaction
- **MySQL** – Database for query execution
- **Matplotlib & Pandas** – Data processing and visualization

## Installation
```bash
# Clone the repository
git clone https://github.com/YourRepo/QueryExpert.git
cd QueryExpert

# Create a virtual environment and install dependencies
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env  # Add your Gemini API key in the .env file

# Run the Streamlit app
streamlit run app.py
```

## Usage
1. **Start the chatbot** using the command `streamlit run app.py`.
2. **Ask a question**, e.g., *"Show total revenue by store location"*.
3. The chatbot **converts** the prompt into an SQL query.
4. The **query executes**, and the result is displayed.
5. If applicable, a **graph is generated** based on the results.

## Example Queries & Outputs
| User Prompt | Generated SQL Query |
|------------|----------------------|
| *"Show all sales records."* | `SELECT * FROM sales;` |
| *"Total revenue from Electronics?"* | `SELECT SUM(total_price) FROM sales WHERE category = 'Electronics';` |
| *"Sales by store location?"* | `SELECT store_location, SUM(total_price) AS total_revenue FROM sales GROUP BY store_location;` |

## Screenshots
(Include relevant screenshots of the UI and visualizations)

## Contribution
1. Fork the repository & clone locally.
2. Create a feature branch: `git checkout -b feature-name`.
3. Commit changes: `git commit -m "Added feature-name"`.
4. Push to the branch: `git push origin feature-name`.
5. Open a Pull Request.

## License
This project is licensed under the MIT License.

---
**Author:** Praneeth Vasa  
GitHub: [github.com/YourRepo](https://github.com/YourRepo/QueryExpert)  
LinkedIn: [linkedin.com/in/YourProfile](https://linkedin.com/in/YourProfile)
