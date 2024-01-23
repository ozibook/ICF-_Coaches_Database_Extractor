import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import os
import streamlit as st

# Helper function to save data to CSV file
def save_to_csv(data):
    if os.path.exists('raw_data.csv'):
        with open('raw_data.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)
    else:
        with open('raw_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)


save_to_csv([["Coach_Name", "Website", "Email", "Phone", "Location", "Rate", "Coaching Themes", "Coaching Methods", "Willing to Relocate", "Special Rates", "Fee Range", "Type of Client", "Organizational Client Types",
                            "Coached Organizations", "Industry Sectors Coached", "Positions Held", "Has Prior Experience Delivering Coach Skills Training to Managers/Leaders", "Degrees", "Gender", "Age", "Fluent Languages", "Can Provide"]])

def check_checkbox_ifnot(id):
    """
    Checks a checkbox on a web page if it is not already checked.

    Parameters:
    - id: The ID of the checkbox.
    """
    checkbox = browser.find_element(By.XPATH, f"//input[@id='{id}']")
    is_checked = checkbox.is_selected()
    if not is_checked:
        browser.execute_script(f"document.getElementById('{id}').click();")

def getInnerTextFromId(id):
    """
    Retrieves the inner text content of an HTML element with the specified ID on a web page.

    Parameters:
    - id: The ID of the HTML element.

    Returns:
    - Inner text content of the HTML element or 'N/A' if not found.
    """
    elem = browser.find_element(By.ID, id)
    if elem:
        return elem.text
    return 'N/A'

def get_data_from_table():
    """
    Extracts data from an HTML table on a web page.

    Returns:
    - A list containing values from the table.
    """
    try:
        element = browser.find_element(By.CLASS_NAME, table_class_name)
        table_data = []
        t_body = element.find_element(By.TAG_NAME, "tbody")
        childrens = t_body.find_elements(By.TAG_NAME, "tr")
        for children in childrens:
            value = ''
            try:
                div_childs = children.find_elements(By.TAG_NAME, "div")
                for i, div in enumerate(div_childs):
                    if i == 0:
                        value += div.text
                    else:
                        value += ',' + div.text
            except Exception as e:
                pass
            table_data.append(value)
        return table_data
    except Exception as e:
        return []

# Helper function to get data from a coach profile tab
def get_data_from_tab(val):
    """
    Opens a new window with a coach profile page, extracts relevant data, appends it to `csv_data`, and closes the window.

    Parameters:
    - val: The value associated with the coach profile page.
    """
    global csv_data

    # Switch to a new window
    browser.switch_to.new_window()

    browser.switch_to.window(browser.window_handles[-1])

    # Open the coach profile page
    browser.execute_script(
        f"window.open('https://apps.coachingfederation.org/eweb/CCFDynamicPage.aspx?webcode=ccfcoachprofileview&coachcstkey={val}')")
    browser.close()
    browser.switch_to.window(browser.window_handles[-1])

    # Wait for the coach profile page to load
    wait.until(EC.presence_of_element_located((By.ID, coach_name_id)))

    # Append data to the CSV
    csv_data.append([
                        getInnerTextFromId(coach_name_id),
                        getInnerTextFromId(website_link_id),
                        getInnerTextFromId(email_id),
                        getInnerTextFromId(phone_id),
                        getInnerTextFromId(address_id),
                        getInnerTextFromId(coach_fee),
                    ] + get_data_from_table())

    # Close the coach profile window
    browser.close()

    # Switch back to the main window
    browser.switch_to.window(browser.window_handles[-1])
    pass

# Helper function to iterate through coach profile cards
def cards_iterate(step=1):
    """
    Iterates through coach profile cards on a web page, extracting data using `get_data_from_tab`.

    Parameters:
    - step: The index of the coach profile card to start iterating from.
    """
    try:
        element = browser.find_element(By.XPATH, f"//div[@class='{div_cards_class_name}'][position()={step}]")
        if element:
            check = element.find_element(By.TAG_NAME, 'input')
            val = check.get_attribute('value')

            # Get data from the coach profile tab
            get_data_from_tab(val)

            # Wait for the coach profile cards to reload
            wait.until(EC.presence_of_element_located((By.ID, 'cards')))

            # Recursively call the function for the next card
            cards_iterate(step + 1)
    except Exception as e:
        return
    return

# Helper function to iterate through pages
def iterate_page(page=1):
    """
    Iterates through pages of coach profiles on a web page, calling `cards_iterate` for each page.

    Parameters:
    - page: The page number to start iterating from.
    """
    global csv_data
    try:
        if page > 1:

            # If on a page greater than 1, click the next page button
            current_path = browser.find_element(By.CSS_SELECTOR, 'a.item.active')
            page = current_path.get_attribute('data-value')
            page = int(page)

            next_path = browser.find_element(
                By.XPATH, f"//a[@class='item'][@data-value={page + 1}]")
            disabled_class = next_path.get_attribute('class')
            if 'disabled' in disabled_class:
                return
            next_path.click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.ID, 'cards')))

        csv_data = []

        # Start iterating through coach profile cards on the current page
        cards_iterate()
        # save data
        save_to_csv(csv_data)

        iterate_page(page + 1)
    except Exception as e:
        return

