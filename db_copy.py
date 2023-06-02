from sqlalchemy import create_engine, Column, String, Integer, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd

# Android uygulaması için marka model ve serilerin olduğu bir database'in oluşturulduğu kod kısmı


new_db_engine = create_engine('sqlite:///car_brand.db')
NewDBSession = sessionmaker(bind=new_db_engine)
new_db_session = NewDBSession()

Base = declarative_base()


class NewCar(Base):
    __tablename__ = 'car_brand'
    id = Column(Integer, primary_key=True, nullable=False)
    marka = Column(Text, name='marka', nullable=False)
    seri = Column(Text, name='seri', nullable=False)
    model = Column(Text, name='model', nullable=True)


Base.metadata.create_all(new_db_engine)

df = pd.read_csv('yedek.csv')

for index, row in df.iterrows():
    marka = row['marka']
    seri = row['seri']
    model = row['model']

    new_car = NewCar(marka=marka, seri=seri, model=model)
    new_db_session.add(new_car)

new_db_session.commit()
new_db_session.close()
