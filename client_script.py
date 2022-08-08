import sqlite3

# establish database connection and cursor object
connection = sqlite3.connect('interview.db')
cur = connection.cursor()

# combine rosters
def create_roster_table():
    cur.execute('CREATE TABLE std_member_info AS SELECT Person_Id AS member_id, First_Name AS member_first_name, Last_Name AS member_last_name, Dob AS date_of_birth, Street_Address AS main_address, City AS city, State AS state, Zip AS zip_code, payer AS payer FROM roster_1 WHERE eligibility_start_date <= "2022-04-01" AND eligibility_end_date >= "2022-05-01" UNION SELECT Person_Id AS member_id, First_Name AS member_first_name, Last_Name AS member_last_name, Dob AS date_of_birth, Street_Address AS main_address, City AS city, State AS state, Zip AS zip_code, payer AS payer FROM roster_2 WHERE eligibility_start_date <= "04/01/2022" AND eligibility_end_date >= "05/01/2022" UNION SELECT Person_Id AS member_id, First_Name AS member_first_name, Last_Name AS member_last_name, Dob AS date_of_birth, Street_Address AS main_address, City AS city, State AS state, Zip AS zip_code, payer AS payer FROM roster_3 WHERE eligibility_start_date <= "2022-04-01" AND eligibility_end_date >= "2022-05-01" UNION SELECT Person_Id AS member_id, First_Name AS member_first_name, Last_Name AS member_last_name, Dob AS date_of_birth, Street_Address AS main_address, City AS city, State AS state, Zip AS zip_code, payer AS payer FROM roster_4 WHERE eligibility_start_date <= "2022-04-01" AND eligibility_end_date >= "2022-05-01" UNION SELECT Person_Id AS member_id, First_Name AS member_first_name, Last_Name AS member_last_name, Dob AS date_of_birth, Street_Address AS main_address, City AS city, State AS state, Zip AS zip_code, payer AS payer FROM roster_5 WHERE eligibility_start_date <= "2022-04-01" AND eligibility_end_date >= "2022-05-01";')


# (1)
def distinct_members():
    cur.execute('SELECT COUNT(DISTINCT member_id) FROM std_member_info;')
    
    print('[Distinct Members]\n')
    for row in cur.fetchall():
        print(row[0])

    print("\n#############################################################")


# (2)
def multiple_member_entries():
    #cur.execute('SELECT member_id, COUNT(*) AS triples_count FROM 'std_member_info' GROUP BY member_id HAVING COUNT(*) > 2;')
    cur.execute('SELECT COUNT(member_id) - COUNT(DISTINCT member_id) FROM std_member_info;')   
    
    print('[Multiple Member Entries]\n')
    for row in cur.fetchall():
        print(row[0])

    print("\n#############################################################")


# (3)
def members_by_payer():
    cur.execute('SELECT payer, COUNT(*) FROM std_member_info GROUP BY payer;')

    print("[Quantity by Payer]\n")
    for row in cur.fetchall():
        print(row[0] + ":", row[1])

    print("\n#############################################################")
    

# (4)
def food_access_by_zip():
    cur.execute('SELECT SUM(CASE WHEN food_access_score < 2 THEN 1 ELSE 0 END) AS low_food_access FROM std_member_info JOIN model_scores_by_zip ON std_member_info.zip_code = model_scores_by_zip.zcta;')

    print("[Members w/ Low Food Access Score]\n")
    for row in cur.fetchall():
        print(row[0])
        
    print("\n#############################################################")


# (5)
def avg_isolation_score():
    cur.execute('SELECT AVG(social_isolation_score) FROM std_member_info JOIN model_scores_by_zip ON std_member_info.zip_code = model_scores_by_zip.zcta;')
    
    print("[Average Isolation Score]\n")
    for row in cur.fetchall():
        print(row[0])
        
    print("\n#############################################################")


# (6)
def high_composite_zip_members():
    #cur.execute('SELECT MAX(algorex_sdoh_composite_score) FROM model_scores_by_zip;')
    cur.execute('SELECT member_id, member_first_name, member_last_name, MAX(algorex_sdoh_composite_score) AS highest_composite_score FROM std_member_info JOIN model_scores_by_zip ON std_member_info.zip_code = model_scores_by_zip.zcta GROUP BY member_id HAVING algorex_sdoh_composite_score = 8.77;')

    print('[Member List in Highest Composite Zip Code]\n')
    for row in cur.fetchall():
        print("Member ID: ", row[0])
        print("Name: ", row[1], row[2])
        print("SDOH Score: ", row[3])
        print("\n")

    print("#############################################################")



#call functions

create_roster_table()
distinct_members()
multiple_member_entries()
members_by_payer()
food_access_by_zip()
avg_isolation_score()
high_composite_zip_members()


#close connection
cur.close()
connection.close()