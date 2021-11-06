try:
    import requests, json, threading, time
    from colorama import Fore, init
except ImportError:
    print("Please intall requests\nOpen cmd and type : pip install requests")
    time.sleep(999)

class PayoutRoblox:
        
    def __init__(self, cookie):
        self.userid = None
        self.name = None
        # self.groups = []
        self.csrf = None
        self.cookie = cookie
        self.head = None
    
    def getting_csrf(self):
        # requests.Session(), don't needed anymore lol, just didn't know how to make a thing but nvm
        cookie = {"Cookie": f".ROBLOSECURITY={self.cookie}"}
        no = requests.post("https://auth.roblox.com/v2/login", headers=cookie)
        csrf = no.headers["x-csrf-token"]
        self.csrf = csrf
        self.head = {"Cookie": f".ROBLOSECURITY={self.cookie}", "X-CSRF-TOKEN": self.csrf}

    def get_group_ids(self, percent):
        user_id = requests.get("http://www.roblox.com/mobileapi/userinfo", headers=self.head)
        usr1 = user_id.json()
        usr1 = usr1["UserID"]
        usr = str(usr1)
        self.userid = usr
        
        # getting the groups
        
        groupids = f"https://groups.roblox.com/v2/users/{self.userid}/groups/roles"
        meth = requests.get(groupids, headers=self.head)
        groups = meth.json()
        for group in groups["data"]:
            xs = (group["group"]["id"])
            
            data = {
                 "PayoutType": "Percentage",
                 "Recipients": [
                 {
                "recipientId": self.userid,
                "recipientType": "User",
                 "amount": percent
                    }
                ]
            }
            
            posting = requests.post(f"https://groups.roblox.com/v1/groups/{str(xs)}/payouts", headers=self.head, json=data)
            
            init(autoreset=True)
            if posting.status_code == 200:
                print(Fore.GREEN + f"Successfully paid out from group : {str(xs)}")
            elif posting.status_code == 403:
                print(Fore.RED + f"Problem with cookie, please check your cookie and this group id : {str(xs)}")
            elif posting.status_code == 400:
                print(Fore.YELLOW + f"This group : {str(xs)} have 0 robux.")
            
            
            
with open("cookies.txt", "r") as cookies:
    string = int(input("Percentage to paid out from all the groups : "))
    for cookie in cookies:
        # print(PayoutRoblox.getting_csrf(cookie))
        data = PayoutRoblox(cookie)
        data.getting_csrf()
        data.get_group_ids(string)
        
        
    
