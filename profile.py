import streamlit as st
import pandas as pd
import plotly.express as px
import folium

st.markdown("""
    <style>
        .main {
            background-color: #0047ab;
        }
        .sidebar .sidebar-content {
            background-color: #0047ab;
        }
        h1, h2, h3, h4, h5, h6, p {
            color: white;
        }
        .dataframe {
            background-color: #0047ab;
            border: 1px solid gray;
        }
        button {
            background-color: white;
            color: #0047ab;
            border-radius: 10px;
        }
        .stChart {
            background-color: #0047ab;
            border-radius: 5px;
        }
    </style>
    """, unsafe_allow_html=True)

coverletter,dataset = st.tabs(["Cover Letter", "Dataset"])

with coverletter:
    with st.sidebar:
        st.header("Quentin Cardona")
        col1, col2 = st.columns([1, 4])
        with col1:
            st.image("linkedinlogo.png", width=50)
        with col2:
            st.markdown("[Linkedin](https://www.linkedin.com/in/quentin-cardona-88b880221)")
        col1, col2 = st.columns([1, 4])
        with col1:
            st.image("githublogo.png", width=50)
        with col2:
            st.markdown("[Github](https://github.com/cquent)")
        st.write("Email : quentin.cardona@efrei.net")

    profile, education, skills, projects, experience = st.tabs(["Profile", "Education", "Skills", "Projects", "Experience"])
    with profile:
        st.header("Profile")
        st.write("I am a student at Efrei Paris, a french engineering school. I am currently in my 4th year of study and I am looking for a 5-month internship in the field of data science.")
        st.write("I am passionate about data science and I am always looking to learn more about this field.")
        st.write("Computer science student focusing on Machine Learning, Deep Learning, and Generative Artificial Intelligence, with strong teamwork skills through multiple projects, particularly using the AGILE methodology. Experienced in working in an international environment, I am rigorous, organized, and adaptable to various demands.")

    with education:
        st.header("Education")
        st.subheader("Efrei Paris")
        st.write("2020 - 2023")
        st.subheader("Preparatory class")
        st.write("2018 - 2020")
        st.subheader("Baccalaureate")
        st.write("2018")

    with skills:
        st.header("Skills")
        st.write("- Python")
        st.write("- SQL")
        st.write("- Machine Learning")
        st.write("- Deep Learning")
        st.write("- Data Visualization")

    with projects:
        st.header("Projects")
        st.subheader("June 2024")
        st.write("Analyzed a patent database in Python to predict categories based on their descriptions.")
        st.subheader("First Semester 2023")
        st.write("Developed a hiking app in React Native, Nest JS, and GraphQL to convert map photos into interactive GPX traces.")

    with experience:
        st.header("Experience")
        st.subheader("Darty")
        st.write("One-month commercial internship, 01/2023")
        st.write("Customer consulting")
        st.subheader("Palais des Thés")
        st.write("One-month worker internship, 07/2022")
        st.write("Stock management")
        st.subheader("Orange")
        st.write("IT internship, 02/2018")

with dataset:
    data = pd.read_csv('dataetudiants.csv', sep=';')

    st.title("Private and Public Universities Enrollment Comparison")

    selected_year = st.selectbox("Select an Academic Year:", data['annee_universitaire'].unique())
    selected_year2 = st.selectbox("Select another Academic Year:", data['annee_universitaire'].unique())

    filtered_data_1 = data[data['annee_universitaire'] == selected_year]
    filtered_data_2 = data[data['annee_universitaire'] == selected_year2]

    total_count_1 = filtered_data_1['secteur'].count()
    total_count_2 = filtered_data_2['secteur'].count()

    combined_data = pd.DataFrame({
        'Sector': ['PU', 'PR'],
        f'{selected_year}': [
            (filtered_data_1['secteur'].value_counts().get('PU', 0) / total_count_1) * 100,
            (filtered_data_1['secteur'].value_counts().get('PR', 0) / total_count_1) * 100
        ],
        f'{selected_year2}': [
            (filtered_data_2['secteur'].value_counts().get('PU', 0) / total_count_2) * 100,
            (filtered_data_2['secteur'].value_counts().get('PR', 0) / total_count_2) * 100 
        ]
    })

    combined_data_melted = combined_data.melt(id_vars='Sector', var_name='Year', value_name='Percentage')

    sector_ratio_fig = px.bar(
        combined_data_melted,
        x='Sector',
        y='Percentage',
        color='Year',
        barmode='group',
        labels={'Percentage': 'Percentage (%)', 'Sector': 'Sector'},
        title=f'Private/Public Ratio Comparison for {selected_year} and {selected_year2}'
    )
    st.plotly_chart(sector_ratio_fig)

    st.write("The distribution of students in public and private universities is relatively stable over the years.")

