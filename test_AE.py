from selenium import webdriver
from pyshadow.main import Shadow
import time
import pandas as pd
from selenium.common.exceptions import ElementNotVisibleException
import json
import os



class omni:
    def __init__(self, email, pswd):
        self.driver = webdriver.Chrome()
        self.shadow = Shadow(self.driver)
        self.id = email
        self.password = pswd
        self.current_directory = os.path.dirname(os.path.abspath(__file__))
        self.quarter_file_path = os.path.join(self.current_directory, 'data', 'quarter.json')

    def test_login(self):
        self.driver.get("https://devomni.annalect.com/login")
        self.driver.maximize_window()
        username = self.shadow.find_element("#username")
        signup_btn = self.shadow.find_element("#eid-login-btn")
        password = self.shadow.find_element("#password")
        username.send_keys(self.id)
        signup_btn.click()
        time.sleep(2)
        password.send_keys(self.password)
        signup_btn.click()
        time.sleep(20)

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
        parent_all_tools = self.shadow.find_element("portal-app-container")
        parent1_all_tools = self.shadow.find_element(parent_all_tools, "omni-nav-menu")
        all_tools = self.shadow.find_element(parent1_all_tools, " omni-style:nth-child(1) > nav:nth-child(1) > div:nth-child(2) > ul:nth-child(1) > div:nth-child(1) > portal-all-tools:nth-child(1) > li:nth-child(1) > omni-tooltip:nth-child(1) > div:nth-child(1) > a:nth-child(1) > omni-icon:nth-child(1)")
        all_tools.click()
        parent_ae = self.shadow.find_element(parent_all_tools, "portal-nav-menu")
        parent1_ae = self.shadow.find_element(parent_ae, "omni-nav-menu")
        parent2_ae = self.shadow.find_element(parent1_ae, "portal-all-tools")
        audience_explorer = self.shadow.find_element(parent2_ae, " omni-style:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > a:nth-child(7) > p:nth-child(2)")
        audience_explorer.click()
        time.sleep(15)

    def test_explore_audience(self):
        iframe_parent = self.shadow.find_element("portal-app-container")
        iframe_parent1 = self.shadow.find_element(iframe_parent, "portal-iframe-container")
        iframe_parent2 = self.shadow.find_element(iframe_parent1, "portal-iframe-element[class='  ']")
        iframe_parent3 = self.shadow.find_element(iframe_parent2, "omni-style")
        iframe = self.shadow.find_element(iframe_parent3, "iframe")
        self.driver.switch_to.frame(iframe)
        parent_create_new_aud = self.shadow.find_element("view-landing")
        parent1_create_new_aud = self.shadow.find_element(parent_create_new_aud, "ae-create-audience")
        create_new_aud_btn = self.shadow.find_element(parent1_create_new_aud, "button[class='button is-primary create-audience-button   ']")
        create_new_aud_btn.click()
        time.sleep(1)
        project_dropdown_parent = self.shadow.find_element(parent1_create_new_aud, "ae-dropdown[class='fadeInUp']")
        project_dropdown = self.shadow.find_element(project_dropdown_parent, ".button.dropdown__button")
        project_dropdown.click()
        project_dropdown_search = self.shadow.find_element(project_dropdown_parent, "#search")
        project_dropdown_search.send_keys("NA_US -")
        project_dropdown_search_result = self.shadow.find_element(project_dropdown_parent, "#id-4491fd44-9e5e-11ee-9ca6-0a58a9feac02-0-text")
        project_dropdown_search_result.click()
        time.sleep(10)

    def test_build_your_audience(self):

        with open(self.quarter_file_path, "r") as json_file:
            json_data = json.load(json_file)
        quarter_value = json_data["quarter"]

        failed_search = []
        search_bar_parent1 = self.shadow.find_element("view-criteria-builder")
        # no_result_div_parent = self.shadow.find_element(search_bar_parent1, "cb-mega-menu")

        search_bar_parent2 = self.shadow.find_element(search_bar_parent1, "cb-search-bar[type='megaMenu']")

        # quarter_dropdown = self.shadow.find_element(search_bar_parent1, ".time-period-dropdown")
        # quarter_dropdown.click()
        # quarter_search = self.shadow.find_element(quarter_dropdown, "#search")

        data = pd.read_csv("AE_data.csv")
        search_data_column = 'search_phrase'
        for quarter in quarter_value:
            quarter_dropdown = self.shadow.find_element(search_bar_parent1, ".time-period-dropdown")
            quarter_dropdown.click()
            quarter_search = self.shadow.find_element(quarter_dropdown, "#search")
            quarter_search.send_keys(quarter)
            time_period_search_result = self.shadow.find_element(quarter_dropdown, ".dropdown-option")
            time_period_search_result.click()
            time.sleep(10)
            for index, row in data.iterrows():
                search_bar = self.shadow.find_element(search_bar_parent2, "#criteria-builder-toolbar-search-input")
                search_button = self.shadow.find_element(search_bar_parent2, ".button.is-small.is-primary.dynamic-search-button")
                search_data = row[search_data_column]
                search_bar.send_keys(search_data)
                time.sleep(2)
                search_button.click()
                time.sleep(4)
                try:
                    parent1 = self.shadow.find_element("view-criteria-builder")
                    no_result_div = self.shadow.find_element(parent1, ".no-results-info")
                except ElementNotVisibleException:
                    failed_search.append(search_data)

                clear_search_icon_parent = self.shadow.find_element(search_bar_parent2, ".is-size-3.remove-search-term")
                clear_search_icon = self.shadow.find_element(clear_search_icon_parent, "div[part='icon']")
                clear_search_icon.click()

            if failed_search:
                failed_df = pd.DataFrame(failed_search, columns=[search_data_column])
                file_name = f"{quarter}_failed_searches.csv"
                file_path = os.path.join(self.current_directory, 'search_results', file_name)
                failed_df.to_csv(file_path, index=False)

        self.driver.quit()








obj = omni("adminqa.user@annalect.com", "e-A)7+T8IW3z1[")
obj.test_login()
obj.test_change_client()
obj.test_ae()
obj.test_explore_audience()
obj.test_build_your_audience()


