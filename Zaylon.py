import os
import requests
import concurrent.futures
import time
from queue import Queue
from threading import Lock
from colorama import init, Fore
import ctypes

PURPLE = "\033[95m"
RESET = "\033[0m"

ctypes.windll.kernel32.SetConsoleTitleA("Zaylon")

# Text UwU

ascii_text = r""" {purple}
__________             .__                 
\____    /____  ___.__.|  |   ____   ____  
  /     /\__  \<   |  ||  |  /  _ \ /    \ 
 /     /_ / __ \\___  ||  |_(  <_> )   |  \
/_______ (____  / ____||____/\____/|___|  /
        \/    \/\/                      \/ 
                    Hisako On Top
{reset} """.format(purple=PURPLE, reset=RESET)


init(autoreset=True)

session = requests.Session()

def check_proxy(proxy, timeout, save_path, send_to_discord, webhook_url, webhook_queue):
    try:
        response = session.get('https://www.example.com', proxies={'http': proxy, 'https': proxy}, timeout=timeout)
        if response.status_code == 200:
            if 'Proxy-Connection' in response.headers:
                result = Fore.GREEN + 'Anonymous'
            else:
                result = Fore.GREEN + 'Good'
                save_proxy(proxy, save_path) 
                if send_to_discord:
                    webhook_queue.put(proxy) 
        else:
            result = Fore.RED + 'Bad'
        return proxy, result
    except requests.exceptions.RequestException:
        return proxy, Fore.RED + 'Bad'

def save_proxy(proxy, save_path):
    date_folder = os.path.join(save_path, get_current_date())
    os.makedirs(date_folder, exist_ok=True)
    filename = os.path.join(date_folder, 'good_proxies.txt')
    with open(filename, 'a') as file:
        file.write(proxy + '\n')

def get_current_date():
    import datetime
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%d')

def send_webhook(webhook_url, proxies):
    import json
    from discord_webhook import DiscordWebhook, DiscordEmbed

    webhook = DiscordWebhook(url=webhook_url)

    embed = DiscordEmbed(title='Proxy Good', color='00ff00')

    for proxy in proxies:
        embed.add_embed_field(name='Proxy', value=proxy)
        
    webhook.add_embed(embed)

    response = webhook.execute()
    # if response.status_code != 204:
    #     print(f'Errore nell\'invio del proxy tramite webhook. Status code: {response.status_code}')
    
def process_webhook_queue(webhook_queue, webhook_url):
    proxies = []
    while not webhook_queue.empty():
        proxy = webhook_queue.get()
        proxies.append(proxy)

        if len(proxies) == 25:
            send_webhook(webhook_url, proxies)
            proxies = []

    if proxies:
        send_webhook(webhook_url, proxies)

def main():
    print(ascii_text)
    file_path = input("Inserisci il percorso del file contenente i proxy da verificare: ")
    timeout = int(input("Inserisci il timeout (in secondi): "))
    max_workers = int(input("Inserisci il numero massimo di workers: "))
    webhook_enabled = input("Vuoi inviare i proxy buoni tramite il webhook su Discord? (Y/N): ").lower() == 'y'
    webhook_url = ''
    webhook_delay = 3  

    if webhook_enabled:
        webhook_url = input("Inserisci l'URL del webhook di Discord: ")

    proxy_list = []
    with open(file_path, 'r') as file:
        proxy_list = [proxy.strip() for proxy in file]

    save_path = os.path.join(os.getcwd(), 'Zaylon')
    os.makedirs(save_path, exist_ok=True)

    good_count = 0
    bad_count = 0

    webhook_queue = Queue() 
    webhook_lock = Lock()  

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(check_proxy, proxy, timeout, save_path, webhook_enabled, webhook_url, webhook_queue)
                   for proxy in proxy_list]
        for future in concurrent.futures.as_completed(futures):
            proxy, result = future.result()
            print(f'{proxy}: {result}')
            if result.endswith('Good'):
                good_count += 1
            elif result.endswith('Bad'):
                bad_count += 1

    print("\nScansione completata.")
    print(f"Proxy buoni trovati: {good_count}")
    print(f"Proxy cattivi trovati: {bad_count}")

    if webhook_enabled:
        print("\nInvio dei proxy buoni tramite webhook su Discord...")
        process_webhook_queue(webhook_queue, webhook_url)
        print("Invio completato.")

if __name__ == '__main__':
    main()
