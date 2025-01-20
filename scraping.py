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

def main():
    apps = get_apps()
    to_delete = []
    if apps:
        for app in apps["applist"]["apps"]:
            id = app["appid"]
            name = app["name"]
            if name == "" or id is None: #Deletes garbage/empty apps
                print("Deleting AppId: ", id)
                to_delete.append(app)

        for app in to_delete:
            apps["applist"]["apps"].remove(app)
            
        with open("apps.json", "w") as file:
            json.dump(apps, file)


if __name__ == "__main__":
    main()
