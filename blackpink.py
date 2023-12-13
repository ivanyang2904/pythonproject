"""
Name: Ivan Yang
CS230: Section 2
Data: Cannabis Registry
URL:

Description:

This program gives an overall summary of the Cannabis_Registry.csv spreadsheet from Analyze Boston. Graphs regarding
license status, license categories, and registries seeking Boston Equity Program are included. There is also an input
text box that lets the user see if their zipcode contains a registry from the Boston area as well as a map of all the
cannabis registries in Boston.
"""

# importing packages
import pandas as pd
import streamlit as st
from PIL import Image
import altair as alt
import pydeck as pdk
import matplotlib.pyplot as plt

# intro to website
st.title("Ivan Yang's CS 230 Final Project")
st.header("Cannabis Registry Data from Analyze Boston")
st.write("If there are any unfamiliar terms, scroll down to the bottom to see definitions and explanations.")
img = Image.open("cannabis.jpg")
st.image(img, width=300)


# calculates the number of registries with each license status
def app_license_status():
    dfCannabis = read_csv("Cannabis_Registry.csv")
    value_counts = dfCannabis["app_license_status"].value_counts()  # counts of unique values
    inactive_licenses_count = value_counts.get("Inactive")
    active_licenses_count = value_counts.get("Active")
    expired_licenses_count = value_counts.get("Expired")
    deleted_licenses_count = value_counts.get("Deleted")
    return inactive_licenses_count, active_licenses_count, expired_licenses_count, deleted_licenses_count


# outputs a bar graph with the calculations of the number of registries with each license status
def app_license_status_output(categories):
    licenses = ["Inactive", "Active", "Expired", "Deleted"]
    license = st.radio("Select a license status:", licenses)  # radio buttons of license statuses
    if license == "Inactive":
        st.write("There are " + str(categories[0]) + " cannabis registries in Boston that have inactive licenses.")
    elif license == "Active":
        st.write("There are " + str(categories[1]) + " cannabis registries in Boston that have active licenses.")
    elif license == "Expired":
        st.write("There are " + str(categories[2]) + " cannabis registries in Boston that have expired licenses.")
    elif license == "Deleted":
        st.write("There is " + str(categories[3]) + " cannabis registry in Boston that has a deleted license.")

    # creates a dictionary with license status as keys and counts as values
    app_license_dictionary = {licenses[i]: categories[i] for i in range(len(licenses))}
    data = {"License Status": list(app_license_dictionary.keys()),
            "Number of Licenses": list(app_license_dictionary.values())}
    df = pd.DataFrame(data)
    # https://altair-viz.github.io/user_guide/generated/toplevel/altair.Chart.html
    bar_chart = (alt.Chart(df, title="Number of Licenses for Each License Status")
                 .mark_bar(color="green")  # sets chart to bar type and green bars
                 .encode(x="License Status", y="Number of Licenses")  # naming x and y axes
                 .properties(width=600))  # sets width of bar chart
    # sets font size of title and sets the title at the middle of the chart
    # https://docs.streamlit.io/library/api-reference/charts/st.altair_chart
    st.altair_chart(bar_chart.configure_title(fontSize=20, anchor="middle"))


# filters dataset and creates a map of the locations of the cannabis registries
def longitude_and_latitude():
    st.header("Map of Cannabis Registries in Boston")
    dfCannabis = read_csv("Cannabis_Registry.csv")
    columns = ["app_business_name", "facility_address", "latitude", "longitude", "facility_zip_code"]
    dfLatAndLong = dfCannabis.loc[:, columns]  # selects all rows from the columns
    dfLatAndLong = dfLatAndLong.dropna(subset=columns)  # removes all rows with null values
    view_Cannabis = pdk.ViewState(
        latitude=dfLatAndLong["latitude"].mean(),
        longitude=dfLatAndLong["longitude"].mean(),
        zoom=11,  # initial zoom level of the map
        pitch=0)  # sets the initial tilt of the map view
    layer1 = pdk.Layer('ScatterplotLayer',
                       data=dfLatAndLong,
                       get_position='[longitude, latitude]',
                       get_radius=75,  # radius of each circle
                       get_color=[255, 0, 0],  # big red circle created
                       pickable=True  # makes the points interactive and selectable
                       )
    # when user hovers over a circle, information below is shown
    tool_tip = {"html": "Registry Name:<br/> <b>{app_business_name}</b> <br/> "
                        "Registry Address: <br/> <b>{facility_address}, 0{facility_zip_code}",
                "style": {"backgroundColor": "steelblue",
                          "color": "white"}
                }
    map = pdk.Deck(
        map_style='mapbox://styles/mapbox/outdoors-v11',  # may style
        initial_view_state=view_Cannabis,
        layers=layer1,
        tooltip=tool_tip
    )

    st.pydeck_chart(map)  # displays the map


# gets the values of unique counts of app categories
def app_license_category():
    dfCannabis = read_csv("Cannabis_Registry.csv")
    column = "app_license_category"
    dfCannabis = dfCannabis.drop(98)  # dropping a row with a null value
    value_counts = dfCannabis[column].value_counts()  # counts of unique values
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


