import pandas as pd
import os
from datetime import datetime
import json
from urllib.request import urlopen
import time
import schedule

project_name = "COVID-19-HK"
project_dir = os.getcwd().split(project_name)[0]
project_dir = os.path.join(project_dir, project_name)


def read_json(path):
    with open(path, mode="r") as f:
        json_file = json.load(f)
    return json_file


def save_key_nums():
    key_nums_url = 'https://chp-dashboard.geodata.gov.hk/covid-19/data/keynum.json'
    key_nums_folder = os.path.join(project_dir, "static/data/key_nums_data/")
    response = urlopen(key_nums_url,timeout=60*5)
    key_nums_json = json.loads(response.read())

    timestamp = key_nums_json['As_of_date']

    timestamp = int(str(timestamp)[:10])
    date_time = datetime.fromtimestamp(timestamp)

    # date_format = "%Y/%m/%d"
    # date_time_str = date_time.strftime(date_format)
    # key_nums_json['As_of_date'] = date_time_str

    date_str = date_time.strftime("%Y_%m_%d")
    file_name = date_str + "_key_nums.json"
    save_file_path = os.path.join(key_nums_folder, file_name)
    with open(save_file_path, 'w') as f:
        json.dump(key_nums_json, f, indent=4)

    file_name = "latest" + "_key_nums.json"
    save_file_path = os.path.join(key_nums_folder, file_name)
    with open(save_file_path, 'w') as f:
        json.dump(key_nums_json, f, indent=4)


def update_latest_confirm_death():
    date_format = "%Y/%m/%d"
    file_path = "static/data/confirmed_death_data/latest_data.json"
    latest_file_path = os.path.join(project_dir, file_path)

    with open(latest_file_path) as f:
        confirm_death_dict = json.load(f)

    key_nums_file_path = os.path.join(
        project_dir, "static/data/key_nums_data/latest_key_nums.json")
    key_nums_json = read_json(key_nums_file_path)

    timestamp = key_nums_json['As_of_date']
    timestamp = int(str(timestamp)[:10])
    date_time = datetime.fromtimestamp(timestamp)
    date_format = "%Y/%m/%d"
    date_time_str = date_time.strftime(date_format)

    # key_nums_json

    new_death = key_nums_json['Death']-key_nums_json['P_Death']
    new_comfirm = key_nums_json['Confirmed_Delta'] + \
        key_nums_json['RAT_Positive_Delta']

    date_list = confirm_death_dict['Date']

    if date_time_str not in date_list:

        confirm_death_dict['Date'] = confirm_death_dict['Date'] + \
            [date_time_str]
        confirm_death_dict['Confirmed'] = confirm_death_dict['Confirmed'] + [new_comfirm]
        confirm_death_dict['Death'] = confirm_death_dict["Death"] + [new_death]

        print(f"INFO: Date {date_time_str} Comfirmed and Death Created !")

    else:

        index = confirm_death_dict['Date'].index(date_time_str)
        old_death = confirm_death_dict['Death'][index]
        old_comfirm = confirm_death_dict['Confirmed'][index]

        if new_death == 0:

            print(f"INFO: Skip {date_time_str} Death")
            confirm_death_dict['Confirmed'][index] = new_comfirm

        else:
            print(f"INFO: Date {date_time_str} Comfirmed and Death Updated !")
            confirm_death_dict['Confirmed'][index] = new_comfirm
            confirm_death_dict['Death'][index] = new_death

    with open(latest_file_path, 'w') as f:
        json.dump(confirm_death_dict, f, indent=4)

    date_time_str = date_time_str.replace('/', '_')
    file_path = f"static/data/confirmed_death_data/{date_time_str}_data.json"
    latest_file_path = os.path.join(project_dir, file_path)
    with open(latest_file_path, 'w') as f:
        json.dump(confirm_death_dict, f, indent=4)


def save_chi_building_data():
    data_url = "http://www.chp.gov.hk/files/misc/building_list_chi.csv"
    building_df = pd.read_csv(data_url)
    total = len(building_df)
    building_df = building_df.groupby("地區").size().reset_index(name="Count")
    building_df.columns = ['District', 'Count']
    building_df = building_df.sort_values(by="Count", ascending=True)
    building_dict = building_df.to_dict("list")
    building_dict['total'] = total
    building_data_folder = os.path.join(
        project_dir, "static/data/building_data/")
    today = datetime.today()
    date_str = today.strftime("%Y_%m_%d")
    file_name = date_str + "_chi_buiding.json"
    save_file_path = os.path.join(building_data_folder, file_name)
    with open(save_file_path, mode='w', encoding="BIG5") as f:
        json.dump(building_dict, f, indent=4)

    file_name = "latest_chi_buiding.json"
    save_file_path = os.path.join(building_data_folder, file_name)
    with open(save_file_path, mode='w', encoding="BIG5") as f:
        json.dump(building_dict, f, indent=4)


def save_eng_building_data():
    data_url = "http://www.chp.gov.hk/files/misc/building_list_eng.csv"
    building_df = pd.read_csv(data_url)
    total = len(building_df)
    building_df = building_df.groupby(
        "District").size().reset_index(name="Count")
    building_df.columns = ['District', 'Count']
    building_df = building_df.sort_values(by="Count", ascending=True)
    building_dict = building_df.to_dict("list")
    building_dict['total'] = total
    building_data_folder = os.path.join(
        project_dir, "static/data/building_data/")
    today = datetime.today()
    date_str = today.strftime("%Y_%m_%d")
    file_name = date_str + "_eng_buiding.json"
    save_file_path = os.path.join(building_data_folder, file_name)
    with open(save_file_path, mode='w', encoding="BIG5") as f:
        json.dump(building_dict, f, indent=4)

    file_name = "latest_eng_buiding.json"
    save_file_path = os.path.join(building_data_folder, file_name)
    with open(save_file_path, mode='w', encoding="BIG5") as f:
        json.dump(building_dict, f, indent=4)


def get_current_date():
    today = datetime.today()
    today_str = today.strftime("%Y-%m-%d %H:%M:%S")
    return today_str


def detect_update():
    key_nums_url = 'https://chp-dashboard.geodata.gov.hk/covid-19/data/keynum.json'

    response = urlopen(key_nums_url)
    key_nums_json = json.loads(response.read())

    data_source_timestamp = key_nums_json['As_of_date']

    curr_json_path = os.path.join(
        project_dir, "static/data/key_nums_data/latest_key_nums.json")

    with open(curr_json_path, "r") as f:
        current_key_nums_json = json.load(f)

    my_source_timestamp = current_key_nums_json['As_of_date']

    return my_source_timestamp < data_source_timestamp


def main():
    print("INFO: Executed At:", get_current_date())
    save_key_nums()
    update_latest_confirm_death()
    save_eng_building_data()
    save_chi_building_data()


def job():
    print(get_current_date())


if __name__ == "__main__":
    # main()
    interval = 60*30
    main()
    while True:

        if detect_update():
            count_max = 10
            count = 0
            while count < count_max:

                main()
                print("INFO:Slepping")
                time.sleep(30*count)
                count += 1

        print("INFO:Slepping")
        time.sleep(interval)
        main()
