import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"  


if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "role" not in st.session_state:
    st.session_state["role"] = None
if "user_info" not in st.session_state:
    st.session_state["user_info"] = {}

st.title("Food Delivery App")


role = st.sidebar.selectbox("I am a", ["User", "Restaurant", "Rider"], key="role_select")


if not st.session_state["logged_in"]:
    auth_option = st.sidebar.radio("Choose Action", ["Login", "Register"], key="auth_option")
    
    if auth_option == "Login":
        st.subheader(f"{role} Login")
        if role == "User":
            login_name = st.text_input("Name", key="user_login_name")
            login_password = st.text_input("Password", type="password", key="user_login_password")
            if st.button("Login as User"):
               
                response = requests.post(f"{API_URL}/login", json={"name": login_name, "password": login_password})
                if response.status_code == 200:
                    st.session_state["logged_in"] = True
                    st.session_state["role"] = "User"
                    st.session_state["user_info"] = response.json()
                    st.success(f"Logged in as {login_name}")
                else:
                    st.error("Invalid credentials for User.")
                    
        elif role == "Restaurant":
           
            restaurant_id = st.number_input("Restaurant ID", min_value=1, key="restaurant_login_id")
            if st.button("Login as Restaurant"):
                resp = requests.get(f"{API_URL}/suggest_restaurants/%%", params={"max_time":1})
                if resp.status_code == 200:
                    restaurants = resp.json()
                    restaurant = next((res for res in restaurants if res["id"] == restaurant_id), None)
                    if restaurant:
                        st.session_state["logged_in"] = True
                        st.session_state["role"] = "Restaurant"
                        st.session_state["user_info"] = restaurant
                        st.success(f"Logged in as {restaurant['name']}")
                    else:
                        st.error("Restaurant not found. Please register first.")
                else:
                    st.error("Error fetching restaurant data.")
                    
        elif role == "Rider":
            rider_id = st.number_input("Rider ID", min_value=1, key="rider_login_id")
            if st.button("Login as Rider"):
                st.session_state["logged_in"] = True
                st.session_state["role"] = "Rider"
                st.session_state["user_info"] = {"id": rider_id}
                st.success(f"Logged in as Rider {rider_id}")
    
    else: 
        st.subheader(f"{role} Registration")
        if role == "User":
            reg_name = st.text_input("Name", key="user_reg_name")
            reg_address = st.text_input("Address", key="user_reg_address")
            reg_password = st.text_input("Password", type="password", key="user_reg_password")
            if st.button("Register as User"):
                response = requests.post(
                    f"{API_URL}/register_user",
                    json={"name": reg_name, "address": reg_address, "password": reg_password}
                )
                if response.status_code == 200:
                    st.success("Registration successful. Please login.")
                else:
                    st.error(response.json().get("detail", "Registration failed."))
                    
        elif role == "Restaurant":
            res_name = st.text_input("Restaurant Name", key="res_reg_name")
            res_cuisine = st.text_input("Cuisine", key="res_reg_cuisine")
            res_location = st.text_input("Location", key="res_reg_location")
            if st.button("Register as Restaurant"):
                response = requests.post(
                    f"{API_URL}/register_restaurant",
                    json={"name": res_name, "cuisine": res_cuisine, "location": res_location}
                )
                if response.status_code == 200:
                    st.success("Restaurant registration successful. Note your Restaurant ID for login.")
                    st.write("Your details:", response.json())
                else:
                    st.error(response.json().get("detail", "Registration failed."))
                    
        elif role == "Rider":
            rider_name = st.text_input("Name", key="rider_reg_name")
            rider_location = st.text_input("Location", key="rider_reg_location")
            if st.button("Register as Rider"):
                response = requests.post(
                    f"{API_URL}/register_rider",
                    json={"name": rider_name, "location": rider_location}
                )
                if response.status_code == 200:
                    st.success("Rider registration successful. Note your Rider ID for login.")
                    st.write("Your details:", response.json())
                else:
                    st.error(response.json().get("detail", "Registration failed."))
                    
