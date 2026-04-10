from datetime import datetime
from storage import load_json, save_json
from mall import mall_data, calculate_parking_fee, get_pricing_description

PARK_FILE = "data/parking.json"


def load_records():
    return load_json(PARK_FILE, [])


def save_records(recs):
    save_json(PARK_FILE, recs)


def get_current_occupancy(mname):
    recs = load_records()
    count = 0
    for r in recs:
        if r["mall"] == mname and r["exit_time"] == None:
            count = count + 1
    return count


def enter_parking(user, mname):
    m = mall_data[mname]
    recs = load_records()

    # dont let the same customer park twice at the same mall
    for r in recs:
        if r["username"] == user["username"] and r["mall"] == mname and r["exit_time"] == None:
            print("")
            print("You already have an open session at " + mname + ".")
            print("Entry was at: " + r["entry_time"])
            return False

    occ = get_current_occupancy(mname)
    if occ >= m["capacity"]:
        print("")
        print(mname + " is full (" + str(m["capacity"]) + " vehicles). Cannot enter.")
        return False

    now = datetime.now()

    new_rec = {
        "username": user["username"],
        "mall": mname,
        "entry_time": now.isoformat(),
        "exit_time": None,
        "mins_parked": None,
        "fee": None,
        "fee_type": None,
        "paid": False
    }

    recs.append(new_rec)
    save_records(recs)

    free = m["capacity"] - occ - 1
    print("")
    print("Entry recorded!")
    print("Mall      : " + m["full_name"])
    print("Time in   : " + now.strftime("%Y-%m-%d %H:%M:%S"))
    print("Pricing   : " + get_pricing_description(mname))
    print("Spaces    : " + str(free) + " remaining")
    return True


def exit_parking(user, mname):
    recs = load_records()

    for r in recs:
        if r["username"] == user["username"] and r["mall"] == mname and r["exit_time"] == None:

            time_in = datetime.fromisoformat(r["entry_time"])
            time_out = datetime.now()

            fee, ftype = calculate_parking_fee(mname, time_in, time_out)

            diff_secs = (time_out - time_in).total_seconds()
            mins = round(diff_secs / 60, 1)

            r["exit_time"] = time_out.isoformat()
            r["mins_parked"] = mins
            r["fee"] = fee
            r["fee_type"] = ftype

            save_records(recs)

            h = int(mins // 60)
            m2 = int(mins % 60)

            print("")
            print("=== Exit Summary ===")
            print("Mall      : " + mall_data[mname]["full_name"])
            print("Entered   : " + time_in.strftime("%Y-%m-%d %H:%M:%S"))
            print("Exited    : " + time_out.strftime("%Y-%m-%d %H:%M:%S"))
            print("Time      : " + str(h) + "h " + str(m2) + "m")
            print("Rate type : " + ftype)
            print("Total due : R" + str(fee))
            return fee, ftype

    print("")
    print("Couldnt find an active session for you at " + mname + ".")
    return 0, ""


def get_user_parking_history(uname):
    recs = load_records()
    done = []
    for r in recs:
        if r["username"] == uname and r["exit_time"] != None:
            done.append(r)
    return done


def get_active_sessions(mname):
    recs = load_records()
    active = []
    for r in recs:
        if r["mall"] == mname and r["exit_time"] == None:
            active.append(r)
    return active


def get_completed_records(mname=None):
    recs = load_records()
    done = []
    for r in recs:
        if r["exit_time"] != None:
            if mname == None or r["mall"] == mname:
                done.append(r)
    return done
