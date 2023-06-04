# Zaylon Proxy Checker

Zaylon Proxy Checker is a tool used to verify the status of proxies. It checks the provided proxy list for working and non-working proxies, and allows you to save the good proxies to a file. Additionally, it provides the option to send the good proxies to a Discord webhook.

## Features

- Verify the status of proxies in a given list
- Check both HTTP and HTTPS proxies
- Determine if a proxy is anonymous or not
- Save the good proxies to a file
- Send the good proxies to a Discord webhook

## Requirements

- Python 3.x

## Usage

1. Clone or download the repository to your computer.
2. Make sure you have Python 3.x installed on your system.
3. Open a terminal or command prompt and navigate to the directory of the program.
4. Run the program by typing the following command: py Zaylon.py 
5. Follow the instructions in the program:
   - Enter the path to the file containing the proxies to be checked.
   - Specify the timeout value in seconds.
   - Enter the maximum number of workers.
   - Choose whether to send the good proxies to a Discord webhook.
   - If sending to a webhook, provide the webhook URL.
6. The program will display the results of the proxy check, including the status (good or bad) for each proxy.
7. After the scan is complete, the program will provide the number of good and bad proxies found.
8. If sending to a Discord webhook, the program will send the good proxies in batches to the webhook.

## Contributing

If you would like to contribute to Zaylon Proxy Checker, you can open a new issue or submit a pull request on the GitHub repository.

---

Enjoy using Zaylon Proxy Checker! If you have any questions or encounter any issues, feel free to contact me.