else:
  
    role = st.session_state["role"]
    st.sidebar.markdown(f"**Logged in as {role}**")
    if role == "User":
        user_menu = st.sidebar.selectbox("User Menu", ["Home", "Search Restaurants", "Place Order", "My Order History"])
        if user_menu == "Home":
            st.subheader("User Home")
            st.write(f"Welcome, {st.session_state['user_info']['name']}!")
        elif user_menu == "Search Restaurants":
            st.subheader("Search Restaurants")
            cuisine = st.text_input("Cuisine Type", key="user_search_cuisine")
            max_time = st.number_input("Max Time (minutes)", min_value=1, key="user_search_time")
            if st.button("Find Restaurants", key="user_find_res"):
                response = requests.get(f"{API_URL}/suggest_restaurants/{cuisine}/{max_time}")
                if response.status_code == 200:
                    restaurants = response.json()
                    if restaurants:
                        for res in restaurants:
                            st.write(f"**{res['name']}** - {res['cuisine']} - {res['location']}")
                    else:
                        st.write("No restaurants found.")
                else:
                    st.write("Error searching restaurants.")
                    
        elif user_menu == "Place Order":
            st.subheader("Place Order")
            cuisine = st.text_input("Enter Cuisine for Search", key="order_cuisine")
            max_time = st.number_input("Max Time (minutes)", min_value=1, key="order_time")
            
          
            if st.button("Search Restaurants", key="order_search"):
                response = requests.get(f"{API_URL}/suggest_restaurants/{cuisine}/{max_time}")
                if response.status_code == 200:
                    restaurants = response.json()
                    if restaurants:
                        st.session_state["restaurant_results"] = {restaurant["name"]: restaurant for restaurant in restaurants}
                    else:
                        st.session_state["restaurant_results"] = {}
                        st.write("No restaurants found matching your search.")
                else:
                    st.write("Error searching restaurants.")
            
           
            if "restaurant_results" in st.session_state and st.session_state["restaurant_results"]:
                restaurant_map = st.session_state["restaurant_results"]
                selected_restaurant = st.selectbox("Select Restaurant", list(restaurant_map.keys()))
                if st.button("Place Order", key="order_btn"):
                    order_response = requests.post(
                        f"{API_URL}/place_order",
                        json={
                            "user_id": st.session_state["user_info"]["id"],
                            "restaurant_id": restaurant_map[selected_restaurant]["id"]
                        }
                    )
                    st.write(order_response.json())                    
       
                    
        elif user_menu == "My Order History":
            st.subheader("My Order History")
            user_id = st.session_state["user_info"]["id"]
            response = requests.get(f"{API_URL}/user_order_history/{user_id}")
            if response.status_code == 200:
                orders = response.json()
                if orders:
                    for order in orders:
                        st.write(f"Order {order['id']}: {order['status']}")
                else:
                    st.write("You have no orders yet.")
            else:
                st.write("Error fetching order history.")
    
    elif role == "Restaurant":
        res_menu = st.sidebar.selectbox("Restaurant Menu", ["Home", "Add Menu Item", "View Orders"])
        if res_menu == "Home":
            st.subheader("Restaurant Home")
            st.write(f"Welcome, {st.session_state['user_info']['name']}!")
        elif res_menu == "Add Menu Item":
            st.subheader("Add Menu Item")
            item_name = st.text_input("Item Name", key="menu_item_name")
            price = st.number_input("Price", min_value=0.0, step=0.5, key="menu_item_price")
            if st.button("Add Item"):
                restaurant_id = st.session_state["user_info"]["id"]
                response = requests.post(
                    f"{API_URL}/add_menu_item",
                    json={"restaurant_id": restaurant_id, "item_name": item_name, "price": price}
                )
                if response.status_code == 200:
                    st.success("Menu item added.")
                    st.write(response.json())
                else:
                    st.error("Failed to add menu item.")
        elif res_menu == "View Orders":
            st.subheader("Orders for Your Restaurant")
            restaurant_id = st.session_state["user_info"]["id"]
            response = requests.get(f"{API_URL}/user_order_history/{restaurant_id}")
            if response.status_code == 200:
                orders = response.json()
                if orders:
                    for order in orders:
                        st.write(f"Order {order['id']}: {order['status']}")
                else:
                    st.write("No orders yet.")
            else:
                st.write("Error fetching orders.")
    
    elif role == "Rider":
        rider_menu = st.sidebar.selectbox("Rider Menu", ["Home", "Update Location", "My Completed Orders"])
        if rider_menu == "Home":
            st.subheader("Rider Home")
            st.write(f"Welcome, Rider {st.session_state['user_info']['id']}!")
        elif rider_menu == "Update Location":
            st.subheader("Update Your Location")
            new_location = st.text_input("New Location", key="rider_new_location")
            if st.button("Update Location"):
                rider_id = st.session_state["user_info"]["id"]
                response = requests.put(f"{API_URL}/update_rider_location/{rider_id}?location={new_location}")
                st.write(response.json())
        elif rider_menu == "My Completed Orders":
            st.subheader("My Completed Orders")
            rider_id = st.session_state["user_info"]["id"]
            response = requests.get(f"{API_URL}/rider_order_history/{rider_id}")
            if response.status_code == 200:
                orders = response.json()
                if orders:
                    for order in orders:
                        st.write(f"Order {order['id']}: {order['status']}")
                else:
                    st.write("No completed orders yet.")
            else:
                st.write("Error fetching order history.")
