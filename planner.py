import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

def calculate_savings(salary, rent, misc_expen, debts):
    cap_left = salary - rent - misc_expen

    health = (salary) * 0.02

    emeg_fund = 6 * (rent + misc_expen) / 10
    savings = cap_left - health - emeg_fund - debts

    return savings, emeg_fund, health

def main():
    st.title("Financial Planner")

    session_state = st.session_state

    if 'salary' not in session_state:
        session_state.salary = 0
    if 'rent' not in session_state:
        session_state.rent = 0
    if 'misc_expen' not in session_state:
        session_state.misc_expen = 0
    if 'debts' not in session_state:
        session_state.debts = 0

    salary = st.number_input("Enter your in hand salary:", value=session_state.salary)
    rent = st.number_input("Enter your home rent:", value=session_state.rent)
    misc_expen = st.number_input("Enter your Miscellaneous expenditure:", value=session_state.misc_expen)
    debts = st.number_input("Enter your debts:", value=session_state.debts)

    session_state.salary = salary
    session_state.rent = rent
    session_state.misc_expen = misc_expen
    session_state.debts = debts

    savings, emeg_fund, health = calculate_savings(salary, rent, misc_expen, debts)

    st.subheader("Financial Summary")
    st.write(f"Emergency Fund: ", emeg_fund)
    st.write("Health insurance: ", health)
    st.write(f"Net Savings: ", round(savings, 2))

    choice = st.radio("Choose your asset goal:", options=["House Buying", "Car Buying", "Jewellery","Others"])
    amount = savings * 10

    if 'house_downpayment' not in session_state:
        session_state.house_downpayment = 1
    if 'house_cost' not in session_state:
        session_state.house_cost = 1
    if 'house_loan_amount' not in session_state:
        session_state.house_loan_amount = 1
    if 'house_years' not in session_state:
        session_state.house_years = 2
    if 'house_loan_tenure' not in session_state:
        session_state.house_loan_tenure = 1
    if 'home_emi' not in session_state:
        session_state.home_emi = 0

    if 'home_save' not in session_state:
        session_state.home_save = 0
 
    if 'home_save2' not in session_state:
        session_state.home_save2 = 1
    if 'car_downpayment' not in session_state:
        session_state.car_downpayment = 1
    if 'car_cost' not in session_state:
        session_state.car_cost = 1
    if 'car_loan_amount' not in session_state:
        session_state.car_loan_amount = 1
    if 'car_years' not in session_state:
        session_state.car_years = 2
    if 'car_loan_tenure' not in session_state:
        session_state.car_loan_tenure = 1
    if 'car_emi' not in session_state:
        session_state.car_emi = 1
    if 'car_save' not in session_state:
        session_state.car_save = 0
    if 'car_save2' not in session_state:
        session_state.car_save2 = 0

    if 'gold_downpayment' not in session_state:
        session_state.gold_downpayment = 1
    if 'gold_cost' not in session_state:
        session_state.gold_cost = 1
    if 'gold_loan_amount' not in session_state:
        session_state.gold_loan_amount = 1
    if 'gold_years' not in session_state:
        session_state.gold_years = 2
    if 'gold_loan_tenure' not in session_state:
        session_state.gold_loan_tenure = 1
    if 'gold_emi' not in session_state:
        session_state.gold_emi = 0
    if 'gold_save' not in session_state:
        session_state.gold_save = 0
    if 'gold_save2' not in session_state:
        session_state.gold_save2 = 0

    
    if 'invest_plan' not in session_state:
        session_state.investPlan = 0

    if 'amt_left' not in session_state:
        session_state.amt_left = 0
    if 'travel' not in session_state:
        session_state.travel = 0



    if choice == "House Buying":
        option = st.radio("Planning for loan: ", options=["Yes", "No"])
        st.subheader("House Buying plans")
        session_state.house_years = st.slider("How many years down the line: ", 1, 60, session_state.house_years)
        session_state.house_cost = st.number_input("Cost of House:", value=session_state.house_cost)
        if option == "Yes":
            session_state.house_downpayment = st.slider("Downpayment:",
                                                        int(session_state.house_cost * 0.1),
                                                        int(session_state.house_cost * 0.9),
                                                        int(session_state.house_cost * 0.1))
            session_state.home_save = st.write("Money to be saved without using savings: ",
                                 round(session_state.house_downpayment / (12 * session_state.house_years), 2))
            session_state.home_save2 = st.write("Money to be saved by using 90% of savings",
                                  round((session_state.house_downpayment - (amount * 0.9)) / (
                                              12 * session_state.house_years), 2))
            session_state.house_loan_tenure = st.slider("Loan Tenure (years):", 1, 60, session_state.house_loan_tenure)
            session_state.house_loan_amount = (session_state.house_cost - session_state.house_downpayment) * 0.05

            for i in range(1, session_state.house_loan_tenure):
                session_state.house_loan_amount = session_state.house_loan_amount + session_state.house_loan_amount * 0.085

            st.write("Loan Amount: ", round(session_state.house_cost - session_state.house_downpayment, 2))
            st.write("Interest: ", round(session_state.house_loan_amount, 2))
            st.write("Total Amount: ",
                     round(session_state.house_cost - session_state.house_downpayment + session_state.house_loan_amount,
                           2))

            # EMI calculation
            r = 9 / 12 / 100  # Monthly interest rate
            session_state.home_emi = ((session_state.house_cost - session_state.house_downpayment) * r * (
                        (1 + r) ** (session_state.house_loan_tenure * 12))) / (
                                   ((1 + r) ** (session_state.house_loan_tenure * 12)) - 1)
            st.write(f"EMI: ", round(session_state.home_emi, 2))

            # Donut chart
            if(savings-session_state.home_emi >0):
                labels = ['Rent', 'Miscellaneous', 'Debts', 'Home EMI', 'Savings']
                sizes = [session_state.rent, session_state.misc_expen, session_state.debts, session_state.home_emi,
                        savings - session_state.home_emi]
                colors = ['#ff9999', '#66b3ff', '#ffcc99', '#99ff99', '#bd05f5']
                fig, ax = plt.subplots()
                ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
                centre_circle = Circle((0, 0), 0.70, fc='white')
                ax.add_patch(centre_circle)
                ax.axis('equal')
                st.pyplot(fig)
            
            else:
                st.write("\n\nYour savings is turning out to be negative")
                st.write("Need to increase your loan tenure")

        else:
            session_state.home_save = round(session_state.house_cost/(12*session_state.house_years),2)
            st.write("Money to be saved without using savings: ",session_state.home_save)
            session_state.home_save2 = round((session_state.house_cost-(amount*0.9))/(12*session_state.house_years),2)
            st.write("Money to be saved by using 90% of savings",)

            labels = ['Rent', 'Miscellaneous', 'Debts', 'For Home', 'Savings']
            sizes = [rent, misc_expen, debts, session_state.home_save, savings-session_state.home_save]
            colors = ['#ff9999', '#66b3ff', '#ffcc99', '#99ff99','#bd05f5']
            fig, ax = plt.subplots()
            ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            centre_circle = Circle((0, 0), 0.70, fc='white')
            ax.add_patch(centre_circle)
            ax.axis('equal')
            st.pyplot(fig)

            if(session_state.home_save2 >=0):
                labels = ['Rent', 'Miscellaneous', 'Debts', 'For Home', 'Savings']
                sizes = [rent, misc_expen, debts, session_state.home_save2, savings-session_state.home_save2]
                colors = ['#ff9999', '#66b3ff', '#ffcc99', '#99ff99','#bd05f5']
                fig, ax = plt.subplots()
                ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
                centre_circle = Circle((0, 0), 0.70, fc='white')
                ax.add_patch(centre_circle)
                ax.axis('equal')
                st.pyplot(fig)


    elif choice == "Car Buying":
        option = st.radio("Planning for loan: ", options=["Yes", "No"])
        st.subheader("Car buying plans ")
        session_state.car_years = st.slider("How many years down the line: ", 1, 60, session_state.car_years)
        session_state.car_cost = st.number_input("Cost of Car:", value=session_state.car_cost)

        # Other car buying logic
        if option == "Yes":
            session_state.car_downpayment = st.slider("Downpayment:",
                                                        int(session_state.car_cost * 0.1),
                                                        int(session_state.car_cost * 0.9),
                                                        int(session_state.car_cost * 0.1))
            session_state.car_save = st.write("Money to be saved without using savings: ",
                                 round(session_state.car_downpayment / (12 * session_state.car_years), 2))
            session_state.car_save2 = st.write("Money to be saved by using 90% of savings",
                                  round((session_state.car_downpayment - (amount * 0.9)) / (
                                              12 * session_state.car_years), 2))
            session_state.car_loan_tenure = st.slider("Loan Tenure (years):", 1, 60, session_state.car_loan_tenure)
            session_state.car_loan_amount = (session_state.car_cost - session_state.car_downpayment) * 0.05

            for i in range(1, session_state.car_loan_tenure):
                session_state.car_loan_amount = session_state.car_loan_amount + session_state.car_loan_amount * 0.085

            st.write("Loan Amount: ", round(session_state.car_cost - session_state.car_downpayment, 2))
            st.write("Interest: ", round(session_state.car_loan_amount, 2))
            st.write("Total Amount: ",
                     round(session_state.car_cost - session_state.car_downpayment + session_state.car_loan_amount,
                           2))

            # EMI calculation
            r = 8 / 12 / 100  # Monthly interest rate
            session_state.car_emi = ((session_state.car_cost - session_state.car_downpayment) * r * (
                        (1 + r) ** (session_state.car_loan_tenure * 12))) / (
                                   ((1 + r) ** (session_state.car_loan_tenure * 12)) - 1)
            st.write(f"EMI: ", round(session_state.car_emi, 2))

            # Donut chart
            if (savings - session_state.home_emi - session_state.car_emi >=0):
                labels = ['Rent', 'Miscellaneous', 'Debts', 'Home EMI', 'Car EMI', 'Savings']
                sizes = [session_state.rent, session_state.misc_expen, session_state.debts, session_state.home_emi, session_state.car_emi,
                        savings - session_state.home_emi - session_state.car_emi]
                colors = ['#ff9999', '#66b3ff', '#ffcc99', '#99ff99', '#bd05f5','#0bbabd']
                fig, ax = plt.subplots()
                ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
                centre_circle = Circle((0, 0), 0.70, fc='white')
                ax.add_patch(centre_circle)
                ax.axis('equal')
                st.pyplot(fig)
            
            else:
                st.write("\n\nYour savings is turning out to be negative")
                st.write("Need to increase your loan tenure")


        else:
            session_state.car_save = round(session_state.car_cost/(12*session_state.car_years),2)
            st.write("Money to be saved without using savings: ",session_state.car_save)
            session_state.car_save2 = round((session_state.car_cost - (amount*0.9))/(12*session_state.car_years),2)
            st.write("Money to be saved by using 90% of savings",session_state.car_save2)
            
            if(savings - session_state.home_emi - session_state.car_save>0):
                labels = ['Rent', 'Miscellaneous', 'Debts', 'Home EMI ', 'For Car ', 'Savings']
                sizes = [session_state.rent, session_state.misc_expen, session_state.debts, session_state.home_emi, session_state.car_save,
                        savings - session_state.home_emi - session_state.car_save]
                colors = ['#ff9999', '#66b3ff', '#ffcc99', '#99ff99', '#bd05f5','#0bbabd']
                fig, ax = plt.subplots()
                ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
                centre_circle = Circle((0, 0), 0.70, fc='white')
                ax.add_patch(centre_circle)
                ax.axis('equal')
                st.pyplot(fig)


            if session_state.car_save2 >=0:
                labels = ['Rent', 'Miscellaneous', 'Debts', 'Home EMI', 'For Car', 'Savings']
                sizes = [session_state.rent, session_state.misc_expen, session_state.debts, session_state.home_emi, session_state.car_save2,
                        savings - session_state.home_emi - session_state.car_save2]
                colors = ['#ff9999', '#66b3ff', '#ffcc99', '#99ff99', '#bd05f5','#0bbabd']
                fig, ax = plt.subplots()
                ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
                centre_circle = Circle((0, 0), 0.70, fc='white')
                ax.add_patch(centre_circle)
                ax.axis('equal')
                st.pyplot(fig)
        




    elif choice == "Jewellery":
        option = st.radio("Planning for loan: ", options=["Yes", "No"])
        st.subheader("Gold buying plans ")
        session_state.gold_years = st.slider("How many years down the line: ", 1, 60,
                                                   session_state.gold_years)
        session_state.gold_cost = st.number_input("Cost of Gold ", value=session_state.gold_cost)

        # Other jewellery buying logic

        if option == "Yes":
            session_state.gold_downpayment = st.slider("Downpayment:",
                                                        int(session_state.gold_cost * 0.1),
                                                        int(session_state.gold_cost * 0.9),
                                                        int(session_state.gold_cost * 0.1))
            session_state.gold_save = st.write("Money to be saved without using savings: ",
                                 round(session_state.gold_downpayment / (12 * session_state.gold_years), 2))
            session_state.gold_save2 = st.write("Money to be saved by using 90% of savings",
                                  round((session_state.gold_downpayment - (amount * 0.9)) / (
                                              12 * session_state.gold_years), 2))
            session_state.gold_loan_tenure = st.slider("Loan Tenure (years):", 1, 60, session_state.gold_loan_tenure)
            session_state.gold_loan_amount = (session_state.gold_cost - session_state.gold_downpayment) * 0.05

            for i in range(1, session_state.gold_loan_tenure):
                session_state.gold_loan_amount = session_state.gold_loan_amount + session_state.gold_loan_amount * 0.085

            st.write("Loan Amount: ", round(session_state.gold_cost - session_state.gold_downpayment, 2))
            st.write("Interest: ", round(session_state.gold_loan_amount, 2))
            st.write("Total Amount: ",
                     round(session_state.gold_cost - session_state.gold_downpayment + session_state.gold_loan_amount,
                           2))

            # EMI calculation
            r = 9.1 / 12 / 100  # Monthly interest rate
            session_state.gold_emi = ((session_state.gold_cost - session_state.gold_downpayment) * r * (
                        (1 + r) ** (session_state.gold_loan_tenure * 12))) / (
                                   ((1 + r) ** (session_state.gold_loan_tenure * 12)) - 1)
            st.write(f"EMI: ", round(session_state.gold_emi, 2))

            # Donut chart
            if (savings - session_state.home_emi - session_state.car_emi >=0) :
                labels = ['Rent', 'Miscellaneous', 'Debts', 'Home EMI', 'Car EMI', 'Gold EMI', 'Savings']
                sizes = [session_state.rent, session_state.misc_expen, session_state.debts, session_state.home_emi, session_state.car_emi, session_state.gold_emi,
                        savings - session_state.home_emi - session_state.car_emi- session_state.gold_emi]
                colors = ['#ff9999', '#66b3ff', '#ffcc99', '#99ff99', '#bd05f5','#0bbabd','#7ed437']
                fig, ax = plt.subplots()
                ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
                centre_circle = Circle((0, 0), 0.70, fc='white')
                ax.add_patch(centre_circle)
                ax.axis('equal')
                st.pyplot(fig)
            
            else:
                st.write("\n\nYour savings is turning out to be negative")
                st.write("Need to increase your loan tenure")


        else:
            session_state.gold_save = round(session_state.gold_cost/(12*session_state.gold_years),2)
            st.write("Money to be saved without using savings: ",session_state.gold_save)
            session_state.gold_save2 = round((session_state.gold_cost-(amount*0.9))/(12*session_state.gold_years),2)
            st.write("Money to be saved by using 90% of savings",session_state.gold_save2)



            labels = ['Rent', 'Miscellaneous', 'Debts', 'Home EMI', 'For Car ','For gold', 'Savings']
            sizes = [session_state.rent, session_state.misc_expen, session_state.debts, session_state.home_emi, session_state.car_save, session_state.gold_save ,
                     savings - session_state.home_emi - session_state.car_save - session_state.gold_save]
            colors = ['#ff9999', '#66b3ff', '#ffcc99', '#99ff99', '#bd05f5','#0bbabd','#7ed437']
            fig, ax = plt.subplots()
            ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            centre_circle = Circle((0, 0), 0.70, fc='white')
            ax.add_patch(centre_circle)
            ax.axis('equal')
            st.pyplot(fig)


            if session_state.car_save2 >=0:
                labels = ['Rent', 'Miscellaneous', 'Debts', 'Home EMI', 'For Car', 'Savings']
                sizes = [session_state.rent, session_state.misc_expen, session_state.debts, session_state.home_emi, session_state.car_save2,
                        savings - session_state.home_emi - session_state.car_save2]
                colors = ['#ff9999', '#66b3ff', '#ffcc99', '#99ff99', '#bd05f5','#0bbabd']
                fig, ax = plt.subplots()
                ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
                centre_circle = Circle((0, 0), 0.70, fc='white')
                ax.add_patch(centre_circle)
                ax.axis('equal')
                st.pyplot(fig)


    elif choice == "Others":
        session_state.amt_left = savings - session_state.home_emi - session_state.car_emi - session_state.gold_emi
        session_state.invest_plan = (session_state.amt_left)*0.2
        session_state.travel = (session_state.amt_left - session_state.invest_plan)*0.1

        
        
        if(session_state.amt_left >=0):
            labels = ['Rent', 'Miscellaneous', 'Debts', 'Home EMI', 'Car EMI', 'Gold EMI','Mutual Funds','Travel','Savings']
            sizes = [session_state.rent, session_state.misc_expen, session_state.debts, session_state.home_emi, session_state.car_emi, session_state.gold_emi,
                    session_state.invest_plan,session_state.travel,savings - session_state.home_emi - session_state.car_emi- session_state.gold_emi-session_state.invest_plan-session_state.travel]
            colors = ['#ff9999', '#66b3ff', '#ffcc99', '#99ff99', '#bd05f5','#0bbabd','#7ed437','#e80c05','#d9e805']
            fig, ax = plt.subplots()
            ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            centre_circle = Circle((0, 0), 0.70, fc='white')
            ax.add_patch(centre_circle)
            ax.axis('equal')
            st.pyplot(fig)


        



if __name__ == "__main__":
    main()