###########################################################

    st.title("Enrollment in Engineering Schools")

    total_counts = data.groupby('annee_universitaire')['effectif'].sum()
    engineering_counts = data.groupby('annee_universitaire')['effectif_ing'].sum()

    engineering_percentages = (engineering_counts / total_counts) * 100

    combined_ratios = pd.DataFrame({
        'Year': engineering_percentages.index,
        'Percentage': engineering_percentages.values
    })

    category_ratio_fig = px.bar(
        combined_ratios,
        x='Year',
        y='Percentage',
        labels={'Percentage': 'Percentage of Total Students', 'Year': 'Academic Year'},
        title='Percentage of Students in Engineering Schools by Year',
        range_y=[0, 6],
    )
    
    st.plotly_chart(category_ratio_fig) 

###########################################################

    st.title("Geographic Analysis of Engineering Schools")

    regions_with_data = data.groupby('geo_nom').filter(lambda x: x['effectif_ing'].sum() > 0)['geo_nom'].unique()
    selected_region = st.selectbox("Select a Region:", regions_with_data)

    regional_data = data[data['geo_nom'] == selected_region]
    yearly_enrollment = regional_data.groupby('annee_universitaire')['effectif_ing'].sum().reset_index()

    yearly_enrollment_fig = px.bar(
        yearly_enrollment,
        x='annee_universitaire',
        y='effectif_ing',
        labels={'effectif_ing': 'Total Engineering Students', 'annee_universitaire': 'Academic Year'},
        title=f'Total Engineering Students in {selected_region} Over the Years',
    )

    st.plotly_chart(yearly_enrollment_fig)

###########################################################

    st.title("Gender Ratio in Engineering Schools by Year")

    gender_counts = data.groupby(['annee_universitaire', 'sexe'])['effectif_ing'].sum().reset_index()
    gender_counts['Percentage'] = gender_counts.groupby('annee_universitaire')['effectif_ing'].transform(lambda x: (x / x.sum()) * 100)

    gender_ratios = gender_counts.pivot(index='annee_universitaire', columns='sexe', values='Percentage').reset_index()
    gender_ratios.columns = ['Year', 'Male', 'Female']

    gender_ratios = gender_ratios.fillna(0)

    gender_ratio_fig = px.bar(
        gender_ratios,
        x='Year',
        y=['Male', 'Female'],
        labels={'value': 'Percentage (%)', 'Year': 'Academic Year'},
        title='Gender Ratio in Engineering Schools by Year',
        barmode='group',
        range_y=[0, 100],
    )

    st.plotly_chart(gender_ratio_fig)

