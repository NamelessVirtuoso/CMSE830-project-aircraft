import streamlit as st
import seaborn as sns
import altair as alt
import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

data = pd.read_csv('https://www.kaggle.com/datasets/faa/wildlife-strikes/download?datasetVersionNumber=1')


red = "#E74C3C"
blue = "#3498DB"
green = "#58D68D"


def hex_to_RGB(hex_str):
    return [int(hex_str[i:i+2], 16) for i in range(1,6,2)]

def get_color_gradient(c1, c2, n):
    assert n > 1
    c1_rgb = np.array(hex_to_RGB(c1))/255
    c2_rgb = np.array(hex_to_RGB(c2))/255
    mix_pcts = [x/(n-1) for x in range(n)]
    rgb_colors = [((1-mix)*c1_rgb + (mix*c2_rgb)) for mix in mix_pcts]
    return ["#" + "".join([format(int(round(val*255)), "02x") for val in item]) for item in rgb_colors]

st.markdown("<h1 style='text-align: center; color: red;'>Dangers up there</h1>", unsafe_allow_html=True)

st.write(" What reasons caused the most aircraft accidents?")

show = st.checkbox('Click here to take a look at the dataset')

if show:
    st.dataframe(data.head())


yes = st.checkbox('Click here to show the missing values')

if yes:
    st.write(data.isna().sum())


st.write(
    "Since we do not use some of the informations, and replacing them with calculated values takes a lot of work, we will simply drop them.")



df = data[data.Operator != "UNKNOWN"]

occur = df.groupby(["Operator ID"]).size()
sorted = occur.sort_values(ascending=False)[0:10]

occur2 = df.groupby(["Operator"]).size()
sorted2 = occur2.sort_values(ascending=False)[0:10].index

fig, ax = plt.subplots()
ax.bar(sorted.index, sorted, color = get_color_gradient(red, blue, len(sorted)))
plt.xlabel("Companies")
plt.ylabel("Number of incidents")
plt.title("Number of incidents by Companies")


if st.checkbox('Which Aircraft company experienced the most accidents?'):
    st.pyplot(fig)
    st.write("These company are:",sorted2)

    st.write("But the number of incidents doesn't necessarily mean the incident rate.")


st.header("Year and month")
st.subheader("Year")
st.write("Let's focus on the year. Which year did most of the incidents happen?")


year = df.groupby(["Incident Year"]).size()
year_sorted = year.sort_values(ascending=False)

fig2, ax2 = plt.subplots()
ax2.bar(year.index, year, color = get_color_gradient(blue, red, len(year)))
plt.xlabel("Year")
plt.ylabel("Number of incidents")
plt.title("Number of incidents versus year")

if st.checkbox('Click to show the years'):
    st.pyplot(fig2)
    year_sorted[0:1]

    st.write("Overall more and more incidents happen. But that doesn't mean the accident rate has increaset.")
    image = Image.open('image.png')
    st.image(image, caption='Accident rate has actually went down')

    st.write("2014, the darkest year of modern Airline industries. Malaysia Airlines MH370 and MH17 went missing on 2014, too.")
    st.write("For more details, check out this [link](https://en.wikipedia.org/wiki/Malaysia_Airlines_Flight_370?oldformat=true)")



st.subheader("Month")
st.write("Let's focus on the month. Which month did most of the incidents happen?")

month = df.groupby(["Incident Month"]).size()
month_sorted = month.sort_values(ascending=False)

fig3, ax3 = plt.subplots()
ax3.bar(month.index, month, color = get_color_gradient(green, green, len(month)))
plt.xlabel("Months")
plt.ylabel("Number of incidents")
plt.title("Number of incidents versus month")

if st.checkbox('Click to show the monthes'):
    st.pyplot(fig3)
    month_sorted[0:1]
    st.write("Augest, September and October has the most accidents.")

st.header("Animals")

st.subheader("Which specie caused the most accidents?")

ani = df.groupby(["Species ID"]).size()
ani_sorted = ani.sort_values(ascending=False)[0:10]

ani2 = df.groupby(["Species Name"]).size()
ani_sorted2 = ani2.sort_values(ascending=False)[0:10].index

fig_a, ax_a = plt.subplots()
ax_a.bar(ani_sorted2, ani_sorted, color = get_color_gradient(red, blue, len(ani_sorted)))
plt.xticks(rotation=90)
plt.xlabel("Species")
plt.ylabel("Number of incidents")
plt.title("Number of incidents versus species")

if st.checkbox('Click to show the species'):
    st.pyplot(fig_a)
    st.write("These species are:",ani_sorted2)

    st.write("Gull is the most dangerous identified animal for aircrafts.")



st.subheader("Damage parts")
st.write("What part of the plane is damaged?")

fig_s = plt.figure(figsize=(10, 4))
sns.heatmap(data.iloc[:,36:44])
fig_s2 = plt.figure(figsize=(10, 4))
sns.heatmap(data.iloc[:,44:52])
fig_s3 = plt.figure(figsize=(10, 4))
sns.heatmap(data.iloc[:,52:66])

if st.checkbox('Click to show the damaged parts'):

    st.pyplot(fig_s)
    st.pyplot(fig_s2)
    st.pyplot(fig_s3)
    st.write("We can see that front parts are being damaged more then rear parts")
    st.write("There are two parts of this graph, strike and damage. If there is a strike, there isn't always a damage.")
    

st.subheader("Engine strike")
st.write("And not surprisingly, if there is a engine strike, there is always an engine damage.")

