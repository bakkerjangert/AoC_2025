import functools
from functools import cache
from functools import lru_cache
import itertools
from collections import Counter


def minimum_pushes(string, buttons):
    lights = [i for i in range(len(string)) if string[i] == '#']
    pushes, solved = 1, False
    while not solved:
        # No need for multiple pushes of a button; pushing button twice reverts a step back
        combinations = itertools.combinations(buttons, pushes)
        for c in combinations:
            numbers = sum(c, ())
            counts = Counter(numbers)
            current_lights = sorted([num for num, cnt in counts.items() if cnt % 2 == 1])
            if lights == current_lights:
                solved = True
                # print(f'Solved in {pushes} pushes!')
                return pushes
        pushes += 1
    return None

def minimum_pushes_pt2(jolts, buttons, current_jolts=None):
    if current_jolts is None:
        current_jolts = [0,] * len(jolts)
    if not buttons:
        return None

def solve_min_presses(buttons, target, current=None, idx=0, presses_record=None):
    if current is None:
        current = [0] * len(target)
    if presses_record is None:
        presses_record = [0] * len(buttons)

    # Basisgeval: alle knoppen geprobeerd
    if idx >= len(buttons):
        return presses_record if current == target else None

    button = buttons[idx]

    # Bereken hoeveel drukken nodig zijn om minstens één target waarde te halen
    diffs = [target[i] - current[i] for i in button]
    # alleen positieve verschillen zijn relevant
    possible_presses = [d for d in diffs if d > 0]
    if not possible_presses:
        max_presses = 0
    else:
        max_presses = min(possible_presses)

    # Probeer van max_presses naar 0 (dus eerst veel drukken, dan minder)
    for presses in range(max_presses, -1, -1):
        new_current = current[:]
        new_record = presses_record[:]
        for _ in range(presses):
            for i in button:
                new_current[i] += 1
        new_record[idx] += presses

        # overschrijding check
        if any(new_current[i] > target[i] for i in button):
            continue

        result = solve_min_presses(buttons, target, new_current, idx + 1, new_record)
        if result is not None:
            # print(f'Found solution: {result}')
            return result

    return None

def solve_min_presses_cached(buttons, target):
    """
    Vind de minimale drukcombinatie om target te bereiken.
    buttons: lijst van knoppen, elke knop is een lijst met indices die hij beïnvloedt
    target: lijst van gewenste eindwaarden
    """

    @cache
    def recurse(idx, current_tuple):
        current = list(current_tuple)

        # Basisgeval: alle knoppen geprobeerd
        if idx >= len(buttons):
            return [] if current == target else None

        button = buttons[idx]

        # Bereken hoeveel drukken nodig zijn om minstens één target waarde te halen
        diffs = [target[i] - current[i] for i in button]
        possible_presses = [d for d in diffs if d > 0]
        max_presses = min(possible_presses) if possible_presses else 0

        # Probeer van max_presses naar 0 (aftellend)
        for presses in range(max_presses, -1, -1):
            new_current = current[:]
            for _ in range(presses):
                for i in button:
                    new_current[i] += 1

            # overschrijding check
            if any(new_current[i] > target[i] for i in button):
                continue

            result = recurse(idx + 1, tuple(new_current))
            if result is not None:
                return [presses] + result

        return None

    # Start de zoektocht
    return recurse(0, tuple([0] * len(target)))

def solve_min_presses_opt1(buttons, target):
    n = len(target)

    @cache
    def recurse(idx, current_tuple):
        current = list(current_tuple)

        # Basisgeval
        if idx >= len(buttons):
            return [] if current == target else None

        # Pruning: overschrijding
        if any(c > t for c, t in zip(current, target)):
            return None

        button = buttons[idx]
        diffs = [target[i] - current[i] for i in button]
        possible_presses = [d for d in diffs if d > 0]
        max_presses = min(possible_presses) if possible_presses else 0

        # Probeer aftellend
        for presses in range(max_presses, -1, -1):
            new_current = current[:]
            for i in button:
                new_current[i] += presses

            # Pruning: overschrijding
            if any(new_current[i] > target[i] for i in button):
                continue

            result = recurse(idx + 1, tuple(new_current))
            if result is not None:
                return [presses] + result

        return None

    return recurse(0, tuple([0] * n))


