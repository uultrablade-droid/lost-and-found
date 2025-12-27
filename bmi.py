import streamlit as st

st.title("BMI Calculator")

#bmi calculator form
with st.form("bmi_form"):
    weight = st.number_input("Weight (kg)", min_value=0.0, step=0.1)
    height = st.number_input("Height (m)", min_value=0.0, step=0.01)
    submit = st.form_submit_button("Calculate BMI")
    
    if submit:
        if weight > 0 and height > 0:
            bmi = weight / (height ** 2)
            st.success(f"Your BMI is: {bmi:.2f}")
            
            if bmi < 18.5:
                st.info("Underweight")
            elif bmi < 25:
                st.success("Normal weight")
            elif bmi < 30:
                st.warning("Overweight")
            else:
                st.error("Obese")
        else:
            st.error("Please enter valid weight and height values")
