import pandas as pd

df = pd.read_excel("C:\\Users\\ZiyiH\\Desktop\\SA\\data\\TD_datasource_71.xlsx", sheet_name="Tabelle1")

# generate subtypset e.g.:db = [[{'a'}, {'a', 'b', 'c'}, {'a', 'c'}, {'d'}, {'c', 'f'}],[{'a'}, {'a', 'b', 'c'}, {'a', 'c'}, {'d'}, {'c', 'f'}]]

subtypset=[]
for i in range(len(df)):
    row = df.iloc[i]

    Personnumber=str(row["#Interview"])
    IncidentNumber=str(row["#TDincident"])
    TDItem=str(row["#TDitem"])
    itemNumber=row["#TDitem"]
    IncidentID=Personnumber+'-'+IncidentNumber

    Subtyp=row["TD Subtype (Li+own)"].capitalize()
    

# add relation between td items (item lead to next item)
    if i==0:
        count_incident=0
        subtypset.append([{Subtyp}])
        OldIncidentID=IncidentID  
        OlditemNumber=itemNumber
    if IncidentID == OldIncidentID:
        if itemNumber==OlditemNumber:
            subtypset[count_incident][itemNumber-1].add(Subtyp)
        if itemNumber==OlditemNumber+1:
            subtypset[count_incident].append({Subtyp})
            OlditemNumber=itemNumber
        OldIncidentID=IncidentID
    if IncidentID != OldIncidentID:
        count_incident=count_incident+1
        subtypset.append([{Subtyp}]) 
        OldIncidentID=IncidentID
        OlditemNumber=itemNumber


# prefixspan
from multiprefixspan import prefixspan_multiple_items_one_event

pre_object = prefixspan_multiple_items_one_event(subtypset, 2)
pre_object.exect()
pt=pre_object.found_patterns

def rankfreq(elem):
    return elem[-1]
pt.sort(key=rankfreq,reverse = True)


# export
pt=pd.DataFrame(pt)
pt.columns = ['pattern','frequency']

#print(len(pt['pattern'].loc[1]))
#filter out the pattern,delete single cause
rows  = [x for x in pt.index if len(pt.loc[x]['pattern'])==1]
pt = pt.drop(rows,axis=0)

pt.to_excel('C:\\Users\\ZiyiH\\Desktop\\SA\\data\\prefixspan\\Subtyppattern.xlsx',index=False, header=True,encoding='utf-8')