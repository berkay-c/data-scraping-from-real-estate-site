import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import streamlit as st
import time

class Scrape:
    out = ''
    city = ''
    district = ''
    neighborhood = ''
    houses_ads_url = []
    scraping_df = pd.DataFrame()

    def __init__(self) -> None:
        pass

    def get_name(self):
        c = input('Enter City Name : ').lower().strip()
        while(c == ''):
            c = input('Enter City Name : ').lower().strip()
        d = input('Enter District Name : ').lower().strip()
        n = input('Enter Neighborhood Name : ').lower().strip()

        translationTable = str.maketrans("ğıİöüşç", "giIousc")
        self.city = c.translate(translationTable)
        self.district = d.translate(translationTable)
        self.neighborhood = n.translate(translationTable)

    def requests_page(self):
        if self.district == '':
            self.URL = 'https://www.hepsiemlak.com/'+self.city+'-satilik'
        else:
            if self.neighborhood == '':
                self.URL = 'https://www.hepsiemlak.com/'+self.district+'-satilik'
            else:
                self.URL = 'https://www.hepsiemlak.com/' + self.district + '-' + self.neighborhood+'-satilik'

        self.page = requests.get(self.URL)
        time.sleep(3)
    def get_number_of_pages(self):
        soup = BeautifulSoup(self.page.content, "lxml")
        time.sleep(3)
        p = soup.find('ul', class_='he-pagination__links')
        temp = []
        for x in p:
            temp.append(x.text)
        self.number_of_pages = int(temp[-1])

    def get_each_house_advert_url(self):
        for i in range(1, self.number_of_pages+1, 1):
            each_page = requests.get(self.URL+'?page='+str(i))

            soup = BeautifulSoup(each_page.content, 'lxml')
            all_houses = soup.find_all('a', class_='img-link')

            for house in all_houses:
                self.houses_ads_url.append('https://www.hepsiemlak.com'+house['href'])

    def get_data_of_each_house(self):
        advert_id = []
        room_hall = []
        gross_m2 = []
        net_m2 = []
        floor_location = []
        building_age = []
        warming_type = []
        number_of_floors = []
        count_of_bathroom = []
        item_stat = []
        building_type = []
        building_facade = []
        building_fuel_type = []
        price = []

        for i in range(len(self.houses_ads_url)):
            each_house = requests.get(self.houses_ads_url[i])
            soup = BeautifulSoup(each_house.content, 'lxml')

            id = soup.find('span', string='İlan no')
            roomhall = soup.find('span', string='Oda + Salon Sayısı')
            gross = soup.find('span', string='Brüt / Net M2')
            net = soup.find('span', string='Brüt / Net M2')
            floor_loc = soup.find('span', string='Bulunduğu Kat')
            b_age = soup.find('span', string='Bina Yaşı')
            warming_t = soup.find('span', string='Isınma Tipi')
            numberfloors = soup.find('span', string='Kat Sayısı')
            countbathroom = soup.find('span', string='Banyo Sayısı')
            item_status = soup.find('span', string='Eşya Durumu')
            building_t = soup.find('span', string='Yapı Tipi')
            build_facade = soup.find('span', string='Cephe')
            build_fuel_type = soup.find('span', string='Yakıt Tipi')
            house_price = soup.find('p', class_='fontRB fz24 price')

            if not id:
                advert_id.append(np.NaN)
            else:
                advert_id.append(id.find_next_sibling('span').text)

            if not roomhall:
                room_hall.append(np.NaN)
            else:
                room_hall.append(roomhall.find_next_sibling('span').text)

            if not gross:
                gross_m2.append(np.NaN)
            else:
                gross_m2.append(gross.find_next_sibling('span').text.strip())

            if not net:
                net_m2.append(np.NaN)
            else:
                net_m2.append(net.find_next_sibling('span').find_next_sibling('span').text.replace('/', '').strip())

            if not floor_loc:
                floor_location.append(np.NaN)
            else:
                floor_location.append(floor_loc.find_next_sibling('span').text)

            if not b_age:
                building_age.append(np.NaN)
            else:
                building_age.append(b_age.find_next_sibling('span').text)

            if not warming_t:
                warming_type.append(np.NaN)
            else:
                warming_type.append(warming_t.find_next_sibling('span').text)

            if not numberfloors:
                number_of_floors.append(np.NaN)
            else:
                number_of_floors.append(numberfloors.find_next_sibling('span').text)

            if not countbathroom:
                count_of_bathroom.append(np.NaN)
            else:
                count_of_bathroom.append(countbathroom.find_next_sibling('span').text)

            if not item_status:
                item_stat.append(np.NaN)
            else:
                item_stat.append(item_status.find_next_sibling('span').text)

            if not building_t:
                building_type.append(np.NaN)
            else:
                building_type.append(building_t.find_next_sibling('span').text)

            if not build_facade:
                building_facade.append(np.NaN)
            else:
                building_facade.append(build_facade.find_next_sibling('span').text)

            if not build_fuel_type:
                building_fuel_type.append(np.NaN)
            else:
                building_fuel_type.append(build_fuel_type.find_next_sibling('span').text)

            if not house_price:
                price.append(np.NaN)
            else:
                price.append(house_price.text.replace('TL', '').replace('.', '').strip())

        self.scraping_df = pd.DataFrame({
            'Id': advert_id,
            'Room + Hall': room_hall,
            'Gross (m2)': gross_m2,
            'Net (m2)': net_m2,
            'Floor Location': floor_location,
            'Building Age': building_age,
            'Warming Type': warming_type,
            'Number of Floors': number_of_floors,
            'Count of Bathroom': count_of_bathroom,
            'Item Status': item_stat,
            'Building Type': building_type,
            'Building Facade': building_facade,
            'Building Fuel Type': building_fuel_type,
            'Price': price
        })

    def dataframe_to_csv(self):
        if self.district == '':
            self.out = 'DataSets/'+self.city+'.csv'
        elif self.neighborhood == '':
            self.out = 'DataSets/'+self.city+'-'+self.district+'.csv'
        else:
            self.out = 'DataSets/'+self.city+'-'+self.district+'-'+self.neighborhood+'.csv'

        self.scraping_df.to_csv(self.out, index=False)

    # Streamlit Section

    def run(self):
        flag = 0
        
        with st.form("my_form"):
            c = st.text_input('Enter City Name :')
            d = st.text_input('Enter District Name :')
            n = st.text_input('Enter Neighborhood Name :')

            submitted = st.form_submit_button("Submit")
            if submitted:
                with st.spinner('Wait for it...'):
                    c = c.lower().strip()
                    d = d.lower().strip()
                    n = n.lower().strip()
                    translationTable = str.maketrans("ğıİöüşç", "giIousc")
                    self.city = c.translate(translationTable)
                    self.district = d.translate(translationTable)
                    self.neighborhood = n.translate(translationTable)

                    self.requests_page()
                    self.get_number_of_pages()
                    self.get_each_house_advert_url()
                    self.get_data_of_each_house()
                    flag = 1

        if flag == 1:
            # download section
            file_name = self.csv_out_name()
            csv = self.convert_df(self.scraping_df)

            st.dataframe(self.scraping_df)  # show dataframe

            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name=file_name,
                mime='text/csv',
            )

        """
        c = st.text_input('Enter City Name :')
        d = st.text_input('Enter District Name :')
        n = st.text_input('Enter Neighborhood Name :')
        if st.button('START'):    
            with st.spinner('Wait for it...'):
                c = c.lower().strip()
                d = d.lower().strip()
                n = n.lower().strip()
                translationTable = str.maketrans("ğıİöüşç", "giIousc")
                self.city = c.translate(translationTable)
                self.district = d.translate(translationTable)
                self.neighborhood = n.translate(translationTable)
                
                self.requests_page()
                self.get_number_of_pages()
                self.get_each_house_advert_url()
                self.get_data_of_each_house()
                
                # download section
                file_name=self.csv_out_name()
                csv = self.convert_df(self.scraping_df)
                
                st.dataframe(self.scraping_df) # show dataframe
                
                st.download_button(     
                label="Download data as CSV",
                data=csv,
                file_name=file_name,
                mime='text/csv',
                
                )"""

    def csv_out_name(self):
        if self.district == '':
            self.out = self.city+'.csv'
        elif self.neighborhood == '':
            self.out = self.city+'-'+self.district+'.csv'
        else:
            self.out = self.city+'-'+self.district+'-'+self.neighborhood+'.csv'
        return self.out

    def convert_df(self, df):
        return df.to_csv()
