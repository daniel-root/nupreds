def get_campus_name (campus):
    # check campus code
    campuses = []
    
    campus = campus.upper()
    
    campus_name = None
    if campus == "CBA":
        campus_name = "Bakersfield"

    if campus == "U$C":
        campus_name = "Channel Islands"

    if campus == "CCH":
        campus_name = "Chico"

    if campus == "CDH":
        campus_name = "Dominguez Hills"

    if campus == "CSH":
        campus_name = "East Bay"

    if campus == "CFS":
        campus_name = "Fresno"

    if campus == "CFI":
        campus_name = "Fullerton"

    if campus == "CHU":
        campus_name = "Humboldt"

    if campus == "CLO":
        campus_name = "Long Beach"

    if campus == "CLA":
        campus_name = "Los Angeles"

    if campus == "CVM":
        campus_name = "Maritime Academy"

    if campus == "MB@":
        campus_name = "Monterey Bay"

    if campus == "MFL":
        campus_name = "Moss Landing"

    if campus == "CNO":
        campus_name = "Northridge"

    if campus == "CPO":
        campus_name = "Pomona"

    if campus == "CSA":
        campus_name = "Sacramento"

    if campus == "CSB":
        campus_name = "San Bernardino"
    
    if campus == "CDS":
        campus_name = "San Diego"

    if campus == "CSF":
        campus_name = "San Francisco"

    if campus == "CSJ":
        campus_name = "San Jose"

    if campus == "CPS":
        campus_name = "San Luis Obispo"

    if campus == "CS1":
        campus_name = "San Marcos"

    if campus == "CSO":
        campus_name = "Sonoma"

    if campus == "CTU":
        campus_name = "Stanislaus"
        
    return campus_name