test = data.iloc[:,45] + data.iloc[:,47] + data.iloc[:,49] + data.iloc[:,43]
test[test > 0 ] = 1
data.insert(0,"Engine strike",test)


if st.checkbox('Click to show the strike/damage plot'):
    option = st.selectbox(
    'I will let you decide this time! Select a color',
    ("viridis","crest","flare","magma","rocket_r"))

    st.write('You selected:', option)

    fig_s4 = plt.figure(figsize=(10, 8))
    sns.heatmap(data.iloc[:,[0,52]], cmap=option)
    st.pyplot(fig_s4)



st.header("Lastly")

st.write("What months do Gull, Mourning Dove and Sparrow cause the most trouble?")

gull = data[data["Species Name"] == "GULL"]
md = data[data["Species Name"] == "MOURNING DOVE"]
sp = data[data["Species Name"] == "SPARROW"]
last = gull.append(md)
last = last.append(sp)

m1 = gull[gull["Incident Month"] == 1]
m1["tt"] = len(m1["Incident Month"])
m2 = gull[gull["Incident Month"] == 2]
m2["tt"] = len(m2["Incident Month"])
m3 = gull[gull["Incident Month"] == 3]
m3["tt"] = len(m3["Incident Month"])
m4 = gull[gull["Incident Month"] == 4]
m4["tt"] = len(m4["Incident Month"])
m5 = gull[gull["Incident Month"] == 5]
m5["tt"] = len(m5["Incident Month"])
m6 = gull[gull["Incident Month"] == 6]
m6["tt"] = len(m6["Incident Month"])
m7 = gull[gull["Incident Month"] == 7]
m7["tt"] = len(m7["Incident Month"])
m8 = gull[gull["Incident Month"] == 8]
m8["tt"] = len(m8["Incident Month"])
m9 = gull[gull["Incident Month"] == 9]
m9["tt"] = len(m9["Incident Month"])
m10 = gull[gull["Incident Month"] == 10]
m10["tt"] = len(m10["Incident Month"])
m11 = gull[gull["Incident Month"] == 11]
m11["tt"] = len(m11["Incident Month"])
m12 = gull[gull["Incident Month"] == 12]
m12["tt"] = len(m12["Incident Month"])


mm1 = md[md["Incident Month"] == 1]
mm1["tt"] = len(mm1["Incident Month"])
mm2 = md[md["Incident Month"] == 2]
mm2["tt"] = len(mm2["Incident Month"])
mm3 = md[md["Incident Month"] == 3]
mm3["tt"] = len(mm3["Incident Month"])
mm4 = md[md["Incident Month"] == 4]
mm4["tt"] = len(mm4["Incident Month"])
mm5 = md[md["Incident Month"] == 5]
mm5["tt"] = len(mm5["Incident Month"])
mm6 = md[md["Incident Month"] == 6]
mm6["tt"] = len(mm6["Incident Month"])
mm7 = md[md["Incident Month"] == 7]
mm7["tt"] = len(mm7["Incident Month"])
mm8 = md[md["Incident Month"] == 8]
mm8["tt"] = len(mm8["Incident Month"])
mm9 = md[md["Incident Month"] == 9]
mm9["tt"] = len(mm9["Incident Month"])
mm10 = md[md["Incident Month"] == 10]
mm10["tt"] = len(mm10["Incident Month"])
mm11 = md[md["Incident Month"] == 11]
mm11["tt"] = len(mm11["Incident Month"])
mm12 = md[md["Incident Month"] == 12]
mm12["tt"] = len(mm12["Incident Month"])

sm1 = sp[sp["Incident Month"] == 1]
sm1["tt"] = len(sm1["Incident Month"])
sm2 = sp[sp["Incident Month"] == 2]
sm2["tt"] = len(sm2["Incident Month"])
sm3 = sp[sp["Incident Month"] == 3]
sm3["tt"] = len(sm3["Incident Month"])
sm4 = sp[sp["Incident Month"] == 4]
sm4["tt"] = len(sm4["Incident Month"])
sm5 = sp[sp["Incident Month"] == 5]
sm5["tt"] = len(sm5["Incident Month"])
sm6 = sp[sp["Incident Month"] == 6]
sm6["tt"] = len(sm6["Incident Month"])
sm7 = sp[sp["Incident Month"] == 7]
sm7["tt"] = len(sm7["Incident Month"])
sm8 = sp[sp["Incident Month"] == 8]
sm8["tt"] = len(sm8["Incident Month"])
sm9 = sp[sp["Incident Month"] == 9]
sm9["tt"] = len(sm9["Incident Month"])
sm10 = sp[sp["Incident Month"] == 10]
sm10["tt"] = len(sm10["Incident Month"])
sm11 = sp[sp["Incident Month"] == 11]
sm11["tt"] = len(sm11["Incident Month"])
sm12 = sp[sp["Incident Month"] == 12]
sm12["tt"] = len(sm12["Incident Month"])


total = pd.concat([m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12,mm1,mm2,mm3,mm4,mm5,mm6,mm7,mm8,mm9,mm10,mm11,mm12,sm1,sm2,sm3,sm4,sm5,sm6,sm7,sm8,sm9,sm10,sm11,sm12])

total = total.rename(columns={"tt": "Total incidents"})

altc = alt.Chart(total).mark_tick().encode(
    y='Species Name',
    x='Incident Month',
    color=alt.Color('Total incidents',
      scale=alt.Scale(domainMid=0, scheme='redblue')),
    tooltip=['Incident Year', 'Incident Month', 'Incident Day', 'Operator', 'Aircraft', 'Airport', 'Total incidents']
).interactive()

st.altair_chart(altc,use_container_width=True)