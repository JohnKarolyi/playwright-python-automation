import datetime

def safe_fill(page, selector, value):
    val_str = str(value)
    
    # 1. Normál dátum formázás (ha óra/perc/másodperc is jön az Excelből)
    if selector == "#birth_date" and " " in val_str:
        val_str = val_str.split(" ")[0]
        
    # 2. Speciális kezelés az érvénytelen (szöveges) életkorhoz
    if selector == "#age":
        try:
            float(val_str)
            page.fill(selector, val_str)
        except ValueError:
            page.locator(selector).focus()
            page.locator(selector).clear()
            page.locator(selector).type(val_str)
            
    # 3. Speciális kezelés a hibás vagy érvénytelen dátumokhoz (pl. "invalid", "2025-99-99")
    elif selector == "#birth_date":
        is_valid_date = True
        try:
            # Megpróbáljuk értelmezni mint valós dátumot
            datetime.datetime.strptime(val_str, "%Y-%m-%d")
        except ValueError:
            is_valid_date = False
            
        if not is_valid_date:
            # Ha hibás a dátum (szöveg vagy valótlan számok), billentyűleütéssel írjuk be
            page.locator(selector).focus()
            page.locator(selector).clear()
            page.locator(selector).type(val_str)
        else:
            # Ha teljesen jó a dátum, mehet a gyors fill
            page.fill(selector, val_str)
        
    else:
        # Minden más normál mezőre (név, email)
        page.fill(selector, val_str)