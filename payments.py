from datetime import datetime
from storage import load_json, save_json

PAY_FILE = "data/payments.json"


def load_payments():
    return load_json(PAY_FILE, [])


def save_payments(data):
    save_json(PAY_FILE, data)


def make_payment(user, mname, amount, rate_type=""):
    print("")
    print("=== Payment ===")
    print("Mall    : " + mname)
    print("Amount  : R" + str(amount))
    print("Rate    : " + rate_type)
    print("")

    ans = input("Proceed with payment? (yes/no): ").strip().lower()
    if ans != "yes" and ans != "y":
        print("Payment not made. Please pay before leaving the mall.")
        return False

    all_payments = load_payments()
    now = datetime.now()

    rec = {
        "username": user["username"],
        "mall": mname,
        "amount": amount,
        "rate_type": rate_type,
        "date": now.strftime("%Y-%m-%d"),
        "paid_at": now.isoformat()
    }

    all_payments.append(rec)
    save_payments(all_payments)

    print("Payment of R" + str(amount) + " successful. Safe travels!")
    return True


def get_user_payments(uname):
    all_payments = load_payments()
    mine = []
    for p in all_payments:
        if p["username"] == uname:
            mine.append(p)
    return mine


def get_mall_payments(mname=None):
    all_payments = load_payments()
    if mname == None:
        return all_payments
    filtered = []
    for p in all_payments:
        if p["mall"] == mname:
            filtered.append(p)
    return filtered
