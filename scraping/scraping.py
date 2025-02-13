import requests
import json
import os
import sys

def get_apps():
    """Uses https://api.steampowered.com/ISteamApps/GetAppList/v2/ to get active list of all apps on steam store
    """
    url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"


    if not os.path.exists("data/apps.json"):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                apps = response.json()
                with open("data/apps.json", "w") as file:
                    json.dump(apps, file)
                return apps
            else:
                print("Error: ", response.status_code)
                return None

        except requests.exceptions.RequestException as e:
            print("Error: ", e)
            return None
    else:
        with open("data/apps.json", "r") as file:
            apps = json.load(file)
        return apps

def get_app_details(id):
    """Uses https://store.steampowered.com/api/appdetails/?appids= to get details of a specific app
    """
    url = "http://store.steampowered.com/api/appdetails/?appids=" + str(id)

    try:
        response = requests.get(url)
        if response.status_code == 200:
            app = response.json()
            return app
        elif response.status_code == 429:
                sys.exit("Error: 429")
        else:
            print("Error: ", response.status_code)
            return None

    except requests.exceptions.RequestException as e:
        print("Error: ", e)
        return None


def main():
    apps = get_apps()
    to_delete = []
    apps_details = []
    if apps:
        for app in apps["applist"]["apps"]:
            id = app["appid"]
            name = app["name"]
            if name == "" or id is None: #Deletes garbage/empty apps
                to_delete.append(app)

        for app in to_delete:
            apps["applist"]["apps"].remove(app)

        for app in apps["applist"]["apps"]:
            id = app["appid"]
            if app["name"].startswith(str(sys.argv[1])):
                app_details = get_app_details(id)

                if app_details:
                    print("Geting App Name: ", app["name"])
                    apps_details.append(app_details)
            
        if not os.path.exists("data/apps_details.json"):
            with open("data/apps_details.json", "w") as file:
                json.dump(apps_details, file)
        else:
            with open("data/apps_details.json", "r") as file:
                file_content = json.load(file)
            file_content.append(apps_details)
            with open("data/apps_details.json", "w") as file:
                json.dump(file_content, file)


if __name__ == "__main__":
    main()
