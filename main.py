from users import login, register_user
from mall import mall_data, MALL_NAMES, get_pricing_description
from parking import enter_parking, exit_parking, get_user_parking_history, get_active_sessions, get_current_occupancy
from payments import make_payment, get_user_payments
from reports import print_mall_report, print_cross_mall_report, export_mall_report_csv, export_cross_mall_report_csv


def pick_mall():
    print("")
    print("Which mall?")
    print("")
    i = 1
    for nm in MALL_NAMES:
        m = mall_data[nm]
        free = m["capacity"] - get_current_occupancy(nm)
        print(str(i) + ". " + m["full_name"])
        print("   Rate   : " + get_pricing_description(nm))
        print("   Free   : " + str(free) + "/" + str(m["capacity"]) + " spaces")
        print("")
        i = i + 1
    print(str(i) + ". Back")
    print("")

    while True:
        raw = input("Choice: ").strip()
        try:
            pick = int(raw)
        except:
            print("Enter a number please.")
            continue

        if pick == i:
            return None
        if pick >= 1 and pick <= len(MALL_NAMES):
            return MALL_NAMES[pick - 1]

        print("Not a valid option.")


# --------------------------------------------------
# what a logged-in customer can do
# --------------------------------------------------
def show_customer_options(usr):
    while True:
        print("")
        print("------------------------------------------")
        print("Hi " + usr["username"] + "! What would you like to do?")
        print("------------------------------------------")
        print("1. Park my vehicle")
        print("2. Exit parking + pay")
        print("3. My parking history")
        print("4. My payment history")
        print("5. Logout")
        print("")

        opt = input("Option: ").strip()

        if opt == "1":
            chosen = pick_mall()
            if chosen != None:
                enter_parking(usr, chosen)
            input("\nEnter to continue...")

        elif opt == "2":
            chosen = pick_mall()
            if chosen != None:
                amt, rtype = exit_parking(usr, chosen)
                if amt > 0:
                    make_payment(usr, chosen, amt, rtype)
            input("\nEnter to continue...")

        elif opt == "3":
            hist = get_user_parking_history(usr["username"])
            print("")
            print("Your parking history:")
            if len(hist) == 0:
                print("Nothing yet.")
            else:
                n = 1
                for rec in hist:
                    print("")
                    print(str(n) + ". " + rec["mall"])
                    print("   In  : " + rec["entry_time"])
                    print("   Out : " + rec["exit_time"])
                    print("   Time: " + str(rec["mins_parked"]) + " min")
                    print("   Fee : R" + str(rec["fee"]))
                    n = n + 1
            input("\nEnter to continue...")

        elif opt == "4":
            pays = get_user_payments(usr["username"])
            print("")
            print("Your payment history:")
            if len(pays) == 0:
                print("No payments on record.")
            else:
                running = 0
                n = 1
                for p in pays:
                    print("")
                    print(str(n) + ". " + p["mall"] + " - R" + str(p["amount"]) + " (" + p["date"] + ")")
                    running = running + p["amount"]
                    n = n + 1
                print("")
                print("Total: R" + str(round(running, 2)))
            input("\nEnter to continue...")

        elif opt == "5":
            print("Logged out.")
            break

        else:
            print("Try again, that wasnt an option.")


