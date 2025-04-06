from flask import Flask, render_template, request
import random
import pymysql

app = Flask(__name__)

# MySQL database connection using PyMySQL
def insert_ride(pickup, dropoff, distance, fare, ride_time):
    print("🛠 Connecting to MySQL...")
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="1234",  # Use your actual password
        database="cabfaredb"
    )
    print("🔌 Connected to MySQL!")

    cursor = conn.cursor()
    print("🖝 Preparing to insert...")

    query = "INSERT INTO rides (pickup, dropoff, distance, fare, ride_time) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (pickup, dropoff, distance, fare, ride_time))

    print("🛄 Executing query...")
    conn.commit()
    print("💾 Committed to DB.")

    conn.close()
    print("🔒 Connection closed.")


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/estimate', methods=['POST'])
def estimate():
    try:
        pickup = request.form['pickup']
        dropoff = request.form['dropoff']
        print(f"Pickup: {pickup}, Dropoff: {dropoff}")

        rides = []
        for _ in range(5):
            distance = round(random.uniform(5, 20), 2)
            fare = round(distance * random.uniform(10, 15), 2)
            ride_time = random.randint(15, 45)
            rides.append({'fare': fare, 'ride_time': ride_time, 'distance': distance})

        print("Rides:", rides)

        best_ride = min(rides, key=lambda x: x['fare'] + x['ride_time'] * 0.5)
        print("Best ride:", best_ride)

        try:
            print("📅 Trying to insert into DB...")
            insert_ride(pickup, dropoff, best_ride['distance'], best_ride['fare'], best_ride['ride_time'])
            print("✅ Best ride inserted into the database successfully!")
        except Exception as e:
            print("⚠️ Database Error:", e)

        return render_template('index.html', rides=rides, best_ride=best_ride)

    except Exception as e:
        print("🔥 Unexpected Error:", e)
        return "Something went wrong", 500

if __name__ == '__main__':
    app.run(debug=True)
