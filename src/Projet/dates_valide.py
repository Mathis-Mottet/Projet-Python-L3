from datetime import datetime

def Dates_Valide(start_date_str: str, end_date_str: str):
    
    date_format="%d/%m/%Y"

    try:
        start_date = datetime.strptime(start_date_str, date_format)
    except ValueError:
        raise ValueError("La date de début doit être au format dd/mm/yyyy")

    try:
        end_date = datetime.strptime(end_date_str, date_format)
    except ValueError:
        raise ValueError("La date de fin doit être au format dd/mm/yyyy")

    if start_date >= end_date:
        raise ValueError(f"La date de début {start_date_str} doit être antérieure à la date de fin {end_date_str}")

    if end_date > datetime.today():
        raise ValueError(f"La date de fin {end_date_str} ne peut pas être supérieure à aujourd'hui ({datetime.today().strftime(date_format)})")

    return start_date, end_date