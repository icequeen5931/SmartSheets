__author__ = 'jpisano'

import mysql.connector
from settings import database

class Coverage:
    def __init__(self):
        # Load Values and Init Object
        cnx = mysql.connector.connect(user=database['USER'],
                                      password=database['PASSWORD'],
                                      host=database['HOST'],
                                      database=database['DATABASE'])
        mycursor = cnx.cursor()
        mycursor.execute("SELECT * FROM coverage")
        team_coverage = mycursor.fetchall()
        cnx.close()

        # Arrange coverage table into Dict of territories and a teams
        self.team_dict = {}
        for territory in team_coverage:
            pss = territory[0]
            tsa = territory[1]
            key = (territory[2] + territory[3] + territory[4] + territory[5] + territory[6]).strip()
            key = key.replace('*', '')
            if len(key)==0:
                key = '*'

            #Create a Dict of territories with a List of team(s) covering each territory
            info = self.team_dict.get(key, [])
            info.append((pss,tsa))
            self.team_dict[key] = info

    def find_team(self,sales_lvl):
        teams = []
        # Look for the team(s) with the longest match on the territory
        longest_match = 0
        pss = []
        tsa = []
        for k,v in self.team_dict.items():

            if sales_lvl.startswith (k, 0, len(k)):
                if len(k) >= longest_match:
                    pss = []
                    tsa = []
                    longest_match= len(k)
                    self.team = v
                    for team in v:
                        pss.append(team[0])
                        tsa.append(team[1])

        tsa = tuple(tsa)
        pss = tuple(pss)
        self.team = [pss,tsa]

        return(self.team)

if __name__ == "__main__":
    jim = Coverage()
    print (jim)