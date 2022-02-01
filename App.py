from Scrape import *
import streamlit as st
from streamlit_option_menu import option_menu


if __name__ == '__main__':
    
    """ s1=Scrape()
    s1.get_name()
    s1.requests_page()
    s1.get_number_of_pages()
    """
    
    st.set_page_config(page_title="Data Scraping From Real Estate Site",initial_sidebar_state='auto',page_icon='chart_with_upwards_trend')
    
    
    page = option_menu(None, ["Home", "Get Data","About Me"],icons=['house', 'app','person'],menu_icon="cast", default_index=0, orientation="horizontal")
    
    if page == "Home":
        st.markdown("## WELCOME  :wave:")
        st.markdown("Hello, I'm **Berkay**. I want to talk about my project.")
        st.markdown("* The data is scraped ' **https://hepsiemlak.com/** ' ")
        st.markdown("* It takes city, district and neighborhood names as input from the user, respectively.")
        st.markdown("* When the data scraping process is completed, it gives a preview of the obtained data.")
        st.markdown("* It can be downloaded in csv format.")
        st.markdown("* Click get data to review the project")
    
    elif page == 'Get Data':
        s1=Scrape()
        s1.run()      
          
    elif page == 'About Me':
        st.markdown("## Hello, I'm Berkay :bar_chart:")
        st.markdown("#### I'm 21 years old. I am a 3rd year Computer Engineering student.  I work to improve myself in the fields of data scraping, data analysis, data visualization, machine learning, object detection.")
        st.markdown("## 🔗 Contact Me and Feedback")
        st.markdown("[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/berkay-c)")
        st.markdown("[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/berkay-c/)")
        st.markdown("[![Gmail](https://img.shields.io/badge/gmail-%23D14836.svg?&style=for-the-badge&logo=gmail&logoColor=white)](mailto:berkayyasinciftci@gmail.com?subject=Hola%20Jiji)")
        