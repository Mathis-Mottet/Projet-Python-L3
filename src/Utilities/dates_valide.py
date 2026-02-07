from datetime import datetime

def Dates_Valide(start_date_str: str, end_date_str: str):
    
    date_format="%d/%m/%Y"

    try:
        start_date=datetime.strptime(start_date_str, date_format)
        end_date=datetime.strptime(end_date_str, date_format)
    except ValueError:
        raise ValueError(f"Les dates doivent être dans le format{date_format}")
    
    if start_date>=end_date:
        raise ValueError(f"{start_date} est supérieur à {end_date} ce qui est impossible")
    
    if end_date > datetime.today():
        raise ValueError(f"{end_date} ne peut pas être supérieur à aujourd'hui : {datetime.today()}")
    
    return start_date, end_date