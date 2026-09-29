import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Smart Expense Analyzer")
st.write("Hello! Let's analyse your expenses.")
st.write("Please provide your financial data in the tables given below:")

# Income & Budget table
data_f = pd.DataFrame({"Monthly income":[0],"Budget":[0]})
edited_dataf = st.data_editor(data_f)

# Expense table
financial_data = {
"Expense Categories":["Housing and Utilities","Food and Groceries","Education and Healthcare",
"Transportation","Entertainment and Dine out","Maid or Service Staff","Clothing and Cosmetics",
"Investments","Loans or EMI's"],
"Amount":[0]*9
}

edited_dataframe = st.data_editor(pd.DataFrame(financial_data))

if st.button("Analyze"):

    total_expense = edited_dataframe["Amount"].sum()
    budget = edited_dataf["Budget"][0]
    income = edited_dataf["Monthly income"][0]

    # Result
    if total_expense <= budget:
        savings = income - total_expense
        st.table(pd.DataFrame({"Total Expense":[total_expense],"Savings":[savings]}))
    else:
        st.table(pd.DataFrame({"Total Expense":[total_expense]}))
        st.markdown("**You have exceeded your budget!**")

    filt_dataframe = edited_dataframe[edited_dataframe["Amount"]>0]

    if not filt_dataframe.empty:

        category_colors={
        "Housing and Utilities":"red","Food and Groceries":"blue","Education and Healthcare":"green",
        "Transportation":"orange","Entertainment and Dine out":"purple","Maid or Service Staff":"pink",
        "Clothing and Cosmetics":"cyan","Investments":"yellow","Loans or EMI's":"brown"
        }

        colors=[category_colors[i] for i in filt_dataframe["Expense Categories"]]

        st.subheader("Your Expense Analysis Charts are as follows:")

        # Pie Chart
        fig1,ax1=plt.subplots(figsize=(10,8))
        ax1.pie(filt_dataframe["Amount"],labels=filt_dataframe["Expense Categories"],
        autopct="%1.1f%%",colors=colors)
        ax1.set_title("Expense Distribution")
        ax1.legend(filt_dataframe["Expense Categories"],title="Expense Categories",
        loc="center left",bbox_to_anchor=(1,0.5))
        st.pyplot(fig1)

        # Bar Chart
        fig2,ax2=plt.subplots(figsize=(10,6))
        ax2.bar(filt_dataframe["Expense Categories"],filt_dataframe["Amount"],color=colors)
        ax2.set_title("Expense by Category")
        ax2.set_xlabel("Categories")
        ax2.set_ylabel("Amount Spent")
        plt.xticks(rotation=90)
        st.pyplot(fig2)

        # Smart Tips
        st.subheader("Smart Tips")
        tips={
        "Entertainment and Dine out":(0.10,"Try reducing spending on entertainment and dining out."),
        "Clothing and Cosmetics":(0.08,"Consider limiting spending on clothing and cosmetics."),
        "Food and Groceries":(0.20,"Reducing outside food orders can help save money.")
        }

        good_management=True

        for cat,(limit,msg) in tips.items():
            if cat in filt_dataframe["Expense Categories"].values:
                amt=filt_dataframe.loc[filt_dataframe["Expense Categories"]==cat,"Amount"].values[0]
                if amt>limit*income:
                    st.info(msg)
                    good_management=False

        if good_management and total_expense<=budget:
            st.success("Great job! You have managed your expenses very well. Keep it up!")

        st.header("Thank You! Have a good day.")