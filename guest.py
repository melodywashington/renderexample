import psycopg2

# Connect to the guestlist database
conn = psycopg2.connect(
    dbname="guestlist",
    user="render_postgres_8swb_user",  # replace with your postgres role
    #password="your_password",  # if required
    host="localhost"
)

cur = conn.cursor()

# Insert form data into the table
cur.execute("INSERT INTO guests (name, message) VALUES (%s, %s)", ("Melody", "Example message here!"))
conn.commit()

cur.close()
conn.close()
