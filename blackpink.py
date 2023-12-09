"""
Name: Ivan Yang
CS230: Section 2
Data: Cannabis Registry
URL:

Description:

This program
"""

import pandas as pd
import streamlit as st
from PIL import Image
import altair as alt
import pydeck as pdk
import matplotlib.pyplot as plt
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from math import radians, sin, cos, sqrt, atan2

# intro to website
st.title("Fall 2023 CS 230 Final Project")
st.header("Data from: Cannabis_Registry.csv")
img = Image.open("cannabis.jpg")
st.image(img, width=300)

def app_license_status():
    dfCannabis = read_csv("Cannabis_Registry.csv")
    value_counts = dfCannabis["app_license_status"].value_counts()
    inactive_licenses_count = value_counts.get("Inactive")
    active_licenses_count = value_counts.get("Active")
    expired_licenses_count = value_counts.get("Expired")
    deleted_licenses_count = value_counts.get("Deleted")
    return inactive_licenses_count, active_licenses_count, expired_licenses_count, deleted_licenses_count


def app_license_status_output(categories):
    licenses = ["Inactive", "Active", "Expired", "Deleted"]
    license = st.radio("Select a license status:", licenses)
    if license == "Inactive":
        st.write("There are " + str(categories[0]) + " cannabis registries in Boston that have inactive licenses.")
    elif license == "Active":
        st.write("There are " + str(categories[1]) + " cannabis registries in Boston that have active licenses.")
    elif license == "Expired":
        st.write("There are " + str(categories[2]) + " cannabis registries in Boston that have expired licenses.")
    elif license == "Deleted":
        st.write("There is " + str(categories[3]) + " cannabis registry in Boston that has a deleted license.")
    app_license_dictionary = {licenses[i]: categories[i] for i in range(len(licenses))}
    data = {"License Status": list(app_license_dictionary.keys()),
            "Number of Licenses": list(app_license_dictionary.values())}
    df = pd.DataFrame(data)
    bar_chart = (alt.Chart(df, title="Number of Licenses for Each License Status")
                 .mark_bar(color="green")
                 .encode(x="License Status", y="Number of Licenses")
                 .properties(width=600))
    st.altair_chart(bar_chart.configure_title(fontSize=20, anchor="middle"))


def longitude_and_latitude():
    st.header("Map of Cannabis Registries in Boston")
    dfCannabis = read_csv("Cannabis_Registry.csv")
    columns = ["app_business_name", "facility_address", "latitude", "longitude", "facility_zip_code"]
    dfLatAndLong = dfCannabis.loc[:, columns]
    dfLatAndLong = dfLatAndLong.dropna(subset=columns)
    view_Cannabis = pdk.ViewState(
        latitude=dfLatAndLong["latitude"].mean(),
        longitude=dfLatAndLong["longitude"].mean(),
        zoom=11,
        pitch=0)
    layer1 = pdk.Layer('ScatterplotLayer',
                       data=dfLatAndLong,
                       get_position='[longitude, latitude]',
                       get_radius=75,
                       get_color=[255, 0, 0],  # big red circle
                       pickable=True
                       )

    tool_tip = {"html": "Registry Name:<br/> <b>{app_business_name}</b> <br/> "
                        "Registry Address: <br/> <b>{facility_address}, 0{facility_zip_code}",
                "style": {"backgroundColor": "steelblue",
                          "color": "white"}
                }
    map = pdk.Deck(
        map_style='mapbox://styles/mapbox/outdoors-v11',
        initial_view_state=view_Cannabis,
        layers=layer1,
        tooltip=tool_tip
    )

    st.pydeck_chart(map)


def app_license_category():
    dfCannabis = read_csv("Cannabis_Registry.csv")
    column = "app_license_category"
    dfCannabis = dfCannabis.drop(98)
    value_counts = dfCannabis[column].value_counts()
    retail_licenses_count = value_counts.get("Retail")
    co_located_licenses_count = value_counts.get("Co-Located")
    operator_licenses_count = value_counts.get("Operator")
    courier_licenses_count = value_counts.get("Courier")
    manufact_licenses_count = value_counts.get("Manufact")
    cultivate_licenses_count = value_counts.get("Cultivate")
    medical_licenses_count = value_counts.get("Medical")
    testlab_licenses_count = value_counts.get("TestLab")
    transport_licenses_count = value_counts.get("Transport")
    return (retail_licenses_count, courier_licenses_count,  co_located_licenses_count, operator_licenses_count,
            testlab_licenses_count, manufact_licenses_count, transport_licenses_count,cultivate_licenses_count,
            medical_licenses_count)


