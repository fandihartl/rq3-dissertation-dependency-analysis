import pandas as pd
from py2neo import Graph

SCHEME = "bolt"
HOST = "localhost"
USERNAME = 'neo4j'
PASSWORD = '112211'

graph = Graph(scheme=SCHEME, host=HOST, auth=(USERNAME, PASSWORD))


df = pd.read_excel("C:\\Users\\ZiyiH\\Desktop\\SA\\data\\CodingPatterns_test.xlsx", sheet_name="Tabelle1")

for i in range(len(df)):
    row = df.iloc[i]
    Personnumber=str(row["#interview"])
    IncidentNumber=str(row["#Tdincident"])
    itemNumber=row["#Tditem"]
    TDItem=str(row["#Tditem"])
    causeid=str(row["TD Cause ID"])
    TDID=Personnumber+'-'+IncidentNumber+'-'+TDItem
    Incident=row["TD incident description"]
    TDType=str(row["TD type"])
    TDSubtype=str(row["TD subtype"]).strip().capitalize()
    Cause=str(row["TD cause"]).strip().capitalize()
    MeasureSoll=str(row["(missing) TD measure"]).strip().capitalize()
    CurrentState=str(row["Current state/TD consequence"]).strip().capitalize()
    initparty=row["Initiating party"].split(',')
    affparty=row["Affected party"].split(',')
    
    
#add person
    add_person ="MERGE (p:Person {name:'"+Personnumber+"'})"
    graph.run(add_person)

#add person-report->incident
    add_incident="match (p:Person {name:'"+Personnumber+"'}) merge (incident:TDIncident {name:'"+Incident+"'}) MERGE (p)-[:REPORTED]->(incident)"
    graph.run(add_incident)

# add td incident->td item
    add_tditem =" match (incident:TDIncident {name:'"+Incident+"'}) merge (item:TDItem {ID:'"+TDID+"'}) merge(incident)<-[:IS_PART_OF]-(item)"
    graph.run(add_tditem)

# add tditem-affect-party 
    for party in affparty:
        party=party.strip()
        add_affparty="match (item:TDItem {ID:'"+TDID+"'}) merge ("+party[0:7]+":Party {name:'"+party+"'})  merge (item)-[:AFFECTS]->("+party[0:7]+")"
        graph.run(add_affparty)
# add tditem-initiate-party 
    for party in initparty:
        party=party.strip()
        add_initparty="match (item:TDItem {ID:'"+TDID+"'})  merge ("+party[0:7]+":Party {name:'"+party+"'})   merge (item)<-[:INITIATES]-("+party[0:7]+")"
        graph.run(add_initparty)

# add relation between td items (item lead to next item)
    if i==0:
        OldIncidentNumber="0"
        OlditemNumber= 0
    if itemNumber ==1:
        pass
    elif IncidentNumber==OldIncidentNumber and itemNumber == OlditemNumber+1:
        add_item_relation=" match (item:TDItem {ID:'"+TDID+"'}), (olditem:TDItem {ID:'"+OldTDID+"'}) merge (olditem)-[:LEAD_TO]->(item)"
        graph.run(add_item_relation)
    else:
        print("wrong order of item in line", i+1 )

    OldIncidentNumber=IncidentNumber
    OlditemNumber= itemNumber
    OldTDID=TDID


    