# outputs a piechart depending on what the user selects from the dropdown
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
    explode = [0] * len(dfCannabis)  # creating a list of 0s
    for i in range(len(columns)):
        if app_license_category == columns[i]:
            explode[i] = 0.5  # explode pie piece based on what the user selects
    # https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.pie.html
    plt.pie(dfCannabis["Values"],  # pie piece size depends on value counts of categories
            labels=dfCannabis["License Category"],  # different categories for each pie piece
            explode=explode)  # explode pie piece based on what the user selects
    st.pyplot(plt)


# function used to read the cannabis_registry.csv
def read_csv(dataset):
    dfCannabis = pd.read_csv(dataset)
    return dfCannabis


# tells the user how many cannabis registries from the Boston area are in the zipcode they input
def vicinity():
    st.header("Find How Many Cannabis Registries From the Boston Area Are in Your Zipcode!")
    dfCannabis = read_csv("Cannabis_Registry.csv")
    column = ["facility_zip_code"]
    dfLocation = dfCannabis.loc[:, column]  # selects all rows from a column
    dfLocation = dfLocation.dropna(subset=column)  # removes rows with null values
    zipcode = st.text_input("Enter a zip code:", "02452")  # Bentley University's zipcode is the default zipcode
    facilities_zipcode = dfLocation["facility_zip_code"].tolist()  # convert the column to a list
    try:  # if the zipcode contains all integers
        zipcode = int(zipcode[1:])
        # checks to see if zipcode is in the list of zipcodes
        facilities_in_zipcode = [item for item in facilities_zipcode if zipcode == item]
        number_of_facilities = len(facilities_in_zipcode)
        if number_of_facilities == 1:
            st.write("There is 1 cannabis registry from the Boston area in " + "0" + str(zipcode) + ".")
        elif len(str(zipcode)) != 4:  # input validation
            st.write("Please type in a valid zipcode.")
        else:
            st.write("There are " + str(number_of_facilities) + " cannabis registries from the Boston area in " + "0" +
                     str(zipcode) + ".")
    except:  # if zipcode does not contain all integers
        st.write("Please type in a valid zipcode.")


# counts the values of registries applying for the boston equity program
def equity_program_designation():
    dfCannabis = read_csv("Cannabis_Registry.csv")
    value_counts = dfCannabis["equity_program_designation"].value_counts()
    no_count = value_counts.get("N")
    yes_count = value_counts.get("Y")
    null_count = len(dfCannabis) - (no_count + yes_count)  # null values are the ones not counted
    return yes_count, no_count, null_count


# outputs a bar graph showing the registries who applied to the boston equity program
def equity_program_designation_output(categories):
    designation = ["Yes", "No", "Not Applicable"]
    equity_program_dictionary = {designation[i]: categories[i] for i in range(len(designation))}
    data = {"Whether Registry Is Seeking Boston Equity Program": list(equity_program_dictionary.keys()),
            "Number of Registries": list(equity_program_dictionary.values())}
    df = pd.DataFrame(data)
    st.header("Boston Cannabis Equity Program")
    # https://altair-viz.github.io/user_guide/generated/toplevel/altair.Chart.html
    bar_chart = (alt.Chart(df, title="Number of Registries Seeking Boston Equity Program")
                 .mark_bar(color="blue")  # making sure the graph is a bar chart and has blue bars
                 # line below is naming the axes
                 .encode(x="Whether Registry Is Seeking Boston Equity Program", y="Number of Registries")
                 .properties(width=600))  # setting the width of the chart to 600
    # https://docs.streamlit.io/library/api-reference/charts/st.altair_chart
    # sets font size of title and sets the title at the middle of the chart
    st.altair_chart(bar_chart.configure_title(fontSize=20, anchor="middle"))


# appendix contains information which users can read if confused
def appendix():
    st.header("Appendix")
    st.markdown("**License Status** (https://masscannabiscontrol.com/applicants-licensees/)")
    st.markdown("**Inactive License**: license is still in the process of becoming active")
    st.markdown("**Active License**: license is active and being used")
    st.markdown("**Expired License**: license is expired")
    st.markdown("**Deleted License**: license is deleted")
    st.write("")
    st.markdown("**License Categories** (https://masscannabiscontrol.com/license-types/#retailer)")
    st.markdown("**Retail License**: license allows for purchasing, transporting, and selling marijuana")
    st.markdown("**Courier License**: license allows for delivery of marijuana directly to consumers and patients")
    st.markdown("**Co-Located License**: license allows for the sharing of a registry")
    st.markdown("**Operator License**: license allows for purchasing marijuana products and sell and deliver to "
                "consumers")
    st.markdown("**TestLab License**: license allows for performing tests on cannabis products")
    st.markdown("**Manufact License**: license allows for manufacturing marijuana products and transfer them to "
                "establishments but not to consumers")
    st.markdown("**Transport License**: license allows for transporting cannabis products")
    st.markdown("**Cultivate License**: license allows for cultivating cannabis and transfer marijuana to other "
                "establishments but not to consumers")
    st.markdown("**Medical License**: license allows for marijuana to be used for medical purposes")
    st.write("")
    st.markdown("**Boston Equity Program** (https://www.boston.gov/departments/economic-development/cannabis-equity-program)")
    st.markdown("**Boston Cannabis Equity Program**: The Boston Cannabis Equity Program designates qualified licensees "
                "as Certified Boston Equity Applicants and provides access to financial and technical assistance.")

# main function
def main():
    app_license_status_output(app_license_status())
    longitude_and_latitude()
    app_license_category_output(app_license_category())
    vicinity()
    equity_program_designation_output(equity_program_designation())
    appendix()


main()
