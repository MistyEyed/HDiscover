import requests
import math as m
import sqlite3 as s
import streamlit as st
import pandas as pd

# HDiscover: User Discovery & Ranking System {IN PROGRESS}
# MiniProject - Harshith Chegondi
# 17-Dec'2025 to 26-Dec'25

def fetch_user():
  url = "https://randomuser.me/api/"
  response = requests.get(url) #creates a connection with url
  data = response.json()  #convert to json format

  if("results" in data):
    user_data = data["results"][0]
    user_name = user_data["name"]["first"] + " " + user_data["name"]["last"]
    user_gender = user_data["gender"]
    user_lat = float(user_data["location"]["coordinates"]["latitude"])
    user_long = float(user_data["location"]["coordinates"]["longitude"])
    return User(user_data["login"]["uuid"], user_name, user_gender, user_lat, user_long)

  else:
    raise Exception("Error 1: Failed to Fetch User Data")


def fetch_multple(count):
  url = f"https://randomuser.me/api/?results={count}"
  response = requests.get(url)
  data = response.json()

  if( int(count) > 0 and "results" in data):
    user_list = []
    for x in data["results"]:
      user_list.append(User(x["login"]["uuid"], x["name"]["first"] + " " + x["name"]["last"], x["gender"], float(x["location"]["coordinates"]["latitude"]), float(x["location"]["coordinates"]["longitude"])))
    return user_list
  else:
    raise Exception("Error 2: Failed to Fetch Users Data")


def merge(dist, low, mid, high):
  n1 = mid - low + 1
  n2 = high - mid
  a = [0] * n1
  b = [0] * n2

  for i in range(n1):
    a[i] = dist[low + i]
  for j in range(n2):
    b[j] = dist[mid + 1 + j]

  i = j = 0
  k = low

  while i < n1 and j < n2:
    if a[i][3] <= b[j][3]:
      dist[k] = a[i]
      i += 1
    else:
      dist[k] = b[j]
      j += 1
    k += 1

  while i < n1:
    dist[k] = a[i]
    i += 1
    k += 1

  while j < n2:
    dist[k] = b[j]
    j += 1
    k += 1

def mergeSort(dist, low, high): #using merge-sort but can use default pythonic sorting(better)
  if low < high:
    mid = (low + high) // 2
    mergeSort(dist, low, mid)
    mergeSort(dist, mid + 1, high)
    merge(dist, low, mid, high)


class User:
  def __init__(self, uuid, name, gender, latitude, longitude):
    self.uuid = uuid
    self.name = name
    self.gender = gender
    self.latitude = latitude
    self.longitude = longitude

  def distance(self, user2): #Haversine Distance for greater approximation than euclidean 
    R = 6371  # Earth radius in kilometers

    lat1 = m.radians(self.latitude)
    lon1 = m.radians(self.longitude)
    lat2 = m.radians(user2.latitude)
    lon2 = m.radians(user2.longitude)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = m.sin(dlat / 2)**2 + m.cos(lat1) * m.cos(lat2) * m.sin(dlon / 2)**2
    c = 2 * m.asin(m.sqrt(a))

    return R * c
  


#DataBase: SQLITE3
conn = s.connect("UserData.db")
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS userdata(
            uuid TEXT PRIMARY KEY,
            name TEXT,
            gender TEXT,
            latitude REAL,
            longitude REAL
            )""")
# cur.execute("DELETE FROM userdata") 
# use this command if you want empty userbase for new entries

cur.execute("""CREATE TABLE IF NOT EXISTS solution(
            uuid TEXT PRIMARY KEY,
            name TEXT,
            gender TEXT,
            latitude REAL,
            longitude REAL
          )""")

cur.execute("DELETE FROM solution") #table is independent for every new entry
conn.commit()

#Frontend: Streamlit
st.title("HDiscovery: User Discovery & Ranking")
st.markdown("""
            ### Discover and rank users based on Geographic Proximity.
            **Author**: Harshith Chegondi""")
st.divider()
st.header("About")
st.markdown("""HDiscover(mini-project) is a prototype system that fetches user data from _randomuser.me_, calculates distances between users, and ranks them using a **custom Merge Sort algorithm**. The system demonstrates **API integration**, **algorithm design**, and **user ranking logic**.""")
st.divider()
st.subheader("Fetch Users")
x = st.slider(    #adds a nice slider animation for interactivity
  "**No. of users to fetch**:",
  min_value=10,
  max_value=200,
  value=100,
  step=10
)
st.divider()

chk = st.button("Fetch a Random User") #returns boolean true if clicked.

    
def main():
  if chk:
    try:
      random_user = fetch_user()
      st.subheader("Selected User")
      st.write(f"""
              **Details:**
                - UUID: {random_user.uuid}
                - Name: {random_user.name}
                - Gender: {random_user.gender}
                - Latitude: {random_user.latitude}
                - Longitude: {random_user.longitude}
           """)
      
      for i in fetch_multple(x):
        cur.execute("INSERT OR IGNORE INTO userdata VALUES(?, ?, ?, ?, ?)", (i.uuid, i.name, i.gender, i.latitude, i.longitude))
      conn.commit()

      query = cur.execute("SELECT * FROM userdata WHERE gender != ?", (random_user.gender,))
      req_users = cur.fetchall()

      dist = []
      for i in req_users:
        temp = User(i[0], i[1], i[2], i[3], i[4])
        dist.append((temp.uuid, temp.name, temp.gender, random_user.distance(temp)))

      if dist:
        mergeSort(dist, 0, len(dist)-1)
      

      for j in range(0,min(100, len(dist))):
        cur.execute("""INSERT INTO solution(uuid, name, gender, latitude, longitude)
                    SELECT uuid, name, gender, latitude, longitude
                    FROM userdata WHERE uuid = ?
                    """, (dist[j][0],))

#Table(frontend):
      st.subheader("Nearest Users")
      df = pd.read_sql("SELECT name, gender FROM solution", conn)
      st.dataframe(df)
      st.divider()
#Map(frontend): 
      st.subheader("User Location Map")
      df1 = pd.read_sql("SELECT latitude, longitude FROM solution", conn)
      st.map(df1)
      st.caption(f"Showing {len(df1)} nearest users on map")
        
    except Exception as e:
      print(str(e))

if __name__ == "__main__":
  main()

conn.commit()
conn.close()