def solve_min_presses_gemini(buttons, target):
    """
    Vindt het minimum aantal indrukken om de 'target' staat te bereiken.

    :param buttons: Lijst van lijsten, waarbij elke binnenste lijst de indices
                    bevat die door de betreffende knop worden verhoogd.
    :param target: De gewenste eindtoestand van de tellers.
    :return: Het minimum totale aantal indrukken, of None als het onmogelijk is.
    """
    n = len(target)
    # Gebruik een zeer grote waarde om een 'oneindige' kosten aan te geven
    INF = float('inf')

    # De staat is (index van de knop, huidige toestand van de tellers)
    # De waarde is het MINIMUM AANTAL OVERIGE indrukken dat nodig is om het doel te bereiken.
    @lru_cache(maxsize=None)
    def recurse(idx, current_tuple):
        # 1. Basisgeval: Alle knoppen zijn verwerkt
        if idx == len(buttons):
            return 0 if list(current_tuple) == target else INF

        current = list(current_tuple)
        button = buttons[idx]
        min_total_presses = INF

        # Bepaal de maximale indrukken voor deze knop (buttons[idx])
        # Het aantal indrukken kan nooit hoger zijn dan de kleinste resterende
        # verschil (target[i] - current[i]) voor alle indices die door deze knop worden beïnvloed.
        max_presses = INF
        for i in button:
            # Als een teller al boven de target is, is dit pad onmogelijk (zou gepruned moeten zijn)
            # Maar dit dient als een extra beveiliging/pruning.
            if current[i] > target[i]:
                return INF

            # Bereken de resterende ruimte voor deze specifieke index
            remaining = target[i] - current[i]
            if remaining < max_presses:
                max_presses = remaining

        # Als max_presses INF is (wat alleen gebeurt als button leeg is), zet het op 0.
        if max_presses == INF:
            max_presses = 0

        # 2. Transitie: Probeer alle mogelijke aantallen indrukken (presses) voor buttons[idx]
        # We proberen aftellend (greedy) omdat we vaak de maximale indrukken nodig hebben,
        # maar voor de correctheid MOETEN we van 0 tot max_presses gaan.
        # De optimale strategie is niet per se greedy!
        for presses in range(max_presses + 1):
            new_current = current[:]

            # Pas de indrukken toe
            for i in button:
                new_current[i] += presses

            # Recursieve oproep: kosten van deze stap + kosten van de volgende stappen
            # Let op: de pruning van 'overschrijding' is nu ingebouwd in de max_presses berekening.
            # We hoeven alleen de nieuwe toestand als tuple door te geven.
            remaining_presses = recurse(idx + 1, tuple(new_current))

            if remaining_presses != INF:
                # Totale kosten = indrukken van deze knop + min. resterende indrukken
                total_presses = presses + remaining_presses
                min_total_presses = min(min_total_presses, total_presses)

        return min_total_presses

    # Start de recursie
    result = recurse(0, tuple([0] * n))

    # Retourneer het resultaat, of None als het INF is
    return result if result != INF else None


import pulp
def solve_min_presses_ilp(buttons, target):
    """
    Lost het probleem op als een Integer Linear Programming (ILP) probleem
    met behulp van de PuLP-bibliotheek. Dit is veel sneller voor kleine
    aantallen knoppen (variabelen).

    :param buttons: Lijst van lijsten (indices die worden beïnvloed).
    :param target: De gewenste eindtoestand van de tellers (constraints).
    :return: Het minimum totale aantal indrukken, of None als onmogelijk.
    """
    N = len(target)  # Aantal tellers (rijen in A)
    M = len(buttons)  # Aantal knoppen (kolommen in A)

    # 1. Maak het LP-probleem aan
    prob = pulp.LpProblem("Minimale Knoop Indrukken", pulp.LpMinimize)

    # 2. Definieer de beslissingsvariabelen (x_m: aantal indrukken per knop)
    # De indrukken moeten gehele getallen zijn (Integer) en niet-negatief (lowBound=0).
    press_vars = [
        pulp.LpVariable(f"x_{m}", lowBound=0, cat='Integer')
        for m in range(M)
    ]

    # 3. Definieer de doelstellingsfunctie (Objective Function)
    # Min sum(x_m)
    prob += pulp.lpSum(press_vars), "Totaal aantal indrukken"

    # 4. Definieer de beperkingen (Constraints)
    # De som van de bijdragen per teller moet gelijk zijn aan de target
    for n in range(N):
        # Bereken de bijdrage van elke knop m aan teller n
        contribution = []
        for m in range(M):
            # Knop m beïnvloedt teller n als index n in buttons[m] zit
            if n in buttons[m]:
                # Coëfficiënt A[n, m] is 1
                contribution.append(press_vars[m])
            # anders is de coëfficiënt 0 (geen bijdrage)

        # De som van de bijdragen moet gelijk zijn aan de target T_n
        prob += pulp.lpSum(contribution) == target[n], f"Constraint_Teller_{n}"

    # 5. Los het probleem op
    # PuLP gebruikt standaard de meegeleverde CBC-oplosser, of een lokaal geïnstalleerde.
    solver = pulp.PULP_CBC_CMD(msg=False)
    prob.solve(solver)
    # prob.solve()

    # 6. Analyseer de resultaten
    if prob.status == pulp.LpStatusOptimal:
        # Optimale oplossing gevonden
        min_presses = pulp.value(prob.objective)
        DePressesPerButton = [int(pulp.value(v)) for v in press_vars] # Optioneel: de daadwerkelijke indrukken
        return int(min_presses), DePressesPerButton

    elif prob.status == pulp.LpStatusInfeasible:
        # Geen oplossing mogelijk (bijv. target [1, 0] met knop [[0]])
        return None

    else:
        # Ander probleem (bijv. onbegrensd, of fout)
        return None

file = 'input.txt'
# file = 'test.txt'
with open(file, encoding="utf8") as f:
    data = f.read().splitlines()

total_pushes_pt1, total_pushes_pt2 = 0, 0
for i, r in enumerate(data):
    lights = r.split('[')[1].split(']')[0]
    jolts = list(map(int, r.split('{')[1].split('}')[0].split(',')))
    buttons = r.split('] ')[1].split(' {')[0]
    buttons = buttons.replace(' ', ', ')
    buttons = buttons.replace(')', ',)')
    buttons = eval(f'({buttons})')
    total_pushes_pt1 += minimum_pushes(lights, buttons)
    buttons = sorted(list(buttons), key=len, reverse=True)
    # print(buttons)
    number_of_pushes, buton_pushes = solve_min_presses_ilp(buttons, jolts)
    print(f'Solution = {buton_pushes} in {number_of_pushes} presses!')
    total_pushes_pt2 += number_of_pushes
    print(f'Solved line {i + 1} from {len(data)}!')
print(f'Part 1: {total_pushes_pt1}')
print(f'Part 2: {total_pushes_pt2}')