###########################################################

    department_coordinates = {
        'Ain': [46.2065, 5.1001],
        'Aisne': [49.5807, 3.2615],
        'Allier': [46.2913, 3.3732],
        'Alpes-de-Haute-Provence': [44.0816, 6.2007],
        'Alpes-Maritimes': [43.6629, 7.4272],
        'Ardèche': [44.6092, 4.5853],
        'Ardennes': [49.5072, 4.9425],
        'Ariège': [43.0663, 1.5862],
        'Aube': [48.2235, 4.0255],
        'Aude': [43.2220, 2.1005],
        'Aveyron': [44.0955, 2.5655],
        'Bouches-du-Rhône': [43.2945, 5.3797],
        'Calvados': [49.4144, -0.3547],
        'Cantal': [44.9298, 2.5860],
        'Charente': [45.6284, -0.1571],
        'Charente-Maritime': [45.6830, -1.1485],
        'Cher': [47.0595, 2.5692],
        'Corrèze': [45.1628, 1.8331],
        'Côte-d\'Or': [47.1009, 4.9887],
        'Côtes-d\'Armor': [48.5881, -2.7214],
        'Creuse': [45.9145, 1.8565],
        'Dordogne': [45.0669, 0.7420],
        'Doubs': [47.0101, 6.1141],
        'Drôme': [44.6293, 5.0417],
        'Essonne': [48.5880, 2.2106],
        'Eure': [49.0830, 1.0737],
        'Eure-et-Loir': [48.4677, 1.2748],
        'Finistère': [48.3874, -4.5905],
        'Gard': [43.9674, 4.3133],
        'Haute-Garonne': [43.6047, 1.4442],
        'Haute-Loire': [45.4302, 3.9202],
        'Haute-Marne': [48.1855, 5.1782],
        'Haute-Savoie': [46.1257, 6.6696],
        'Hautes-Alpes': [44.5422, 6.1084],
        'Hautes-Pyrénées': [43.0955, 0.0420],
        'Haut-Rhin': [47.7430, 7.3006],
        'Hauts-de-Seine': [48.8534, 2.2242],
        'Isère': [45.5772, 5.5474],
        'Jura': [46.6977, 5.7007],
        'Landes': [43.7162, -0.6917],
        'Loir-et-Cher': [47.6711, 1.1976],
        'Loire': [45.5472, 4.0758],
        'Loire-Atlantique': [47.2268, -1.5365],
        'Loiret': [47.8824, 1.9353],
        'Lot': [44.5841, 1.6475],
        'Lot-et-Garonne': [44.3985, 0.7767],
        'Manche': [48.6713, -1.4252],
        'Marne': [48.8491, 4.4969],
        'Haute-Marne': [48.1882, 5.1380],
        'Mayenne': [48.2336, -0.6538],
        'Meurthe-et-Moselle': [48.6498, 6.1900],
        'Meuse': [49.0877, 5.5601],
        'Morbihan': [47.7316, -2.9882],
        'Moselle': [49.0995, 6.0913],
        'Nièvre': [46.9812, 3.4741],
        'Nord': [50.4046, 3.1122],
        'Oise': [49.4203, 2.2048],
        'Orne': [48.6923, -0.6222],
        'Pas-de-Calais': [50.3920, 2.8151],
        'Puy-de-Dôme': [45.7742, 3.0745],
        'Pyrénées-Atlantiques': [43.3566, -0.4180],
        'Pyrénées-Orientales': [42.5378, 2.8938],
        'Rhône': [45.7485, 4.8467],
        'Saône-et-Loire': [46.6611, 4.8275],
        'Sarthe': [47.9224, 0.2801],
        'Savoie': [45.6542, 6.2123],
        'Haute-Savoie': [46.1257, 6.6696],
        'Somme': [49.8890, 2.2922],
        'Tarn': [43.6352, 2.2729],
        'Tarn-et-Garonne': [44.0233, 1.3875],
        'Var': [43.5251, 6.1035],
        'Vaucluse': [44.0244, 5.0774],
        'Vendée': [46.6670, -1.4735],
        'Vienne': [46.5803, 0.3452],
        'Vosges': [48.1412, 6.2298],
        'Yonne': [47.0586, 3.3801],
        'Yvelines': [48.8384, 1.9162],
    }

    selected_year_3 = st.selectbox("Select an Academic Year:", data['annee_universitaire'].unique(), key='3')

    engineering_data = data[(data['effectif_ing'] > 0) & (data['annee_universitaire'] == selected_year_3)]

    gender_data = engineering_data.groupby(['geo_nom', 'sexe'])['effectif_ing'].sum().reset_index()
    total_gender_data = gender_data.groupby('geo_nom')['effectif_ing'].sum().reset_index()
    total_gender_data.rename(columns={'effectif_ing': 'total_students'}, inplace=True)

    gender_data = gender_data.merge(total_gender_data, on='geo_nom')
    gender_data['percentage_girls'] = (gender_data[gender_data['sexe'] == 2]['effectif_ing'] / gender_data['total_students']) * 100

    girls_percentage = gender_data[gender_data['sexe'] == 2][['geo_nom', 'percentage_girls']]

    m = folium.Map(location=[46.6034, 1.8883], zoom_start=6)

    for idx, row in girls_percentage.iterrows():
        if row['geo_nom'] in department_coordinates:
            lat, lon = department_coordinates[row['geo_nom']]
            color = 'purple' if row['percentage_girls'] < 20 else 'blue' if row['percentage_girls'] < 30 else 'green' if row['percentage_girls'] < 40 else 'yellow' if row['percentage_girls'] < 60 else 'orange' if row['percentage_girls'] < 80 else 'red'
            folium.CircleMarker(
                location=[lat, lon],
                radius=10,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.6,
                popup=f"{row['geo_nom']}: {row['percentage_girls']:.2f}%"
            ).add_to(m)

    map_file = 'map.html'
    m.save(map_file)

    with open(map_file, 'r', encoding='utf-8') as f:
        map_html = f.read()

    st.components.v1.html(map_html, height=500, scrolling=True)

    st.write("We notice an increase in the percentage of girls in engineering schools over the years.")
    st.write("These percentages are very different depending on the region.")