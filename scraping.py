import requests
import json

def get_apps():
    """Uses https://api.steampowered.com/ISteamApps/GetAppList/v2/ to get active list of all apps on steam store
    """
    url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            apps = response.json()
            return apps
        else:
            print("Error: ", response.status_code)
            return None

    except requests.exceptions.RequestException as e:
        print("Error: ", e)
        return None

def get_app_details(id):
    """Uses https://store.steampowered.com/api/appdetails/?appids= to get details of a specific app
    """
    url = "http://store.steampowered.com/api/appdetails/?appids=" + str(id)

    try:
        response = requests.get(url)
        if response.status_code == 200:
            app = response.json()
            return app
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
                print("Deleting AppId: ", id)
                to_delete.append(app)

        for app in to_delete:
            apps["applist"]["apps"].remove(app)

        for app in apps["applist"]["apps"]:
            id = app["appid"]
            app_details = get_app_details(id)
            if app_details:
                apps_details.append(app_details)
            
        with open("apps.json", "w") as file:
            json.dump(apps, file)
        with open("apps_details.json", "w") as file:
            json.dump(apps_details, file)


if __name__ == "__main__":
    main()
