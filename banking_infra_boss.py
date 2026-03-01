import streamlit as st
import sqlite3
import random

conn = sqlite3.connect("bank.db", check_same_thread=False)
c = conn.cursor()

# ---------- DATABASE ----------
c.execute("CREATE TABLE IF NOT EXISTS atm(id INTEGER PRIMARY KEY, status TEXT, cash INTEGER)")
c.execute("CREATE TABLE IF NOT EXISTS wallet(id INTEGER PRIMARY KEY, name TEXT, balance INTEGER)")
c.execute("CREATE TABLE IF NOT EXISTS loan(id INTEGER PRIMARY KEY, name TEXT, amount INTEGER, status TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS expense(id INTEGER PRIMARY KEY, item TEXT, cost INTEGER)")
conn.commit()

st.title("🏦 Finance & Banking IT Infrastructure Management System")

menu = ["ATM Monitoring","Digital Wallet","Loan Management","Expense Tracker","Fraud Detection","Infrastructure"]
choice = st.sidebar.selectbox("Select Module",menu)

# ================= ATM MONITORING =================
if choice == "ATM Monitoring":
    st.header("🏧 ATM Monitoring System")

    if st.button("Add ATM"):
        c.execute("INSERT INTO atm(status,cash) VALUES('Online',50000)")
        conn.commit()
        st.success("ATM Added")

    st.subheader("Update ATM Status")
    atm_id = st.number_input("ATM ID", min_value=1)
    status = st.selectbox("Status",["Online","Offline"])
    cash = st.number_input("Cash Available")

    if st.button("Update ATM"):
        c.execute("UPDATE atm SET status=?, cash=? WHERE id=?", (status,cash,atm_id))
        conn.commit()
        st.success("ATM Updated")

    data = c.execute("SELECT * FROM atm").fetchall()
    st.table(data)

# ================= DIGITAL WALLET =================
elif choice == "Digital Wallet":
    st.header("💳 Digital Wallet System")

    name = st.text_input("User Name")

    col1,col2,col3 = st.columns(3)

    with col1:
        amount = st.number_input("Add Money")
        if st.button("Add"):
            c.execute("INSERT INTO wallet(name,balance) VALUES(?,?)",(name,amount))
            conn.commit()
            st.success("Money Added")

    with col2:
        send = st.number_input("Send Money")
        if st.button("Send"):
            c.execute("UPDATE wallet SET balance=balance-? WHERE name=?",(send,name))
            conn.commit()
            st.success("Money Sent")

    with col3:
        if st.button("Check Balance"):
            data = c.execute("SELECT balance FROM wallet WHERE name=?",(name,)).fetchone()
            if data:
                st.info(f"Balance: ₹{data[0]}")

    data = c.execute("SELECT * FROM wallet").fetchall()
    st.table(data)

# ================= LOAN MANAGEMENT =================
elif choice == "Loan Management":
    st.header("🏦 Loan Management System")

    name = st.text_input("Applicant Name")
    amount = st.number_input("Loan Amount")

    if st.button("Apply Loan"):
        c.execute("INSERT INTO loan(name,amount,status) VALUES(?,?,?)",(name,amount,"Pending"))
        conn.commit()
        st.success("Loan Applied")

    st.subheader("Approve / Reject Loan")
    loan_id = st.number_input("Loan ID", min_value=1)
    decision = st.selectbox("Decision",["Approved","Rejected"])

    if st.button("Update Loan"):
        c.execute("UPDATE loan SET status=? WHERE id=?",(decision,loan_id))
        conn.commit()
        st.success("Loan Updated")

    st.subheader("Track Loan Status")
    track_id = st.number_input("Enter Loan ID", min_value=1, key="track")
    if st.button("Check Status"):
        data = c.execute("SELECT status FROM loan WHERE id=?",(track_id,)).fetchone()
        if data:
            st.info(f"Loan Status: {data[0]}")

    data = c.execute("SELECT * FROM loan").fetchall()
    st.table(data)

# ================= EXPENSE TRACKER =================
elif choice == "Expense Tracker":
    st.header("📊 Expense Tracker")

    item = st.text_input("Expense Item")
    cost = st.number_input("Cost")

    if st.button("Add Expense"):
        c.execute("INSERT INTO expense(item,cost) VALUES(?,?)",(item,cost))
        conn.commit()
        st.success("Expense Added")

    data = c.execute("SELECT * FROM expense").fetchall()
    st.table(data)

# ================= FRAUD DETECTION =================
elif choice == "Fraud Detection":
    st.header("🚨 Fraud Detection")

    amount = st.number_input("Transaction Amount")

    if st.button("Check Transaction"):
        if amount > 100000:
            st.error("⚠️ Fraud Alert!")
        else:
            st.success("Transaction Safe")

# ================= INFRASTRUCTURE =================
elif choice == "Infrastructure":
    st.header("🖥️ IT Infrastructure Monitoring")

    cpu = random.randint(20,90)
    ram = random.randint(30,95)

    st.write("CPU Usage:",cpu,"%")
    st.write("RAM Usage:",ram,"%")

    if cpu > 80 or ram > 85:
        st.error("⚠️ System Overload")
    else:
        st.success("System Healthy")