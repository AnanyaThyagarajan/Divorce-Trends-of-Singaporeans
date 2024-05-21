import streamlit as st
import pandas as pd
import plotly.express as px

def load_css(file_name):
    with open(file_name, "r") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Function to load data from URL
@st.cache
def load_data(url):
    data = pd.read_csv(url)
    data.drop(columns='Unnamed: 0', inplace=True)
    return data
def convert_columns_to_numeric(data, y_axis):
    for col in y_axis:
        data[col] = pd.to_numeric(data[col], errors='coerce')  # Convert to numeric and handle errors
    return data
# URLs of datasets
urls = {
    'Population Structure': "https://raw.githubusercontent.com/AnanyaThyagarajan/Divorce-Trends-of-Singaporeans/main/dataset/cleaned_population_structure.csv",
    'Marriage Key Indicators': "https://raw.githubusercontent.com/AnanyaThyagarajan/Divorce-Trends-of-Singaporeans/main/dataset/cleaned_marriage_key_indicators.csv",
    'Marriage Rate by Age Group': "https://raw.githubusercontent.com/AnanyaThyagarajan/Divorce-Trends-of-Singaporeans/main/dataset/cleaned_marriage_rate.csv",
    'Median Age of Bride and Grooms': "https://raw.githubusercontent.com/AnanyaThyagarajan/Divorce-Trends-of-Singaporeans/main/dataset/cleaned_median_age_of_bride_and_grooms.csv",
    'Divorce Rate by Age Group': "https://raw.githubusercontent.com/AnanyaThyagarajan/Divorce-Trends-of-Singaporeans/main/dataset/cleaned_divorce_rate.csv",
    'Age Group and Sex of Divorcees': "https://raw.githubusercontent.com/AnanyaThyagarajan/Divorce-Trends-of-Singaporeans/main/dataset/cleaned_age_grp_and_sex_of_divorcees.csv",
    'Divorce Key Indicators': "https://raw.githubusercontent.com/AnanyaThyagarajan/Divorce-Trends-of-Singaporeans/main/dataset/cleaned_divorce_key_indicators.csv"
}

def main():
    load_css('style.css')
    st.title('Singapore Marriage and Divorce Trends Dashboard')
    
    dataset_name = st.sidebar.selectbox('Select a Dataset', list(urls.keys()))
    data = load_data(urls[dataset_name])

    if st.sidebar.checkbox('Show raw data'):
        st.write(data)
    # Footer
    footer = """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #111111;
        color: white;
        text-align: center;
        padding: 10px;
    }
    </style>
    <div class="footer">
        <p>Made by Ananya Krithika Thyagarajan | <a href="https://www.linkedin.com/in/ananya-krithikathyagarajan" target="_blank">LinkedIn</a> | <a href="https://github.com/AnanyaThyagarajan/Divorce-Trends-of-Singaporeans" target="_blank">GitHub</a></p>
    </div>
    """
    st.markdown(footer, unsafe_allow_html=True)
    
    plot_type = st.sidebar.radio("Select Plot Type", ('Line Plot', 'Bar Plot'))

    if st.sidebar.checkbox('Show Plot'):
        x_axis = st.sidebar.selectbox('Choose the X-axis', options=data.columns)
        y_options = [col for col in data.columns if col != x_axis]
        y_axis = st.sidebar.multiselect('Choose the Y-axis', options=y_options, default=y_options[0])
        
        if y_axis:
            data = convert_columns_to_numeric(data, y_axis)
            if plot_type == 'Line Plot':
                fig = px.line(data, x=x_axis, y=y_axis, title=f'Trends in {dataset_name}')
            elif plot_type == 'Bar Plot':
                fig = px.bar(data, x=x_axis, y=y_axis, title=f'Trends in {dataset_name}')

            st.plotly_chart(fig)



if __name__ == "__main__":
    main()
