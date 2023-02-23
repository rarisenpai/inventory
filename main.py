import streamlit as st
import pandas as pd
## SQL DATABASE CODE
import sqlite3

st. set_page_config(layout="wide")
conn = sqlite3.connect("drug_data.db",check_same_thread=False)
c = conn.cursor()

def drug_update(drug_name, drug_expiry, drug_mainuse, drug_quantity,drug_price, drug_id):
    c.execute('''
        UPDATE Drugs 
        SET D_Name = ?, D_ExpDate = ?, D_Use = ?,D_price=?, D_Qty = ?
        WHERE D_id = ?
    ''', (drug_name, drug_expiry, drug_mainuse, drug_quantity,drug_price, drug_id))
    conn.commit()

def clear_sales():
    c.execute('''
    DROP TABLE sales
    ''')
    conn.commit()

def clear_drugs():
    c.execute('''
    DROP TABLE drugs
    ''')
    conn.commit()

def create_sales_table():
    # create the sales table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS sales
                 (date TEXT, item TEXT, quantity INTEGER, price REAL, total REAL)''')
    
def record_sale(date, item, quantity, price):
    # calculate the total price
    total = int(quantity) * int(price)
    
    # insert the sale into the database
    c.execute("INSERT INTO sales VALUES (?, ?, ?,?)", (date, item, quantity, price, total))
    
    # commit the transaction
    conn.commit()

def export_sales(filename):
    # execute the query and read the results into a dataframe
    df = pd.read_sql('SELECT * FROM sales', conn)

    # create a download button for the CSV file
    csv = df.to_csv(index=False)
    return csv
            

def sales_view_all_data(search_term=None):
    if search_term:
        c.execute("SELECT * FROM sales WHERE item LIKE ?", ('%' + search_term + '%',))
    else:
        c.execute('SELECT * FROM sales')
    sales_data = c.fetchall()
    return sales_data

def update_sales(drug_id, drug_quantity):
    c.execute('''SELECT D_Qty from Drugs where D_id = ?''', (drug_id,))
    result = c.fetchone()
    if result is not None:
        drug_value = result[0]
        # calculate new value of drug quantity
        new_value = int(drug_value) - int(drug_quantity)
        # update drug quantity in database
        c.execute("UPDATE drugs SET D_Qty=? WHERE D_id=?", (new_value, drug_id))
        conn.commit()
    else:
        st.error("No drug found with ID:", drug_id)

def drug_delete(Did):
    c.execute(''' DELETE FROM Drugs WHERE D_id = ?''', (Did,))
    conn.commit()

def drug_create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS Drugs(
                D_Name VARCHAR(50) NOT NULL,
                D_ExpDate DATE NOT NULL, 
                D_Use INT NOT NULL,
                D_Qty INT NOT NULL, 
                D_Price INT NOT NULL,
                D_id INT PRIMARY KEY NOT NULL
                )
                ''')
    print('DRUG Table create Successfully')

def drug_add_data(Dname, Dexpdate, Duse, Dqty, Dprice,Did):
    c.execute('''INSERT INTO Drugs (D_Name, D_Expdate, D_Use, D_Qty, D_price,D_id) VALUES(?,?,?,?,?,?)''', (Dname, Dexpdate, Duse,Dqty,Dprice, Did))
    conn.commit()

def drug_view_all_data(search_term=None):
    if search_term:
        c.execute("SELECT * FROM Drugs WHERE D_Name LIKE ?", ('%' + search_term + '%',))
    else:
        c.execute('SELECT * FROM Drugs')
    drug_data = c.fetchall()
    return drug_data

def admin():
    st.title("Wellrose Pharmacy Dashboard")
    menu = ["Drugs"]
    st.sidebar.selectbox("Menu",menu)
    menu = ["Add", "View", "Update", "Delete", "Sales","View sales"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Add":
        with st.form(key='add_drug_form'):
            st.subheader("Add Drugs")

            col1, col2 = st.columns(2)

            with col1:
                drug_name = st.text_input("Enter the Drug Name")
                drug_expiry = st.date_input("Expiry Date of Drug (YYYY-MM-DD)")
                drug_mainuse = st.text_input("Milligrams")
            with col2:
                drug_quantity = st.text_input("Enter the quantity")
                drug_price = st.text_input("Enter the price")
                drug_id = st.text_input("Enter the Drug id (example:#D1)")

            if st.form_submit_button("Add Drug"):
                drug_add_data(drug_name,drug_expiry,drug_mainuse,drug_quantity,drug_price, drug_id)
                st.success("Successfully Added Data")
    if choice == "View":
        st.subheader("Drug Details")

        search_term = st.text_input("Search for a drug by name")
        search = st.checkbox("Search")
        if search:
            drug_result = drug_view_all_data(search_term)
        else:
            drug_result = drug_view_all_data()

        drug_clean_df = pd.DataFrame(drug_result, columns=["Name", "Expiry Date", "Milligrams", "Quantity","price" ,"ID"])
        drug_clean_df.index+=1
        st.table(drug_clean_df)
        if st.button('Clear drugs'):
            clear_drugs()



    if choice == 'Update':
        with st.form(key='update_drug_form'):
            st.subheader("Update Drugs")

            col1, col2 = st.columns(2)

            with col1:
                drug_name = st.text_input("Enter the Drug Name")
                drug_expiry = st.date_input("Expiry Date of Drug (YYYY-MM-DD)")
                drug_mainuse = st.text_input("Milligrams")
            with col2:
                drug_quantity = st.text_input("Enter the quantity")
                drug_price = st.text_input("Enter the price")
                drug_id = st.text_input("Enter the Drug id (example:#D1)")

            if st.form_submit_button("Update Drug"):
                drug_update(drug_name,drug_expiry,drug_mainuse,drug_quantity,drug_price,drug_id)
                st.success("Successfully Updated Data")

    if choice == 'Delete':
        st.subheader("Delete Drugs")
        did = st.text_input("Drug ID")
        if st.button(label="Delete"):
            drug_delete(did)
            st.success("Successfully Deleted Data")
            
    if choice == 'Sales':
        with st.form(key='sell_drug_form'):
            st.subheader('make sales')
            col1, col2 = st.columns(2)

            with col1:
                drug_id = st.text_input("Enter the Drug id")
                date = st.date_input("Date of sale (YYYY-MM-DD)")
                item = st.text_input("Enter the Drug name")
            with col2:
                drug_quantity = st.text_input("Enter the number sold:")
                price = st.text_input('Enter price')
        
            if st.form_submit_button("Sell Drug"):
                update_sales(drug_id,drug_quantity)
                record_sale(date, item, drug_quantity, price)
                st.success("Successfully sold Data")  

    if choice == "View sales":
        st.subheader("sales Details")

        search_term = st.text_input("Search for sales")
        search = st.checkbox("Search")
        if search:
            sales_result = sales_view_all_data(search_term)
        else:
            sales_result = sales_view_all_data()
        sales_clean_df = pd.DataFrame(sales_result, columns=["date", "item", "drug_quantity", "price"])
        sales_clean_df.index+=1
        st.table(sales_clean_df)
        csv = export_sales('sale')
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='sales.csv',
        )
        if st.button('Clear sales'):
            clear_sales()


if __name__ == '__main__':
    drug_create_table()
    create_sales_table()
    admin()
