from selenium import webdriver
from pyshadow.main import Shadow
import time
import pandas as pd
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
import json
import os



class omni:
    def __init__(self, email, pswd):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")  # Activate headless mode
        self.chrome_options.add_argument("--disable-gpu")  # Disable GPU usage to prevent issues
        self.driver = webdriver.Chrome()
        self.shadow = Shadow(self.driver)
        self.id = email
        self.password = pswd
        self.current_directory = os.path.dirname(os.path.abspath(__file__))
        self.quarter_file_path = os.path.join(self.current_directory, 'data', 'quarter.json')

    def test_login(self):
        self.driver.get("https://qaomni.annalect.com/login")
        self.driver.maximize_window()
        username = self.shadow.find_element("#username")
        signup_btn = self.shadow.find_element("#eid-login-btn")
        password = self.shadow.find_element("#password")
        username.send_keys(self.id)
        signup_btn.click()
        time.sleep(10)
        password.send_keys(self.password)
        signup_btn.click()
        time.sleep(40)





    def test_change_client(self):

        parent_all_tools = self.shadow.find_element("portal-app-container")
        parent1_client = self.shadow.find_element(parent_all_tools, "portal-client-selection-menu")
        parent2_client = self.shadow.find_element(parent1_client, "portal-client-button[aria-haspopup='listbox']")
        client_btn = self.shadow.find_element(parent2_client,".button.is-rounded.is-text.is-capitalized.is-size-3.has-text-weight-semibold")
        client_btn.click()
        time.sleep(1)
        search = self.shadow.find_element(parent1_client, ".input")
        search.send_keys("Omni QA Client")
        dropdown_item = self.shadow.find_element(parent1_client, ".dropdown-item")
        dropdown_item.click()
        time.sleep(15)

    def test_ae(self):
        time.sleep(10)
        parent_all_tools = self.shadow.find_element("portal-app-container")
        parent1_all_tools = self.shadow.find_element(parent_all_tools, "portal-nav-menu")
        parent2_all_tools = self.shadow.find_element(parent1_all_tools, "omni-nav-menu")
        all_tools = self.shadow.find_element(parent2_all_tools, "omni-style:nth-child(1) > nav:nth-child(1) > div:nth-child(2) > ul:nth-child(1) > div:nth-child(1) > portal-all-tools:nth-child(1) > li:nth-child(1) > omni-tooltip:nth-child(1) > div:nth-child(1) > a:nth-child(1) > omni-icon:nth-child(1)")
        all_tools.click()
        parent_ae = self.shadow.find_element(parent_all_tools, "portal-nav-menu")
        parent1_ae = self.shadow.find_element(parent_ae, "omni-nav-menu")
        parent2_ae = self.shadow.find_element(parent1_ae, "portal-all-tools")
        audience_explorer = self.shadow.find_element(parent2_ae, "a[title='Audience Explorer (Omni)']")
        audience_explorer.click()
        time.sleep(40)

    def test_explore_audience(self):
        with open(self.quarter_file_path, "r") as json_file:
            json_data = json.load(json_file)
            quarter_value = json_data["quarter"]
            filenames = json_data['filenames']
        iframe_parent = self.shadow.find_element("portal-app-container")
        iframe_parent1 = self.shadow.find_element(iframe_parent, "portal-iframe-container")
        iframe_parent2 = self.shadow.find_element(iframe_parent1, "portal-iframe-element[class='  ']")
        iframe_parent3 = self.shadow.find_element(iframe_parent2, "omni-style")
        iframe = self.shadow.find_element(iframe_parent3, "iframe")
        self.driver.switch_to.frame(iframe)
        parent_create_new_aud = self.shadow.find_element("view-landing")
        parent1_create_new_aud = self.shadow.find_element(parent_create_new_aud, "ae-create-audience")
        create_new_aud_btn = self.shadow.find_element(parent1_create_new_aud,
                                                      "button[class='button is-primary create-audience-button   ']")
        create_new_aud_btn.click()
        time.sleep(1)
        project_dropdown_parent = self.shadow.find_element(parent1_create_new_aud, "ae-dropdown[class='fadeInUp']")
        project_dropdown = self.shadow.find_element(project_dropdown_parent, ".button.dropdown__button")
        project_dropdown.click()

        project_dropdown_search = self.shadow.find_element(project_dropdown_parent, "#search")

        for filename in filenames:

            try:
                project_dropdown_search.send_keys(filename)
                project_dropdown_search_result = self.shadow.find_element(project_dropdown_parent,
                                                                          " omni-style:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)")
                project_dropdown_search_result.click()

            except Exception as e:
                cancel_mega_menu = self.shadow.find_element(".button.is-text.is-small")
                cancel_mega_menu.click()
                view = self.shadow.find_element("view-criteria-builder")
                view_project_dropdown = self.shadow.find_element(view, " omni-style:nth-child(1) > omni-tile:nth-child(1) > header:nth-child(1) > section:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > ae-dropdown:nth-child(2)")
                view_project_dropdown.click()
                time.sleep(5)
                dropdown_search = self.shadow.find_element(view_project_dropdown, "#search")
                dropdown_search.send_keys(filename)
                time.sleep(5)
                dropdown_item = self.shadow.find_element(view_project_dropdown, "#dropdown-menu > div > div.dropdown-list > div:nth-child(1)")
                dropdown_item.click()

            time.sleep(30)

            search_bar_parent1 = self.shadow.find_element("view-criteria-builder")

            search_bar_parent2 = self.shadow.find_element(search_bar_parent1, "cb-search-bar[type='megaMenu']")

            data = pd.read_csv("AE_data.csv")
            search_data_column = "search_phrase"
            search_phrases = data['search_phrase'].tolist()
            modified_list = [string.replace(" ", "").lower() for string in search_phrases]
            for quarter in quarter_value:
                failed_search = []

                quarter_dropdown = self.shadow.find_element(search_bar_parent1, ".time-period-dropdown")
                try:
                    quarter_dropdown.click()
                except ElementClickInterceptedException:
                    # cancel_mega_menu_parent1 = self.shadow.find_element("cb-mega-menu")
                    cancel_mega_menu = self.shadow.find_element(".button.is-text.is-small")
                    cancel_mega_menu.click()
                    quarter_dropdown.click()
                    time.sleep(20)

                quarter_search = self.shadow.find_element(quarter_dropdown, "#search")
                quarter_search.send_keys(quarter)
                time_period_search_result = self.shadow.find_element(quarter_dropdown, ".dropdown-option")
                time_period_search_result.click()
                time.sleep(40)
                for index, row in data.iterrows():
                    search_bar = self.shadow.find_element(search_bar_parent2, "#criteria-builder-toolbar-search-input")
                    search_button = self.shadow.find_element(search_bar_parent2,
                                                             ".button.is-small.is-primary.dynamic-search-button")
                    search_data = row[search_data_column]
                    search_bar.send_keys(search_data)
                    search_button.click()
                    time.sleep(7)
                    try:
                        parent1 = self.shadow.find_element("view-criteria-builder")
                        no_result_div = self.shadow.find_element(parent1, ".no-results-info")
                    except ElementNotVisibleException:
                        search_result = self.shadow.find_elements(".attribute-item span[slot='invoker']")
                        for result in search_result:
                            result_text = result.text
                            actual_text = result_text
                            result_text = result_text.replace(" ", "").lower()
                            if result_text in modified_list:
                                failed_search.append(actual_text)


                    clear_search_icon_parent = self.shadow.find_element(search_bar_parent2,
                                                                        ".is-size-3.remove-search-term")
                    clear_search_icon = self.shadow.find_element(clear_search_icon_parent, "div[part='icon']")
                    clear_search_icon.click()

                if failed_search:
                    # Remove duplicates from the failed_search list
                    failed_search = list(set(failed_search))
                    file_name = f"{quarter}_found_searches.csv"
                    file_path = os.path.join(self.current_directory, 'search_results', file_name)
                    new_column_name = filename

                    if not os.path.isfile(file_path):
                        failed_df = pd.DataFrame(failed_search, columns=[new_column_name])
                        failed_df.to_csv(file_path, index=False)
                    else:
                        # Load existing CSV into a DataFrame
                        existing_df = pd.read_csv(file_path)

                        # Create a DataFrame for current failed searches and merge it with the existing DataFrame
                        new_data = pd.DataFrame({new_column_name: failed_search})
                        existing_df = pd.concat([existing_df, new_data], axis=1)

                        # Save the updated DataFrame back to the CSV file
                        existing_df.to_csv(file_path, index=False)













obj = omni("adminqa.user@annalect.com", "]1uMo%1R35i0kS")
obj.test_login()
# obj.test_change_client()
obj.test_ae()
obj.test_explore_audience()
# obj.test_build_your_audience()


