from langchain.tools import tool

@tool
def get_helpdesk_info(query: str) -> str:
    """
    Execute a SQL query on the tickets table and return the results.
    Input must be a valid SQL query string, not a natural language question.
    """

    #db is db/helpdesk.db
    #write code to connect to the sqlite db and fetch the required information based on the query
    import sqlite3
    conn = sqlite3.connect('db/helpdesk.db')
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return str(result)