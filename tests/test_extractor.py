import os
from datetime import datetime
from src.hardy_calendar.extractor import _parse_plan

def test_parse_one_day():
    # Load the HTML file
    with open(os.path.join(os.path.dirname(__file__), "./plan.html"), encoding="utf-8") as f:
        html = f.read()

    # Parse the plan
    plans = _parse_plan(html)

    # Find the first date (adjust as needed)
    day = datetime(2025, 6, 30)  # 30.06

    expected = """
⇒ Speed
Ćwiczenia: cal SKI/bike ERG, burpee box step, forearm plank, swing + push press
Metoda treningowa: 2 x 12 min EMOM
Czas pracy w części głównej: 25 min

⇒ Athletic
Ćwiczenia: DEADLIFT, side jacknife, OHP, seated band row
Metoda treningowa: 4 rundy, co 2,5 min wykonaj parę ćwiczeń
Czas pracy w części głównej: 21 min
INFO:

⇒ FBB
Ćwiczenia: DB's butterfly, powerband triceps extension, b-stance BB RDL, push up plank leg abduction
Metoda treningowa: 4 rundy, co 2,5 min wykonaj parę ćwiczeń
Czas pracy w części głównej: 21 min
""".strip()
    
    assert day in plans
    assert plans[day] == expected


def test_parse_another_day():
    # Load the HTML file
    with open(os.path.join(os.path.dirname(__file__), "./plan.html"), encoding="utf-8") as f:
        html = f.read()

    # Parse the plan
    plans = _parse_plan(html)

    # Find the first date (adjust as needed)
    day = datetime(2025, 7, 1)  # 01.07
    
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
""".strip()
    assert day in plans
    assert plans[day] == expected
