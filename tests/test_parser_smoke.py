import os
from datetime import datetime
from src.hardy_calendar.parser import parse_weekly_plan_page

POST_URL = "https://www.hardywyzszaforma.pl/plan"

# PARSER ALWAYS RETURNS CURRENT YEAR BECAUSE HARDY DOESN'T PROVIDE YEAR IN PLAN HEADERS
# I HAD TO APPROXIMATE IT SOMEHOW :/
current_year = datetime.now().year

def test_parse_one_day():
    # Load the HTML file
    with open(os.path.join(os.path.dirname(__file__), "./plan.html"), encoding="utf-8") as f:
        html = f.read()

    # Parse the plan
    plans = parse_weekly_plan_page(POST_URL, html)

    # Find the first date (adjust as needed)
    day = datetime(current_year, 6, 30)  # 30.06

    expected = """
⇒ Speed
Ćwiczenia: cal SKI/bike ERG, burpee box step, forearm plank, swing + push press
Metoda treningowa: 2 x 12 min EMOM
Czas pracy w części głównej: 25 min

⇒ Athletic
Ćwiczenia: DEADLIFT, side jacknife, OHP, seated band row
Metoda treningowa: 4 rundy, co 2,5 min wykonaj parę ćwiczeń
Czas pracy w części głównej: 21 min

⇒ FBB
Ćwiczenia: DB's butterfly, powerband triceps extension, b-stance BB RDL, push up plank leg abduction
Metoda treningowa: 4 rundy, co 2,5 min wykonaj parę ćwiczeń
Czas pracy w części głównej: 21 min

Source: https://www.hardywyzszaforma.pl/plan
Got questions? Ideas? Come here: https://github.com/cajivah/hardy-calendar/issues
""".strip()
    
    assert day in plans
    assert plans[day] == expected


def test_parse_another_day():
    # Load the HTML file
    with open(os.path.join(os.path.dirname(__file__), "./plan.html"), encoding="utf-8") as f:
        html = f.read()

    # Parse the plan
    plans = parse_weekly_plan_page(POST_URL, html)

    # Find the first date (adjust as needed)
    day = datetime(current_year, 7, 1)  # 01.07
    
    expected = """
⇒ Speed
Ćwiczenia: AAB/bike ERG, slow rotational climbers, DU/SU (skakanka), TRX row, push upl plank drag in, wall ball
Metoda treningowa: 2 x 8 min EMOM + 2 min MAX
Czas pracy w części głównej: 21 min

⇒ Speed Beginners
Ćwiczenia: AAB/bike ERG, slow rotational climbers, DU/SU (skakanka), TRX row, push upl plank drag in, wall ball
Metoda treningowa: 2 x 8 min EMOM + 2 min MAX
Czas pracy w części głównej: 21 min

⇒ Athletic
Ćwiczenia: chin up, goblet squat, tuck up
Metoda treningowa: 20 min WORK
Czas pracy w części głównej: 20 min

⇒ Athletic Beginners
Ćwiczenia: ring row, squat, tuck up
Metoda treningowa: 16 min WORK
Czas pracy w części głównej: 16 min

⇒ FBB
Ćwiczenia: heavy ring row, hammer curl + drop set, DB single leg hip thrust, spanish squat
Metoda treningowa: 4 rundy, co 2,5 min wykonaj parę ćwiczeń
Czas pracy w części głównej: 21 min

Source: https://www.hardywyzszaforma.pl/plan
Got questions? Ideas? Come here: https://github.com/cajivah/hardy-calendar/issues
""".strip()
    assert day in plans
    assert plans[day] == expected

def test_parse_last_day():
    # Load the HTML file
    with open(os.path.join(os.path.dirname(__file__), "./plan.html"), encoding="utf-8") as f:
        html = f.read()

    # Parse the plan
    plans = parse_weekly_plan_page(POST_URL, html)

    # Find the first date (adjust as needed)
    day = datetime(current_year, 7, 6)  # 06.07
    
    expected = """
⇒ Fast&strong
Ćwiczenia: burpee, DB's push press, bridge walkout, alt. Db snatch, forearm plank
Metoda treningowa: 12 i 8 min EMOM
Czas pracy w części głównej: 20 min

Source: https://www.hardywyzszaforma.pl/plan
Got questions? Ideas? Come here: https://github.com/cajivah/hardy-calendar/issues
""".strip()
    assert day in plans
    print(plans[day])
    assert plans[day] == expected