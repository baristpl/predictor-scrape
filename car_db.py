from sqlalchemy import create_engine, Column, Integer, String, func
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///cars_listing.db')

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Car(Base):
    __tablename__ = 'car'
    id = Column(Integer, primary_key=True)
    ilan_no = Column(String, name='ilan_no')
    ilan_tarihi = Column(String, name='ilan_tarihi')
    marka = Column(String, name='marka')
    seri = Column(String, name='seri')
    model = Column(String, name='model')
    yil = Column(String, name='yil')
    kilometre = Column(String, name='kilometre')
    vites_tipi = Column(String, name='vites_tipi')
    yakit_tipi = Column(String, name='yakit_tipi')
    kasa_tipi = Column(String, name='kasa_tipi')
    motor_hacmi = Column(String, name='motor_hacmi')
    motor_gucu = Column(String, name='motor_gucu')
    cekis = Column(String, name='cekis')
    ortalama_yakit_tuketimi = Column(String, name='ortalama_yakit_tuketimi')
    yakit_deposu = Column(String, name='yakit_deposu')
    boya_degisen = Column(String, name='boya_degisen')
    takasa_uygun = Column(String, name='takasa_uygun')
    kimden = Column(String, name='kimden')
    price = Column(String, name='price')
    arac_turu = Column(String, name='arac_turu')
    renk = Column(String, name='renk')
    plaka_uyrugu = Column(String, name='plaka_uyrugu')
    garanti_durumu = Column(String, name='garanti_durumu')
    aracin_ilk_sahibi = Column(String, name='aracin_ilk_sahibi')
    yillik_mtv = Column(String, name='yillik_mtv')
    silindir_sayisi = Column(String, name='silindir_sayisi')
    tork = Column(String, name='tork')
    maksimum_guc = Column(String, name='maksimum_guc')
    minimum_guc = Column(String, name='minimum_guc')
    hizlanma = Column(String, name='hizlanma')
    maksimum_hiz = Column(String, name='maksimum_hiz')
    ortalama_yakit_tuketimi2 = Column(String, name='ortalama_yakit_tuketimi2')
    sehir_ici_yakit_tuketimi = Column(String, name='sehir_ici_yakit_tuketimi')
    sehir_disi_yakit_tuketimi = Column(String, name='sehir_disi_yakit_tuketimi')
    uzunluk = Column(String, name='uzunluk')
    genislik = Column(String, name='genislik')
    yukseklik = Column(String, name='yukseklik')
    agirlik = Column(String, name='agirlik')
    bos_agirlik = Column(String, name='bos_agirlik')
    koltuk_sayisi = Column(String, name='koltuk_sayisi')
    bagaj_hacmi = Column(String, name='bagaj_hacmi')
    on_lastik = Column(String, name='on_lastik')
    aks_araligi = Column(String, name='aks_araligi')
    is_wrecked = Column(String, name='is_wrecked')
    tramer_kaydi = Column(String, name='tramer_kaydi')
    tramer_tutari = Column(String, name='tramer_tutari')
    sanziman = Column(String, name='sanziman')


class ListingUrl(Base):
    __tablename__ = 'listing_urls'
    id = Column(Integer, primary_key=True)
    url = Column(String)


class Feature(Base):
    __tablename__ = 'feature'
    id = Column(Integer, primary_key=True)
    name = Column(String)


Base.metadata.create_all(engine)


def add_feature_if_not_exists(feature_name):
    existing_feature = session.query(Feature).filter_by(name=feature_name).first()
    if not existing_feature:
        feature = Feature()
        feature.name = feature_name
        insert_feature(feature)


def insert_car(car: Car):
    session.add(car)
    session.commit()


def insert_feature(feature: Feature):
    session.add(feature)
    session.commit()


def insert_listing_url(url: ListingUrl):
    session.add(url)
    session.commit()


def get_all_listing_urls_generator():
    for listing_url in session.query(ListingUrl).offset(36887).yield_per(1):
        yield listing_url


def get_number_of_rows():
    count = session.query(func.count(ListingUrl.id)).scalar()
    return count
