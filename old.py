import numpy as np
import pickle
import streamlit as st
from get_geo import get_latitude_longitude
from search_place import get_nearby_places

# loading the saved model
loaded_model = pickle.load(open('Downloads/trained_model.sav', 'rb'))

loaded_regression = pickle.load(open('Downloads/prediction.sav', 'rb'))

# loading additional information from a separate text file
def load_additional_information():
    with open('C:/Users/CRang/PycharmProjects/machine learning/information.txt', 'r') as f:
        return f.read()


# Dictionary of dishes and their calorie values
dishes = {
    "Puri": 75,
    "Chapati": 60,
    "Paratha": 150,
    "Idli": 100,
    "Dosa Plain": 120,
    "Dosa Masala": 250,
    "sambar": 150,
    "Cooked rice": 120,
    "Phulka": 60,
    "Naan": 150,
    "Dal": 150,
    "Curd": 100,
    "Vegetable curry": 150,
    "Meat curry": 175,
    "Tea": 45,
    "Fresh fruit juice": 120
}


def calorie_counter():
    st.title("Calorie Counter")
    st.write("Enter the quantity for each dish to calculate the total calories.")

    # Create empty dictionary to store dish quantities
    dish_quantities = {}

    # Display dishes and quantity inputs
    for dish in dishes:
        quantity = st.number_input(f"Enter quantity for {dish}", key=f"{dish}_quantity", min_value=0, step=1)
        dish_quantities[dish] = quantity

    # Calculate total calories
    total_calories = sum(dishes[dish] * quantity for dish, quantity in dish_quantities.items())

    # Display total calories
    st.write("Total calories:", total_calories)



# creating a function for Diabetes Prediction
def diabetes_prediction(input_data):
    # changing the input_data to numpy array
    input_data_as_numpy_array = np.asarray(input_data)

    # reshape the array as we are predicting for one instance
    input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)

    prediction = loaded_model.predict(input_data_reshaped)


    if prediction[0] == 0:
        return {'Prediction': 'The person is not diabetic'}
    else:
        information = load_additional_information()
        return {'Prediction': 'The person is diabetic', 'Information': information}

def diabetes_regression(input_data):
    # changing the input_data to numpy array
    input_data_as_numpy_array = np.asarray(input_data)

    # reshape the array as we are predicting for one instance
    input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)

    regression = loaded_regression.predict(input_data_reshaped)

    return regression


def diabetes_classification():
    st.write("Enter 0 if Ans is No Else 1")

    # getting the input data from the user
    Age = st.text_input('Age')
    Gender = st.text_input('Gender: Enter 0 if Male Else 1')
    complications = st.text_input('complications: Enter 1 if you have any of these [Hypertension, Neuropathy, Nephropathy, Diabetic ulcer , Chronic Kidney Disease] ')
    smoked = st.text_input('Smoked')
    work_moderate_activity = st.text_input('Work Moderate Activity (Brisk Walking, Carrying load)')
    High_blood_pressure = st.text_input('High Blood Pressure')
    High_blood_sugar = st.text_input('High Blood Sugar')
    family_members_diabetes = st.text_input('Family Members Diabetes')
    BMI = st.text_input('BMI')
    WHR = st.text_input('WHR')
    address = st.text_input('address: Enter current location')

    # code for prediction
    Diabetes = ''

    # creating a button for prediction
    if st.button('Diabetes Test Result'):
        input_values = [Age, Gender, complications, smoked, work_moderate_activity,
                        High_blood_pressure, High_blood_sugar, family_members_diabetes, BMI, WHR]
        if all(value.strip() for value in input_values):
            try:
                input_values = [float(value) for value in input_values]
                result = diabetes_prediction(input_values)
                regresult = diabetes_regression(input_values)
                st.write(result['Prediction']) # Display the prediction result
                if 'Information' in result:
                    st.write(result['Information'])# Display additional information if available
                if result['Prediction'] == 'The person is diabetic':
                    latitude, longitude = get_latitude_longitude(address)
                    hospitals = get_nearby_places(latitude, longitude, 2000, "hospital")
                    if hospitals:
                        st.write("Nearby Hospitals:")
                        for hospital in hospitals:
                            name = hospital["name"]
                            address = hospital["address"]
                            st.write(f"Name: {name}")
                            st.write(f"Address: {address}")
                            st.write("------------")
                    else:
                        st.write("No hospitals found nearby.")
            except ValueError:
                st.error('Please enter numeric values for Age, BMI, and WHR.')
        else:
            st.error('Please provide values for all input fields.')


def bmi_calculator():
    st.title("BMI Calculator")

    # getting the input data for BMI calculation
    height = st.text_input("Height (in meters)")
    weight = st.text_input("Weight (in kilograms)")

    # creating a button to calculate BMI
    if st.button("Calculate BMI"):
        if height and weight:
            try:
                height = float(height)
                weight = float(weight)
                bmi = weight / (height ** 2)
                st.write("Your BMI is:", bmi)
            except ValueError:
                st.error("Please enter valid numeric values for height and weight.")
        else:
            st.error("Please provide values for height and weight.")

def load_diet_file():
    with open('C:/Users/CRang/PycharmProjects/machine learning/diet.txt', 'r') as f:
        return f.read()

def diet_for_diabetes():
    st.title("Diet for Diabetes")
    st.write("Recommended diet for diabetes:")
    diet = load_diet_file()
    st.write(diet)

def load_exercise_file():
    with open('C:/Users/CRang/PycharmProjects/machine learning/exercise.txt', 'r') as f:
        return f.read()

def exercise_for_diabetes():
    st.title("Exercise for Diabetes")
    st.write("Recommended exercises for diabetes:")
    exercise = load_exercise_file()
    st.write(exercise)


def main():
    # giving a title
    st.title("Diabetes Classification App")

    # Create a sidebar menu for navigation
    menu = ['Diabetes Classification', 'BMI Calculator', 'Calorie counter','Diet','Exercises']
    choice = st.sidebar.selectbox('Select Page', menu)

    if choice == 'Diabetes Classification':
        diabetes_classification()
    elif choice == 'BMI Calculator':
        bmi_calculator()
    elif choice == "Calorie counter":
        calorie_counter()
    elif choice == "Diet":
        diet_for_diabetes()
    elif choice == "Exercises":
        exercise_for_diabetes()


if __name__ == '__main__':
    main()