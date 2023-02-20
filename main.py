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


def drug_delete(Did):
    c.execute(''' DELETE FROM Drugs WHERE D_id = ?''', (Did,))
    conn.commit()

def drug_create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS Drugs(
                D_Name VARCHAR(50) NOT NULL,
                D_ExpDate DATE NOT NULL, 
                D_Use VARCHAR(50) NOT NULL,
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


    st.title("Pharmacy Database Dashboard")
    menu = ["Drugs", "Orders"]
    choice = st.sidebar.selectbox("Menu", menu)



    ## DRUGS
    if choice == "Drugs":

        menu = ["Add", "View", "Update", "Delete"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "Add":
            with st.form(key='add_drug_form'):
                st.subheader("Add Drugs")

                col1, col2 = st.columns(2)

                with col1:
                    drug_name = st.text_input("Enter the Drug Name")
                    drug_expiry = st.date_input("Expiry Date of Drug (YYYY-MM-DD)")
                    drug_mainuse = st.text_input("When to Use")
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

            drug_clean_df = pd.DataFrame(drug_result, columns=["Name", "Expiry Date", "Use", "Quantity","price" "ID"])
            drug_clean_df.index+=1
            st.table(drug_clean_df)



        if choice == 'Update':
            with st.form(key='update_drug_form'):
                st.subheader("Update Drugs")

                col1, col2 = st.columns(2)

                with col1:
                    drug_name = st.text_input("Enter the Drug Name")
                    drug_expiry = st.date_input("Expiry Date of Drug (YYYY-MM-DD)")
                    drug_mainuse = st.text_input("When to Use")
                with col2:
                    drug_quantity = st.text_input("Enter the quantity")
                    drug_price = st.text_input("Enter the price")
                    drug_id = st.text_input("Enter the Drug id (example:#D1)")

                if st.form_submit_button("Update Drug"):
                    drug_update(drug_name,drug_expiry,drug_mainuse,drug_quantity,drug_price,drug_id)
                    st.success("Successfully Added Data")
        if choice == 'Delete':
            st.subheader("Delete Drugs")
            did = st.text_input("Drug ID")
            if st.button(label="Delete"):
                drug_delete(did)

if __name__ == '__main__':
    drug_create_table()
    admin()
