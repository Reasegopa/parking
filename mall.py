import math

# mall details - each mall has different pricing so i kept them separate
# got the capacities from the assignment brief
mall_data = {
    "Gateway": {
        "full_name": "Gateway Theatre of Shopping (Umhlanga, Durban)",
        "pricing": "flat",
        "rate": 15.00,
        "capacity": 250,
    },
    "Pavilion": {
        "full_name": "Pavilion Shopping Centre (Westville, Durban)",
        "pricing": "hourly",
        "rate": 10.00,
        "capacity": 180,
    },
    "La Lucia": {
        "full_name": "La Lucia Mall (La Lucia, Durban)",
        "pricing": "capped_hourly",
        "rate": 12.00,
        "daily_max": 60.00,
        "capacity": 150,
    }
}

# just a list so i can loop through them in order
MALL_NAMES = ["Gateway", "Pavilion", "La Lucia"]

# keeping MALLS as an alias so other files dont break
MALLS = mall_data


def pricing_info(mname):
    m = mall_data[mname]
    if m["pricing"] == "flat":
        return "Flat Rate - R" + str(m["rate"]) + " per visit"
    elif m["pricing"] == "hourly":
        return "Hourly - R" + str(m["rate"]) + "/hour (rounded up to next hour)"
    elif m["pricing"] == "capped_hourly":
        return "Hourly - R" + str(m["rate"]) + "/hour, max R" + str(m["daily_max"]) + " per day"
    return "N/A"

# kept this name so other files can still import it
def get_pricing_description(mname):
    return pricing_info(mname)


def calc_fee(mname, entry_dt, exit_dt):
    m = mall_data[mname]

    secs = (exit_dt - entry_dt).total_seconds()
    if secs < 60:
        secs = 60  # minimum 1 min, just in case someone exits immediately

    hrs = secs / 3600
    billed_hrs = math.ceil(hrs)

    if m["pricing"] == "flat":
        fee = m["rate"]
        desc = "Flat Rate"

    elif m["pricing"] == "hourly":
        fee = billed_hrs * m["rate"]
        desc = "Hourly (" + str(billed_hrs) + "h)"

    elif m["pricing"] == "capped_hourly":
        fee = billed_hrs * m["rate"]
        if fee > m["daily_max"]:
            fee = m["daily_max"]
        desc = "Capped Hourly (" + str(billed_hrs) + "h, cap R" + str(m["daily_max"]) + ")"
    else:
        fee = 0
        desc = "?"

    return round(fee, 2), desc

# alias so parking.py doesnt need changes
def calculate_parking_fee(mname, entry_dt, exit_dt):
    return calc_fee(mname, entry_dt, exit_dt)