def app_license_category_output(categories):
    st.sidebar.title("Pie Chart of Cannabis Registry License Categories")
    st.sidebar.write("Scroll until you see the pie chart!")
    columns = ["Retail", "Courier", "Co-Located", "Operator", "TestLab", "Manufact", "Transport", "Cultivate",
               "Medical"]
    dfCannabis = pd.DataFrame({"License Category": columns, "Values": categories})
    app_license_category = st.sidebar.selectbox("Select a license category:", columns)
    if app_license_category == "Retail":
        st.sidebar.write("There are " + str(categories[0]) + " cannabis registries in Boston that have retail "
                                                             "licenses.")
    elif app_license_category == "Courier":
        st.sidebar.write("There are " + str(categories[1]) + " cannabis registries in Boston that have courier "
                                                             "licenses.")
    elif app_license_category == "Co-Located":
        st.sidebar.write("There are " + str(categories[2]) + " cannabis registries in Boston that have co-located "
                                                             "licenses.")
    elif app_license_category == "Operator":
        st.sidebar.write("There are " + str(categories[3]) + " cannabis registries in Boston that have operator "
                                                             "licenses.")
    elif app_license_category == "TestLab":
        st.sidebar.write("There is " + str(categories[4]) + " cannabis registry in Boston that has a testlab "
                                                            "license.")
    elif app_license_category == "Manufact":
        st.sidebar.write("There are " + str(categories[5]) + " cannabis registries in Boston that have manufact "
                                                             "licenses.")
    elif app_license_category == "Transport":
        st.sidebar.write("There is " + str(categories[6]) + " cannabis registry in Boston that has a transport "
                                                            "license.")
    elif app_license_category == "Cultivate":
        st.sidebar.write("There are " + str(categories[7]) + " cannabis registries in Boston that have cultivate "
                                                             "licenses.")
    elif app_license_category == "Medical":
        st.sidebar.write("There are " + str(categories[8]) + " cannabis registries in Boston that have medical "
                                                             "licenses.")
    st.header("Pie Chart of Cannabis Registry License Categories")
    explode = [0] * len(dfCannabis)
    for i in range(len(columns)):
        if app_license_category == columns[i]:
            explode[i] = 0.5
    plt.pie(dfCannabis["Values"], labels=dfCannabis["License Category"], explode=explode)
    st.pyplot(plt)


def read_csv(dataset):
    dfCannabis = pd.read_csv(dataset)
    return dfCannabis


def vicinity():
    st.header("Find how many cannabis registries from the Boston area are in your zipcode!")
    dfCannabis = read_csv("Cannabis_Registry.csv")
    column = ["facility_zip_code"]
    dfLocation = dfCannabis.loc[:, column]
    dfLocation = dfLocation.dropna(subset=column)
    zipcode = st.text_input("Enter a zip code:", "02452")
    facilities_zipcode = dfLocation["facility_zip_code"].tolist()
    try:
        zipcode = int(zipcode[1:])
        facilities_in_zipcode = [item for item in facilities_zipcode if zipcode == item]
        number_of_facilities = len(facilities_in_zipcode)
        if number_of_facilities == 1:
            st.write("There is 1 cannabis registry from the Boston area in " + "0" + str(zipcode) + ".")
        elif len(str(zipcode)) != 4:
            st.write("Please type in a valid zipcode.")
        else:
            st.write("There are " + str(number_of_facilities) + " cannabis registries from the Boston area in " + "0" +
                     str(zipcode) + ".")
        print(facilities_zipcode[0])
        print(zipcode)
    except:
        st.write("Please type in a valid zipcode.")


def equity_program_designation():
    dfCannabis = read_csv("Cannabis_Registry.csv")
    value_counts = dfCannabis["equity_program_designation"].value_counts()
    no_count = value_counts.get("N")
    yes_count = value_counts.get("Y")
    null_count = len(dfCannabis) - (no_count + yes_count)
    return yes_count, no_count, null_count


def equity_program_designation_output(categories):
    designation = ["Yes", "No", "Not Applicable"]
    equity_program_dictionary = {designation[i]: categories[i] for i in range(len(designation))}
    data = {"Whether Registry Is Seeking Boston Equity Program": list(equity_program_dictionary.keys()),
            "Number of Registries": list(equity_program_dictionary.values())}
    df = pd.DataFrame(data)
    st.write("")
    st.write("")
    st.write("")
    bar_chart = (alt.Chart(df, title="Number of Registries Seeking Boston Equity Program")
                 .mark_bar(color="blue")
                 .encode(x="Whether Registry Is Seeking Boston Equity Program", y="Number of Registries")
                 .properties(width=600))
    st.altair_chart(bar_chart.configure_title(fontSize=20, anchor="middle"))



def status_and_category():
    dfCannabis = read_csv("Cannabis_Registry.csv")
    columns = ["app_license_category", "app_license_status"]
    dfCategoryAndStatus = dfCannabis.loc[:, columns]
    dfLocation = dfCategoryAndStatus.dropna(subset=columns)
    print(dfLocation)


app_license_status_output(app_license_status())
longitude_and_latitude()
app_license_category_output(app_license_category())
vicinity()
status_and_category()
equity_program_designation_output(equity_program_designation())
