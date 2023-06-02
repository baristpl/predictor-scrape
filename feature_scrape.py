from typing import List

from car_db import get_all_listing_urls_generator, get_number_of_rows, add_feature_if_not_exists, Car, insert_car
from bs4 import BeautifulSoup
import requests

count = 0
ATTRIBUTE_MAPPING = {
    'İlan No': 'ilan_no',
    'İlan Tarihi': 'ilan_tarihi',
    'Marka': 'marka',
    'Seri': 'seri',
    'Model': 'model',
    'Yıl': 'yil',
    'Kilometre': 'kilometre',
    'Vites Tipi': 'vites_tipi',
    'Yakıt Tipi': 'yakit_tipi',
    'Kasa Tipi': 'kasa_tipi',
    'Motor Hacmi': 'motor_hacmi',
    'Motor Gücü': 'motor_gucu',
    'Çekiş': 'cekis',
    'Ort. Yakıt Tüketimi': 'ortalama_yakit_tuketimi',
    'Yakıt Deposu': 'yakit_deposu',
    'Boya-değişen': 'boya_degisen',
    'Takasa Uygun': 'takasa_uygun',
    'Kimden': 'kimden',
    'price': 'price',
    'Araç Türü': 'arac_turu',
    'Renk': 'renk',
    'Plaka Uyruğu': 'plaka_uyrugu',
    'Garanti Durumu': 'garanti_durumu',
    'Aracın ilk sahibiyim': 'aracin_ilk_sahibi',
    'Yıllık MTV': 'yillik_mtv',
    'Silindir Sayısı': 'silindir_sayisi',
    'Tork': 'tork',
    'Maksimum Güç': 'maksimum_guc',
    'Minimum Güç': 'minimum_guc',
    'Hızlanma (0-100)': 'hizlanma',
    'Maksimum Hız': 'maksimum_hiz',
    'Ortalama Yakıt Tüketimi': 'ortalama_yakit_tuketimi2',
    'Şehir İçi Yakıt Tüketimi': 'sehir_ici_yakit_tuketimi',
    'Şehir Dışı Yakıt Tüketimi': 'sehir_disi_yakit_tuketimi',
    'Uzunluk': 'uzunluk',
    'Genişlik': 'genislik',
    'Yükseklik': 'yukseklik',
    'Ağırlık': 'agirlik',
    'Boş Ağırlığı': 'bos_agirlik',
    'Koltuk Sayısı': 'koltuk_sayisi',
    'Bagaj Hacmi': 'bagaj_hacmi',
    'Ön Lastik': 'on_lastik',
    'Aks Aralığı': 'aks_araligi',
    'is_wrecked': 'is_wrecked',
    'tramer_kaydi': 'tramer_kaydi',
    'tramer_tutari': 'tramer_tutari',
    'Şanzıman': 'sanziman',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

base_url = "https://www.arabam.com"


def build_get_details_url(listing_id: str) -> str:
    return f"https://www.arabam.com/advertDetail/details?id={listing_id}"


def scrape_short_description(features_dict: dict, doc: BeautifulSoup) -> dict[str, str]:
    container = doc.find("ul", class_="w100 cf mt12 detail-menu")
    if container is None:
        return None
    tags = container.find_all("li", class_="bcd-list-item")

    for tag in tags:
        spans = tag.find_all('span')
        if len(spans) == 2:
            key = spans[0].text.strip().removesuffix(':')
            value = spans[1].text.strip()
            features_dict[key] = value

    return features_dict


def scrape_price(features_dict: dict, doc: BeautifulSoup) -> dict[str, str]:
    tag = doc.find("p", class_="font-default-plusmore bold ls-03")
    if tag is not None:
        features_dict["price"] = tag.text.strip().removesuffix(" TL")
        return features_dict
    else:
        print("cannot find")


def scrape_details(features_dict: dict) -> dict[str, str]:
    listing_id = features_dict["İlan No"]
    fetch_url = build_get_details_url(listing_id)

    details_response = requests.get(fetch_url, headers=headers)
    details_doc = BeautifulSoup(details_response.text, "html.parser")
    tags = details_doc.find_all("dl", class_="cf vertically-centered-big m0 technical-info pl20")

    for tag in tags:
        spans = tag.find_all('span')
        if len(spans) == 2:
            key = spans[0].text.strip()
            value = spans[1].text.strip()
            features_dict[key] = value
    return features_dict


def scrape_tramer_info(features_dict: dict, doc: BeautifulSoup) -> dict[str, str]:
    wrecked_tag = doc.find("div", class_="cf pl4 pr4 font-default-minus")
    features_dict["is_wrecked"] = False
    if wrecked_tag is not None:
        p_tag = wrecked_tag.find("p")
        if p_tag is not None and p_tag.text.strip() == "Bu araç ağır hasar kayıtlıdır.":
            features_dict["is_wrecked"] = True

    if features_dict["is_wrecked"]:
        return features_dict

    tramer_tag = doc.find("div", class_="cf pl4 pr4 font-default-minus pt20 border-top-grey2")
    if tramer_tag is not None:
        p_tag = tramer_tag.find("p")
        span_tag = tramer_tag.find("span", class_="pl4 bold")
        if p_tag is not None and p_tag.text.strip() == "Tramer tutarı yok":
            features_dict["tramer_kaydi"] = False
            features_dict["tramer_tutari"] = 0
        elif span_tag is not None:
            features_dict["tramer_tutari"] = span_tag.text.strip().removesuffix(" TL")
            features_dict["tramer_kaydi"] = True
        else:
            features_dict["tramer_kaydi"] = None
            features_dict["tramer_tutari"] = None
    else:
        features_dict["tramer_kaydi"] = None
        features_dict["tramer_tutari"] = None

    return features_dict


def run_scrape(listing_url: str) -> dict[str, str | bool]:
    print(listing_url)
    features_dict = {}
    response = requests.get(base_url + listing_url, headers=headers)
    doc = BeautifulSoup(response.text, "html.parser")

    dict = scrape_short_description(features_dict, doc)
    if dict is None:
        return None

    scrape_price(features_dict, doc)
    scrape_details(features_dict)
    scrape_tramer_info(features_dict, doc)
    return features_dict


def parse_car_data(car_data: dict[str, str]) -> Car:
    car = Car()

    for key, value in car_data.items():
        if key in ATTRIBUTE_MAPPING:
            attribute_name = ATTRIBUTE_MAPPING[key]
            setattr(car, attribute_name, value)

    return car


for listing_url in get_all_listing_urls_generator():

    feature_dict = run_scrape(listing_url.url)
    if feature_dict is None:
        continue
    car = parse_car_data(feature_dict)
    insert_car(car)
