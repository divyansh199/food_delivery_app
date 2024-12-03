import pandas as pd
import numpy as np
import pickle

from flask.views import MethodView
from wtforms import Form, StringField, IntegerField, SubmitField, SelectField, TimeField, DateField
from flask import Flask, render_template, request

from datetime import date, time

from files.distance_to_deliver import DistanceToDeliver
from files.data_cleaning import DataCleaning
from files.encoding import Encoding
from files.feature_engineering import FeatureEngineering

with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

with open('xgbmodel.pkl', 'rb') as f:
    model = pickle.load(f)


app = Flask(__name__)

class HomePage(MethodView):

    def get(self):
        return render_template('index.html')


class FoodFormPage(MethodView):

    def get(self):
        food = FoodForm()
        return render_template('food_form_page.html', food=food)

    def post(self):

        food = FoodForm(request.form)
        dist1 = DistanceToDeliver(food.restaurant_address.data)
        dist2 = DistanceToDeliver(food.delivery_address.data)
        restaurant_lat, restaurant_long = dist1.scrape()
        delivery_lat, delivery_long =  dist2.scrape()
        input_data = pd.DataFrame({
        'Delivery_person_ID': [food.delivery_person_id.data],
        'Delivery_person_Age': [food.age.data],
        'Delivery_person_Ratings': [food.ratings.data],
        'Restaurant_latitude': [restaurant_lat],
        'Restaurant_longitude': [restaurant_long],
        'Delivery_location_latitude': [delivery_lat],
        'Delivery_location_longitude': [delivery_long],
        'Order_Date': [food.order_date.data],
        'Time_Orderd': [food.time_ordered.data],
        'Time_Order_picked': [food.time_order_picked.data],
        'weather_conditions': [food.weather.data],
        'Road_traffic_density': [food.traffic.data],
        'Vehicle_condition': [food.vehicle_condition.data],
        'Type_of_order': [food.order_type.data],
        'Type_of_vehicle': [food.vehicle_type.data],
        'multiple_deliveries': [food.multiple_deliveries.data],
        'Festival': [food.festival.data],
        'City': [food.city.data]
        })

        data_clean = DataCleaning()
        feature = FeatureEngineering()
        encode = Encoding()

        input_data = data_clean.extract_columns_value(input_data)
        input_data =  data_clean.update_datatype(input_data)
        input_data = feature.extract_date_features(input_data)
        input_data = feature.calculate_time_diff(input_data)
        input_data = feature.calculate_distance(input_data)
        input_data = encode.label_encoding(input_data)
        input_data.drop('Delivery_person_ID', axis=1, inplace=True)
        scaled_data = scaler.transform(input_data)
        prediction =  model.predict(scaled_data)
        prediction = round(prediction[0], 2)

        return render_template('food_form_page.html', prediction=prediction, food=food, result = True)




class FoodForm(Form):

    delivery_person_id = StringField('Delivery Person ID', default= 'BANGRES19DEL01')
    age = IntegerField('Age', default= 20)
    ratings = SelectField(u'Rating', choices=[('1','1⭐️'),('2','2⭐️'),('3','3⭐️'),('4','4⭐️'),('5','5⭐️')])
    order_date = DateField('Order Date', format='%Y-%m-%d')
    time_ordered = TimeField('Time Ordered', format='%H:%M:%S')
    time_order_picked = TimeField('Time Order Picked', format='%H:%M:%S')
    weather = SelectField(u'Weather Condition', choices=[('Sunny','Sunny'),('Clody','Clody'),('Rainy','Rainy'),('Foggy','Foggy')])
    traffic = SelectField(u'Road Traffic Density', choices=[('Low','Low'),('Medium','Medium'),('High','High'),('Jam','Jam')])
    vehicle_condition = IntegerField('Vehicle Condition', default= 0)
    order_type = SelectField('Type of Order', choices=[('Snack','Snack'), ('Meal','Meal'), ('Drinks','Drinks'), ('Buffet','Buffet')])
    vehicle_type = SelectField('Type of Vehicle', choices=[('Bike','Bike'), ('Scooter','Scooter'), ('Car','Car'), ('Truck','Truck')])
    multiple_deliveries = IntegerField('Multiple Deliveries', default= 0)
    festival = SelectField('Festival', choices=[('No','No'), ('Yes','Yes')])
    city = SelectField('City', choices = [('Urban','Urban'), ('Semi-Urban','Semi-Urban'), ('Metropolitan','Metropolitan')])

    restaurant_address = StringField('Restaurant Address')
    delivery_address = StringField('Delivery Address')

    button = SubmitField('Calculate')







# app.add_url_rule('/', view_func=HomePage.as_view('homepage'))

app.add_url_rule('/', view_func= FoodFormPage.as_view('food_form_page'))

if __name__ == '__main__':
    app.run(debug=True)