def Driver(location, ):
    """
    Main driver function that orchestrates the automation process. It interacts with the webpage, filters data, and initiates data extraction by calling other functions.

    Parameters:
    - location: The location to filter coach profiles.

    Returns:
    - A string indicating the completion status.
    """

    # Helper function to check and click checkboxes if not already checked
    check_checkbox_ifnot(acc)
    check_checkbox_ifnot(pcc)
    check_checkbox_ifnot(mcc)

    # Click the location filter button
    location_filter_btn = browser.find_element(By.XPATH, f"//button[@id='{location_btn_id}']")
    if location_filter_btn:
        browser.execute_script(
            f"document.getElementById('{location_btn_id}').click();")

    time.sleep(2)

    # Select the location from the modal
    location_btn = browser.find_element(By.XPATH, f"//button[@data-display='{location}']")
    if location_btn:
        location_btn.click()

    # Close the location modal
    location_modal = browser.find_element(By.XPATH, f"//div[@id='{location_modal_id}']")
    if location_modal:
        browser.execute_script(f"$('#{location_modal_id}').modal('hide');")

    time.sleep(2)

    # Helper function to get text from an element by its ID

    # Check if coach profile cards are present on the page
    if browser.find_element(By.XPATH, "//div[@id='cards']"):
        csv_data = []

        # Start iterating through pages
        iterate_page()

    time.sleep(5)  # wait #TODO CHANGE TO 50

    # Close the browser
    browser.quit()
    return "Done"

def Runner(Country, Country_Code):

    """
    Runs the automation process, extracts coach profile data, and performs additional data cleaning.

    Parameters:
    - Country: The location to filter coach profiles.
    - Country_Code: The country code used for updating phone numbers.

    Returns:
    - A string indicating the completion status.
    """

    Driver(location=Country)
    print("driver done")
    df = pd.read_csv('raw_data.csv')
    # Updating Name
    # Split the 'Coach_Name' column into 'FirstName' and 'LastName' and removing Main column
    df[['Coach', 'Credentials']] = df['Coach_Name'].str.split(',', n=1 ,expand=True)
    df['Coach'] = df['Coach'].str.replace(r'(Mr\.|Ms\.|Mrs\.)\s*', '', regex=True)
    df['Coach'] = df['Coach'].str.title()
    df[['First_Name', 'Last_Name']] = df['Coach'].str.split(expand=True, n=1)

    #Adding hierarchy
    df['Credentials'] = df.Credentials.str.replace(' ACC, PCC','PCC')


    # Updating Phone number
    value = str(Country_Code)
    df['Phone'] = df['Phone'].astype(str).str.replace(rf'(\+{value}|{value})\s*', '', regex=True)
    df['Phone'] = value + df['Phone']

    #Adding Country
    df['Country'] = Country

    df.to_csv(f'{Country}.csv',index=False)
    st.success("Extraction Completed")

    return 'Done'


# Define IDs and other information for various elements
acc = 'credential-acc'
pcc = 'credential-pcc'
mcc = 'credential-mcc'
location_btn_id = 'add-location'
location_modal_id = 'locations-modal'
div_cards_class_name = 'ui fluid link  card'
table_class_name = 'ui.unstackable.very.basic.definition.table'

coach_name_id = 'coachName'
website_link_id = 'webSiteLink'
email_id = 'emailLink'
phone_id = 'phoneLbl'
address_id = 'addressLbl'
coach_fee = "coachFee"


# ---------------------------------------------------------------------
# Set up the Chrome driver
browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# Open the target website
# the page for filters
browser.get('https://apps.coachingfederation.org/eweb/CCFDynamicPage.aspx?webcode=ccfsearch&site=icfapp')
# Wait for the page to load
wait = WebDriverWait(browser, 10)
wait.until(EC.presence_of_element_located((By.ID, acc)))
wait.until(EC.presence_of_element_located((By.ID, location_btn_id)))