# --------------------------------------------------
# admin sees their own mall only
# --------------------------------------------------
def show_admin_options(usr):
    mname = usr["mall"]

    if mname == None or mname not in mall_data:
        print("This admin account doesnt have a mall assigned. Contact the owner.")
        return

    m = mall_data[mname]

    while True:
        occ = get_current_occupancy(mname)
        rem = m["capacity"] - occ

        print("")
        print("------------------------------------------")
        print("Admin Panel - " + m["full_name"])
        print("Currently: " + str(occ) + " parked, " + str(rem) + " free")
        print("------------------------------------------")
        print("1. See whos parked right now")
        print("2. Capacity overview")
        print("3. Mall report")
        print("4. Export report to CSV")
        print("5. Logout")
        print("")

        opt = input("Option: ").strip()

        if opt == "1":
            now_parked = get_active_sessions(mname)
            print("")
            print("Currently at " + mname + ":")
            if len(now_parked) == 0:
                print("Nobody parked right now.")
            else:
                n = 1
                for r in now_parked:
                    print(str(n) + ". " + r["username"] + "  (in at " + r["entry_time"] + ")")
                    n = n + 1
            input("\nEnter to continue...")

        elif opt == "2":
            print("")
            print(mname + " capacity:")
            print("Total  : " + str(m["capacity"]))
            print("Used   : " + str(occ))
            print("Free   : " + str(rem))
            filled = int((occ / m["capacity"]) * 20)
            bar = "[" + "#" * filled + "-" * (20 - filled) + "]"
            pct = int((occ / m["capacity"]) * 100)
            print("Usage  : " + bar + " " + str(pct) + "%")
            input("\nEnter to continue...")

        elif opt == "3":
            print_mall_report(mname)
            input("\nEnter to continue...")

        elif opt == "4":
            export_mall_report_csv(mname)
            input("\nEnter to continue...")

        elif opt == "5":
            print("Logged out.")
            break

        else:
            print("Invalid option, try again.")


# --------------------------------------------------
# owner/shareholder sees everything
# --------------------------------------------------
def show_owner_options(usr):
    while True:
        print("")
        print("------------------------------------------")
        print("Owner Dashboard - " + usr["username"])
        print("------------------------------------------")
        print("1. Report: single mall")
        print("2. Report: all malls compared")
        print("3. Export: single mall CSV")
        print("4. Export: all malls CSV")
        print("5. Live capacity - all malls")
        print("6. Logout")
        print("")

        opt = input("Option: ").strip()

        if opt == "1":
            chosen = pick_mall()
            if chosen != None:
                print_mall_report(chosen)
            input("\nEnter to continue...")

        elif opt == "2":
            print_cross_mall_report()
            input("\nEnter to continue...")

        elif opt == "3":
            chosen = pick_mall()
            if chosen != None:
                export_mall_report_csv(chosen)
            input("\nEnter to continue...")

        elif opt == "4":
            export_cross_mall_report_csv()
            input("\nEnter to continue...")

        elif opt == "5":
            print("")
            print("Live capacity:")
            for nm in MALL_NAMES:
                md = mall_data[nm]
                occ = get_current_occupancy(nm)
                free = md["capacity"] - occ
                filled = int((occ / md["capacity"]) * 20)
                bar = "[" + "#" * filled + "-" * (20 - filled) + "]"
                pct = int((occ / md["capacity"]) * 100)
                print("")
                print(md["full_name"])
                print(bar + " " + str(occ) + "/" + str(md["capacity"]) + " (" + str(free) + " free, " + str(pct) + "% full)")
            input("\nEnter to continue...")

        elif opt == "6":
            print("Logged out.")
            break

        else:
            print("Not a valid option.")


# --------------------------------------------------
# startup
# --------------------------------------------------
def main():
    print("")
    print("==========================================")
    print("  KZN Smart Mall Parking System")
    print("  Gateway | Pavilion | La Lucia")
    print("==========================================")
    print("")

    while True:
        print("1. Login")
        print("2. Register")
        print("3. Quit")
        print("")

        ch = input("Choose: ").strip()

        if ch == "1":
            usr = login()
            if usr != None:
                r = usr["role"]
                if r == "customer":
                    show_customer_options(usr)
                elif r == "admin":
                    show_admin_options(usr)
                elif r == "owner":
                    show_owner_options(usr)
                else:
                    print("Unknown role, contact the owner.")

        elif ch == "2":
            register_user()

        elif ch == "3":
            print("Goodbye!")
            break

        else:
            print("Please choose 1, 2 or 3.")
            print("")


if __name__ == "__main__":
    main()
