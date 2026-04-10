from storage import load_json, save_json

USERS_FILE = "data/users.json"

# seeded staff accounts so the system isnt empty on first run
# passwords are basic for now, would hash them in a real system
staff_accounts = [
    {"username": "admin_gateway",  "password": "admin123", "role": "admin", "mall": "Gateway"},
    {"username": "admin_pavilion", "password": "admin123", "role": "admin", "mall": "Pavilion"},
    {"username": "admin_lalucia",  "password": "admin123", "role": "admin", "mall": "La Lucia"},
    {"username": "owner",          "password": "owner123",  "role": "owner", "mall": None},
]


def load_users():
    all_users = load_json(USERS_FILE, [])

    # collect existing usernames to avoid duplicates
    taken = []
    for u in all_users:
        taken.append(u["username"])

    # add any missing staff accounts
    changed = False
    for acc in staff_accounts:
        if acc["username"] not in taken:
            all_users.append(acc)
            changed = True

    if changed:
        save_users(all_users)

    return all_users


def save_users(users):
    save_json(USERS_FILE, users)


def register_user():
    all_users = load_users()

    print("")
    print("=== Create New Account ===")

    uname = input("Choose a username: ").strip()

    if uname == "" or uname.lower() == "back":
        return None

    # check if taken
    for u in all_users:
        if u["username"] == uname:
            print("That username is already taken, try something else.")
            return None

    pw = input("Choose a password: ").strip()
    if pw == "":
        print("Password cant be empty.")
        return None

    pw2 = input("Re-enter password: ").strip()
    if pw != pw2:
        print("Passwords didnt match.")
        return None

    new_acc = {
        "username": uname,
        "password": pw,
        "role": "customer",
        "mall": None
    }

    all_users.append(new_acc)
    save_users(all_users)
    print("Account created! You can now log in, " + uname + ".")
    return new_acc


def login():
    all_users = load_users()

    print("")
    print("=== Login ===")
    uname = input("Username: ").strip()
    pw = input("Password: ").strip()

    for u in all_users:
        if u["username"] == uname and u["password"] == pw:
            print("Logged in as " + uname + " (" + u["role"] + ")")
            return u

    print("Wrong username or password.")
    return None
