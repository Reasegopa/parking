import csv
import os
from datetime import datetime
from mall import mall_data, MALL_NAMES
from parking import get_completed_records, get_active_sessions, get_current_occupancy
from payments import get_mall_payments

REPORTS_DIR = "data/reports"


def get_mall_stats(mname):
    done = get_completed_records(mname)
    pay_recs = get_mall_payments(mname)
    currently_in = get_active_sessions(mname)

    num_vehicles = len(done)

    rev = 0
    for p in pay_recs:
        rev = rev + p["amount"]

    # work out average time spent parked
    total_mins = 0
    valid = 0
    for r in done:
        if r["mins_parked"] != None:
            total_mins = total_mins + r["mins_parked"]
            valid = valid + 1

    if valid > 0:
        avg_mins = round(total_mins / valid, 1)
    else:
        avg_mins = 0

    return {
        "name": mname,
        "full_name": mall_data[mname]["full_name"],
        "pricing": mall_data[mname]["pricing"],
        "cap": mall_data[mname]["capacity"],
        "active": len(currently_in),
        "served": num_vehicles,
        "revenue": round(rev, 2),
        "avg_mins": avg_mins
    }


def print_mall_report(mname):
    s = get_mall_stats(mname)
    print("")
    print("=" * 50)
    print("  " + s["full_name"])
    print("=" * 50)
    print("  Pricing      : " + s["pricing"].replace("_", " ").title())
    print("  Capacity     : " + str(s["cap"]))
    print("  Now parked   : " + str(s["active"]))
    print("  Total served : " + str(s["served"]))
    print("  Revenue      : R" + str(s["revenue"]))
    print("  Avg time     : " + str(s["avg_mins"]) + " min")
    print("=" * 50)


def print_cross_mall_report():
    print("")
    print("=" * 60)
    print("  ALL MALLS - COMPARISON REPORT")
    print("  " + datetime.now().strftime("%Y-%m-%d %H:%M"))
    print("=" * 60)

    total_rev = 0
    total_served = 0

    for mname in MALL_NAMES:
        s = get_mall_stats(mname)
        total_rev = total_rev + s["revenue"]
        total_served = total_served + s["served"]

        print("")
        print("  " + s["full_name"])
        print("  Pricing  : " + s["pricing"].replace("_", " ").title())
        print("  Active   : " + str(s["active"]))
        print("  Served   : " + str(s["served"]))
        print("  Revenue  : R" + str(s["revenue"]))
        print("  Avg stay : " + str(s["avg_mins"]) + " min")
        print("  " + "-" * 45)

    print("")
    print("  Combined total vehicles : " + str(total_served))
    print("  Combined revenue        : R" + str(round(total_rev, 2)))
    print("=" * 60)


def export_mall_report_csv(mname):
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = REPORTS_DIR + "/mall_" + mname.replace(" ", "_") + "_" + ts + ".csv"

    s = get_mall_stats(mname)
    done = get_completed_records(mname)
    payments = get_mall_payments(mname)

    f = open(fname, "w", newline="")
    w = csv.writer(f)

    w.writerow(["KZN Smart Mall Parking System"])
    w.writerow([mall_data[mname]["full_name"]])
    w.writerow(["Exported: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    w.writerow([])
    w.writerow(["Summary"])
    w.writerow(["Vehicles served", s["served"]])
    w.writerow(["Total revenue (R)", s["revenue"]])
    w.writerow(["Average duration (min)", s["avg_mins"]])
    w.writerow(["Currently parked", s["active"]])
    w.writerow([])
    w.writerow(["Parking Records"])
    w.writerow(["Customer", "Entry", "Exit", "Duration (min)", "Fee (R)", "Rate Type"])
    for r in done:
        w.writerow([r["username"], r["entry_time"], r["exit_time"], r["mins_parked"], r["fee"], r["fee_type"]])

    w.writerow([])
    w.writerow(["Payment Records"])
    w.writerow(["Customer", "Amount (R)", "Rate Type", "Date", "Paid At"])
    for p in payments:
        w.writerow([p["username"], p["amount"], p["rate_type"], p["date"], p["paid_at"]])

    f.close()
    print("")
    print("Report saved: " + fname)
    return fname


def export_cross_mall_report_csv():
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = REPORTS_DIR + "/all_malls_" + ts + ".csv"

    f = open(fname, "w", newline="")
    w = csv.writer(f)

    w.writerow(["KZN Smart Mall Parking System - All Malls"])
    w.writerow(["Exported: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    w.writerow([])
    w.writerow(["Mall", "Pricing", "Capacity", "Active", "Served", "Revenue (R)", "Avg Stay (min)"])

    total_rev = 0
    total_served = 0

    for mname in MALL_NAMES:
        s = get_mall_stats(mname)
        total_rev = total_rev + s["revenue"]
        total_served = total_served + s["served"]
        w.writerow([s["name"], s["pricing"].replace("_", " ").title(), s["cap"], s["active"], s["served"], s["revenue"], s["avg_mins"]])

    w.writerow([])
    w.writerow(["TOTAL", "", "", "", total_served, round(total_rev, 2), ""])

    f.close()
    print("")
    print("Cross-mall report saved: " + fname)
    return fname
