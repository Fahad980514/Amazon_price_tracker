from bs4 import BeautifulSoup
import requests
import smtplib
import os
from dotenv import find_dotenv, load_dotenv
import lxml

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

url = "https://www.amazon.com/Instant-Pot-Plus-Programmable-Sterilizer/dp/B075CYMYK6/?_encoding=UTF8&pd_rd_w=1oT1D&content-id=amzn1.sym.730a4fb4-1f7f-4520-9e50-8136d347aedd%3Aamzn1.symc.abfa8731-fff2-4177-9d31-bf48857c2263&pf_rd_p=730a4fb4-1f7f-4520-9e50-8136d347aedd&pf_rd_r=MFW51XJ5EF77CZ40QQ1N&pd_rd_wg=TlNvJ&pd_rd_r=02feb374-fd38-4af4-925a-e612bde131d1&ref_=pd_hp_d_btf_ci_mcx_mr_ca_id_hp_d&th=1"
email = os.getenv("email")
password = os.getenv("password")
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Priority": "u=0, i",
    "Sec-Ch-Ua-Platform": "Windows",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
}

#minimal_headers = {
# "Accept-Language": "en-US,en;q=0.9",
# "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
# }

response = requests.get(url, headers=headers)
data = response.text

#Finding Html element that contain price with the currency sign
soup = BeautifulSoup(data, "lxml")

#Getting the price only and name only text
price_tag = soup.find(class_ = "a-offscreen").get_text()
item_name = soup.find(name = "span" , class_ = "a-size-large product-title-word-break").get_text().split()
item_name = " ".join(item_name)

#Replacing the currency sign
price_without_sign = price_tag.replace("$", "")

#showing as a float number
price_as_float = float(price_without_sign)


if price_as_float < 100:
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=email, password=password)
        connection.sendmail(from_addr=email,
                            to_addrs=email,
                            msg=f"Subject:Amazon Price Alert\n\n{item_name} only for ${price_as_float}\n, {url}".encode("utf-8")
                            )
