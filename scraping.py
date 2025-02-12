import requests
import json
import os

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
                #print("Deleting AppId: ", id)
                to_delete.append(app)

        for app in to_delete:
            apps["applist"]["apps"].remove(app)

        print("Total Apps: ", len(apps["applist"]["apps"]))

        for app in apps["applist"]["apps"]:
            id = app["appid"]
            if app["name"].startswith("a"): #Change manual to avoid 429 error (a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,0,1,2,3,4,5,6,7,8,9)
                app_details = get_app_details(id)
                if app_details:
                    print("Geting App Name: ", app["name"])
                    apps_details.append(app_details)
            
        with open("apps.json", "w") as file:
            json.dump(apps, file)
        if not os.path.exists("apps_details.json"):
            with open("apps_details.json", "w") as file:
                json.dump(apps_details, file)
        else:
            with open("apps_details.json", "r") as file:
                file_content = json.load(file)
            file_content.update(apps_details)
            with open("apps_details.json", "w") as file:
                json.dump(file_content, file)


if __name__ == "__main__":
    main()
