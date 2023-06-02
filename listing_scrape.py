from bs4 import BeautifulSoup
import requests

from car_db import insert_listing_url, ListingUrl

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

test_url = "https://www.arabam.com/ikinci-el/otomobil/renault"
brands = ["alfa-romeo", "audi", "bmw", "chevrolet", "citroen", "dacia", "fiat", "ford", "honda", "hyundai", "kia",
          "lada", "mazda", "mercedes-benz", "nissan", "opel", "peugeot", "renault", "seat", "skoda", "tofas", "toyota",
          "volkswagen", "volvo"]

base_url = "https://www.arabam.com"
second_hand_cars_url = "/ikinci-el/otomobil"

all_models = []


def discover_brand_models(brand_url: str):
    response = requests.get(base_url + brand_url, headers=headers)
    doc = BeautifulSoup(response.text, "html.parser")
    tags = doc.find_all("a", class_="list-item")

    for tag in tags:
        href = tag['href']
        if href.startswith(brand_url+'-'):
            all_models.append(href)


def discover_all_models():
    for brand in brands:
        discover_brand_models(f"{second_hand_cars_url}/{brand}")


def add_listing_url_to_db(url: str):
    listing_url = ListingUrl()
    listing_url.url = url

    insert_listing_url(listing_url)


def gather_car_listings(url: str):
    brand_listing_result = requests.get(url, headers=headers)
    doc = BeautifulSoup(brand_listing_result.text, "html.parser")
    tags = doc.find_all(class_="listing-list-item pr should-hover bg-white")

    for tag in tags:
        a_tag = tag.find('a')
        if a_tag and 'href' in a_tag.attrs:
            add_listing_url_to_db(a_tag['href'])

    next_page_tag = doc.find("a", id="pagingNext")
    if next_page_tag is not None and 'href' in next_page_tag.attrs:
        gather_car_listings(base_url + next_page_tag['href'])
    else:
        print("end of list!")


def gather_all_brands_car_listing():
    discover_all_models()

    for model in all_models:
        brand_listing_url = f"{base_url}{model}?take=50"
        gather_car_listings(brand_listing_url)

gather_all_brands_car_listing()