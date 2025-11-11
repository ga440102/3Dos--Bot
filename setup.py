from aiohttp import ClientResponseError, ClientSession, ClientTimeout, BasicAuth
from aiohttp_socks import ProxyConnector
from fake_useragent import FakeUserAgent
from datetime import datetime
from colorama import *
import asyncio, json, pytz, re, os

wib = pytz.timezone('Asia/Jakarta')

class Dos:
    def __init__(self) -> None:
        self.BASE_API = "https://api.dashboard.3dos.io/api"
        self.PAGE_URL = "https://dashboard.3dos.io/"
        self.SITE_KEY = "6Lfp7N8qAAAAAGzZkHCJXV7mCHX25VuEeE1dh5Md"
        self.CAPTCHA_KEY = None
        self.HEADERS = {}
        self.proxies = []
        self.proxy_index = 0
        self.account_proxies = {}

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def log_status(self, action, status, message="", error=None):
        if status == "success":
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}Action :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {action} {Style.RESET_ALL}"
                f"{Fore.CYAN+Style.BRIGHT}Status :{Style.RESET_ALL}"
                f"{Fore.GREEN+Style.BRIGHT} {status.capitalize()} {Style.RESET_ALL}"
                f"{(Fore.MAGENTA+Style.BRIGHT + '- ' + Style.RESET_ALL + Fore.WHITE+Style.BRIGHT + message + Style.RESET_ALL) if message else ''}"
            )
        elif status == "failed":
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}Action :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {action} {Style.RESET_ALL}"
                f"{Fore.CYAN+Style.BRIGHT}Status :{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} {status.capitalize()} {Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                f"{Fore.YELLOW+Style.BRIGHT} {str(error)} {Style.RESET_ALL}"
            )
        elif status in ["retry", "waiting"]:
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}Action :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {action} {Style.RESET_ALL}"
                f"{Fore.CYAN+Style.BRIGHT}Status :{Style.RESET_ALL}"
                f"{Fore.YELLOW+Style.BRIGHT} {status.capitalize()} {Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {message} {Style.RESET_ALL}"
            )

    def welcome(self):
        print(
            f"""
        {Fore.GREEN + Style.BRIGHT}3Dos {Fore.BLUE + Style.BRIGHT}Auto BOT
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Rey? {Fore.YELLOW + Style.BRIGHT}<INI WATERMARK>
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
    def load_accounts(self):
        filename = "accounts.json"
        try:
            if not os.path.exists(filename):
                self.log(f"{Fore.RED}File {filename} Not Found.{Style.RESET_ALL}")
                return

            with open(filename, 'r') as file:
                data = json.load(file)
                if isinstance(data, list):
                    return data
                return []
        except json.JSONDecodeError:
            return []
        
    def load_captcha_key(self):
        try:
            with open("capmonster_key.txt", 'r') as file:
                captcha_key = file.read().strip()

            return captcha_key
        except Exception as e:
            return None
        
    def save_tokens(self, new_accounts):
        filename = "tokens.json"
        try:
            if os.path.exists(filename) and os.path.getsize(filename) > 0:
                with open(filename, 'r') as file:
                    existing_accounts = json.load(file)
            else:
                existing_accounts = []

            account_dict = {acc["email"]: acc for acc in existing_accounts}

            for new_acc in new_accounts:
                account_dict[new_acc["email"]] = new_acc

            updated_accounts = list(account_dict.values())

            with open(filename, 'w') as file:
                json.dump(updated_accounts, file, indent=4)

            self.log_status("Save Tokens", "success", "Tokens saved to file")

        except Exception as e:
            self.log_status("Save Tokens", "failed", error=e)
            return []
        
    async def load_proxies(self):
        filename = "proxy.txt"
        try:
            if not os.path.exists(filename):
                self.log(f"{Fore.RED + Style.BRIGHT}File {filename} Not Found.{Style.RESET_ALL}")
                return
            with open(filename, 'r') as f:
                self.proxies = [line.strip() for line in f.read().splitlines() if line.strip()]
            
            if not self.proxies:
                self.log(f"{Fore.RED + Style.BRIGHT}No Proxies Found.{Style.RESET_ALL}")
                return

            self.log(
                f"{Fore.GREEN + Style.BRIGHT}Proxies Total  : {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(self.proxies)}{Style.RESET_ALL}"
            )
        
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Failed To Load Proxies: {e}{Style.RESET_ALL}")
            self.proxies = []

    def check_proxy_schemes(self, proxies):
        schemes = ["http://", "https://", "socks4://", "socks5://"]
        if any(proxies.startswith(scheme) for scheme in schemes):
            return proxies
        return f"http://{proxies}"

    def get_next_proxy_for_account(self, account):
        if account not in self.account_proxies:
            if not self.proxies:
                return None
            proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
            self.account_proxies[account] = proxy
            self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return self.account_proxies[account]

    def rotate_proxy_for_account(self, account):
        if not self.proxies:
            return None
        proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
        self.account_proxies[account] = proxy
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return proxy
    
    def build_proxy_config(self, proxy=None):
        if not proxy:
            return None, None, None

        if proxy.startswith("socks"):
            connector = ProxyConnector.from_url(proxy)
            return connector, None, None

        elif proxy.startswith("http"):
            match = re.match(r"http://(.*?):(.*?)@(.*)", proxy)
            if match:
                username, password, host_port = match.groups()
                clean_url = f"http://{host_port}"
                auth = BasicAuth(username, password)
                return None, clean_url, auth
            else:
                return None, proxy, None

        raise Exception("Unsupported Proxy Type.")
    
    def mask_account(self, account):
        if "@" in account:
            local, domain = account.split('@', 1)
            mask_account = local[:3] + '*' * 3 + local[-3:]
            return f"{mask_account}@{domain}"

    def print_question(self):
        while True:
            try:
                print(f"{Fore.WHITE + Style.BRIGHT}1. Run With Proxy{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}2. Run Without Proxy{Style.RESET_ALL}")
                proxy_choice = int(input(f"{Fore.BLUE + Style.BRIGHT}Choose [1/2] -> {Style.RESET_ALL}").strip())

                if proxy_choice in [1, 2]:
                    proxy_type = (
                        "With" if proxy_choice == 1 else 
                        "Without"
                    )
                    print(f"{Fore.GREEN + Style.BRIGHT}Run {proxy_type} Proxy Selected.{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Please enter either 1  or 2.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1  or 2).{Style.RESET_ALL}")

        rotate_proxy = False
        if proxy_choice == 1:
            while True:
                rotate_proxy = input(f"{Fore.BLUE + Style.BRIGHT}Rotate Invalid Proxy? [y/n] -> {Style.RESET_ALL}").strip()
                if rotate_proxy in ["y", "n"]:
                    rotate_proxy = rotate_proxy == "y"
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter 'y' or 'n'.{Style.RESET_ALL}")

        return proxy_choice, rotate_proxy
    
    async def check_connection(self, proxy_url=None):
        connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
        try:
            async with ClientSession(connector=connector, timeout=ClientTimeout(total=10)) as session:
                async with session.get(url="https://api.ipify.org?format=json", proxy=proxy, proxy_auth=proxy_auth) as response:
                    response.raise_for_status()
                    self.log_status("Check Connection", "success", "Connection OK")
                    return True
        except (Exception, ClientResponseError) as e:
            self.log_status("Check Connection", "failed", error=e)
            return None
        
    async def solve_recaptcha(self, retries=5):
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=60)) as session:
                    
                    if self.CAPTCHA_KEY is None:
                        self.log_status("Captcha", "failed", error="Captcha Key Not Found")
                        return None

                    url = "https://api.capmonster.cloud/createTask"
                    data = json.dumps({
                        "clientKey": self.CAPTCHA_KEY,
                        "task": {
                            "type": "RecaptchaV3TaskProxyless",
                            "websiteURL": self.PAGE_URL,
                            "websiteKey": self.SITE_KEY,
                            "minScore": 0.9,
                            "pageAction": "login"
                        }
                    })
                    async with session.post(url=url, data=data) as response:
                        response.raise_for_status()
                        result_text = await response.text()
                        result_json = json.loads(result_text)

                        if result_json.get("errorId") != 0:
                            err_text = result_json.get("errorDescription", "Unknown Error")
                            
                            self.log_status("Captcha", "failed", error=err_text)
                            await asyncio.sleep(5)
                            continue

                        task_id = result_json.get("taskId")
                        self.log_status("Captcha", "success", f"Task Id: {task_id}")

                        for _ in range(30):
                            res_url = "https://api.capmonster.cloud/getTaskResult"
                            res_data = json.dumps({
                                "clientKey": self.CAPTCHA_KEY,
                                "taskId": task_id
                            })
                            async with session.post(url=res_url, data=res_data) as res_response:
                                res_response.raise_for_status()
                                res_result_text = await res_response.text()
                                res_result_json = json.loads(res_result_text)

                                if res_result_json.get("status") == "ready":
                                    recaptcha_token = res_result_json["solution"]["gRecaptchaResponse"]
                                    self.log_status("Captcha", "success", "Recaptcha Solved Successfully")
                                    return recaptcha_token
                                elif res_result_json.get("status") == "processing":
                                    self.log_status("Captcha", "waiting", "Captcha Not Ready")
                                    await asyncio.sleep(5)
                                    continue
                                else:
                                    break

            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    self.log_status("Captcha", "retry", f"Attempt {attempt + 1}/{retries}")
                    await asyncio.sleep(5)
                    continue
                else:
                    self.log_status("Captcha", "failed", error=e)
                    return None
        
    async def auth_login(self, email: str, password: str, captcha_token: str, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/auth/login"
        data = json.dumps({"email":email, "password":password, "captcha_token":captcha_token})
        headers = {
            **self.HEADERS[email],
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data, proxy=proxy, proxy_auth=proxy_auth) as response:
                        if response.status == 421: 
                            result = await response.json()
                            err_msg = result.get("message", "Unknown Error")
                            self.log_status("Login", "failed", error=err_msg)
                            return None
                        
                        response.raise_for_status()
                        result = await response.json()
                        return result
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    self.log_status("Login", "retry", f"Attempt {attempt + 1}/{retries}")
                    await asyncio.sleep(5)
                    continue
                else:
                    self.log_status("Login", "failed", error=e)
                    return None

    async def process_check_connection(self, email: str, use_proxy: bool, rotate_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(email) if use_proxy else None
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}Proxy  :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {proxy if proxy else 'No Proxy'} {Style.RESET_ALL}"
            )

            is_valid = await self.check_connection(proxy)
            if is_valid: return True
            
            if rotate_proxy:
                proxy = self.rotate_proxy_for_account(email)
                await asyncio.sleep(1)
                continue

            return False

    async def process_accounts(self, email: str, password: str, use_proxy: bool, rotate_proxy: bool):
        is_valid = await self.process_check_connection(email, use_proxy, rotate_proxy)
        if not is_valid:
            self.log_status("Process Account", "failed", error="Connection check failed")
            return

        proxy = self.get_next_proxy_for_account(email) if use_proxy else None

        captcha_token = await self.solve_recaptcha()
        if not captcha_token: return

        login = await self.auth_login(email, password, captcha_token, proxy)
        if not login: return

        status = login.get("status")
        message = login.get("message", "Unknown Message")

        if status == "Success":
            access_token = login.get("data", {}).get("access_token")
            self.log_status("Login", "success", message)

            account_data = [{"email": email, "access_token": access_token}]
            self.save_tokens(account_data)
            self.log_status("Process Account", "success", f"Account {self.mask_account(email)} processed successfully")
        else:
            self.log_status("Login", "failed", error=message)

    async def main(self):
        try:
            accounts = self.load_accounts()
            if not accounts:
                self.log(f"{Fore.RED + Style.BRIGHT}No Accounts Loaded.{Style.RESET_ALL}")
                return
            
            captcha_key = self.load_captcha_key()
            if captcha_key:
                self.CAPTCHA_KEY = captcha_key

            proxy_choice, rotate_proxy = self.print_question()

            self.clear_terminal()
            self.welcome()
            self.log(
                f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(accounts)}{Style.RESET_ALL}"
            )

            use_proxy = True if proxy_choice == 1 else False
            if use_proxy:
                await self.load_proxies()

            separator = "=" * 27
            for idx, account in enumerate(accounts, start=1):
                if account:
                    email = account["Email"]
                    password = account["Password"]

                    if "@" not in email or not password:
                        self.log_status("Account Validation", "failed", error="Invalid account format")
                        continue

                    self.log(
                        f"{Fore.CYAN + Style.BRIGHT}{separator}[{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {self.mask_account(email)} {Style.RESET_ALL}"
                        f"{Fore.CYAN + Style.BRIGHT}]{separator}{Style.RESET_ALL}"
                    )

                    self.HEADERS[email] = {
                        "Accept": "application/json, text/plain, */*",
                        "Accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
                        "Origin": "https://dashboard.3dos.io",
                        "Referer": "https://dashboard.3dos.io/",
                        "Sec-Fetch-Dest": "empty",
                        "Sec-Fetch-Mode": "cors",
                        "Sec-Fetch-Site": "same-site",
                        "User-Agent": FakeUserAgent().random
                    }

                    await self.process_accounts(email, password, use_proxy, rotate_proxy)
                    await asyncio.sleep(3)

        except FileNotFoundError:
            self.log(f"{Fore.RED}File 'captcha_key.txt' Not Found.{Style.RESET_ALL}")
            return
        except Exception as e:
            self.log_status("Main Process", "failed", error=e)
            raise e

if __name__ == "__main__":
    try:
        bot = Dos()
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.RED + Style.BRIGHT}[ EXIT ] 3Dos - BOT{Style.RESET_ALL}                                      ",                                       
        )