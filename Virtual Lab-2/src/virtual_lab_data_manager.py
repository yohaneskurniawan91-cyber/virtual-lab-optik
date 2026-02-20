import os
import pandas as pd
import requests
import json
from openpyxl import Workbook

class DataManager:
    @staticmethod
    def save_data_unified(data, module_name):
        # Save data to local Excel file
        local_file_path = os.path.join("Hasil_Praktikum", module_name.replace(" ", "_") + ".xlsx")
        DataManager.save_to_excel(data, local_file_path)

        # Sync data with Google Sheets
        success, msg = DataManager.sync_with_google_sheets(data, module_name)
        return success, msg

    @staticmethod
    def save_to_excel(data, file_path):
        df = pd.DataFrame(data)
        df.to_excel(file_path, index=False)

    @staticmethod
    def sync_with_google_sheets(data, module_name):
        # Load Google Apps Script endpoint from config
        with open("config/db_config.json") as config_file:
            config = json.load(config_file)
            endpoint = config["endpoint"]

        # Prepare data for sending
        payload = {
            "module_name": module_name,
            "data": data
        }

        try:
            response = requests.post(endpoint, json=payload)
            response.raise_for_status()
            return True, "Data synced successfully with Google Sheets."
        except requests.exceptions.RequestException as e:
            return False, f"Failed to sync data: {str(e)}"

    @staticmethod
    def get_profile():
        # Placeholder for fetching user profile information
        # This should be replaced with actual implementation
        return {"name": "User", "nim": "123456"}