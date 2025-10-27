class F1TippCalculator:
    def __init__(self):
        # Punktesystem
        self.race_points = {1: 8, 2: 7, 3: 6, 4: 5, 5: 4, 6: 3, 7: 2, 8: 1}
        self.quali_points = {1: 4, 2: 3, 3: 2, 4: 1}
        self.wm_bonus = 20
        self.consolation_point = 1

    def max_points_per_race(self):
        """Berechnet maximale Punkte pro Rennen (Quali + Rennen)"""
        max_quali = sum(self.quali_points.values())
        max_race = sum(self.race_points.values())
        return max_quali + max_race

    """
                  Berechnet Punkte für ein einzelnes Rennen/Quali

                  tips: Liste der getippten Fahrer in Reihenfolge [P1, P2, P3, ...]
                  actual_result: Liste der tatsächlichen Fahrer in Reihenfolge [P1, P2, P3, ...]
                  is_quali: True für Qualifying (Top 4), False für Rennen (Top 8)

                  Returns: Anzahl der Punkte
                  """
    def calculate_race_points(self, tips, actual_result, is_quali=False):
        points = 0
        points_system = self.quali_points if is_quali else self.race_points
        top_positions = 4 if is_quali else 8

        # Prüfe nur die relevanten Positionen
        tips = tips[:top_positions]
        actual_top = actual_result[:top_positions]

        for pos, tipped_driver in enumerate(tips, start=1):
            # Prüfe ob Fahrer auf richtiger Position
            if pos <= len(actual_result) and actual_result[pos - 1] == tipped_driver:
                # Richtige Position!
                points += points_system[pos]
            # Prüfe ob Fahrer in Top X ist (aber falsche Position)
            elif tipped_driver in actual_top:
                # Fahrer ist in Top X, aber falsche Position
                points += self.consolation_point

        return points

    """
    Analysiert den Championship-Status

    participants: Liste von Dicts mit 'name', 'points', 'driver_wm_tip', 'team_wm_tip'
    races_
    """
    def calculate_championship_status(self, participants, races_remaining):
        max_points_remaining = races_remaining * self.max_points_per_race()
        max_points_with_wm = max_points_remaining + (2*self.wm_bonus)

        sorted_participants = sorted(participants, key=lambda x: x['points'], reverse=True)
        leader = sorted_participants[0]

        print("=" * 70)
        print("🏁 FORMEL 1 KICKTIPP - CHAMPIONSHIP STATUS 🏁")
        print("=" * 70)
        print(f"\n📋 PUNKTESYSTEM:")
        print(f"   Qualifying (Top 4):")
        print(f"      • Richtige Position: P1=4, P2=3, P3=2, P4=1 Punkte")
        print(f"      • Fahrer in Top 4, aber falsche Position: {self.consolation_point} Punkt")
        print(f"   Rennen (Top 8):")
        print(f"      • Richtige Position: P1=8, P2=7, P3=6, P4=5, P5=4, P6=3, P7=2, P8=1")
        print(f"      • Fahrer in Top 8, aber falsche Position: {self.consolation_point} Punkt")
        print(f"   WM-Tipps: Je {self.wm_bonus} Punkte für richtigen Fahrer- und Team-Weltmeister")
        print(f"\n📊 Verbleibende Rennen: {races_remaining}")
        print(f"💯 Maximale Punkte pro Rennen: {self.max_points_per_race()} (Quali: 10 + Rennen: 36)")
        print(f"🏆 WM-Bonus verfügbar: {2 * self.wm_bonus} Punkte (2x {self.wm_bonus})")
        print(f"📈 Maximale Punkte noch zu vergeben: {max_points_with_wm}")

        print("\n" + "-" * 70)
        print("AKTUELLER STAND:")
        print("-" * 70)

        for i, p in enumerate(sorted_participants, 1):
            print(f"{i}. {p['name']}: {p['points']} Punkte")
            print(f"   └─ Fahrer-WM-Tipp: {p['driver_wm_tip']}")
            print(f"   └─ Team-WM-Tipp: {p['team_wm_tip']}")

        print("\n" + "=" * 70)
        print("CHAMPIONSHIP ANALYSE:")
        print("=" * 70)

        # Prüfe für jeden Teilnehmer
        for participant in enumerate(sorted_participants):
            print(f"\n🔍 {participant['name']}:")

            if i == 0:
                # Leader
                margin = participant['points'] -  sorted_participants[1]['points']
                max_others_can_score = max_points_with_wm

                print(f"   Vorsprung: {margin} Punkte")
                print(f"   Verfolger können maximal holen: {max_others_can_score} Punkte")

                if margin > max_others_can_score:
                    print(f"   ✅ CHAMPION! Uneinholbar vorne!")
                else:
                    points_needed_to_secure = max_others_can_score - margin + 1
                    print(f"   ⚠️  Noch nicht sicher!")
                    print(f"   💪 Benötigt noch {points_needed_to_secure} Punkte um sicher zu sein")

            else:
                # Verfolger
                gap = leader['points'] - participant['points']
                max_can_score = max_points_with_wm
                max_leader_can_score = max_points_with_wm

                print(f"   Rückstand auf {leader['name']}: {gap} Punkte")
                print(f"   Maximal noch zu holen: {max_can_score} Punkte")

                if gap > max_can_score:
                    print(f"   ❌ Mathematisch ausgeschieden")
                else:
                    # Berechne benötigte Punkte (worst case: Leader holt auch alles)
                    min_points_to_win = gap + 1
                    print(f"   ✅ Noch im Rennen!")
                    print(f"   💪 Mindestens {min_points_to_win} Punkte zum Überholen nötig")
                    print(f"   📌 Realistisch: Wenn Leader 0 Punkte macht, reichen {min_points_to_win} Punkte")
                    print(f"   📌 Worst Case: Wenn Leader alles holt, unmöglich einzuholen")

        print("\n" + "=" * 70)
        print("WM-TIPP BONUS ANALYSE:")
        print("=" * 70)

        team_tips_count = {}
        for p in sorted_participants:
            team = p['team_wm_tip']
            if team not in team_tips_count:
                team_tips_count[team] = []
            team_tips_count[team].append(p['name'])

        print(f"🏆 Team-WM Tipps:")
        for team, players in team_tips_count.items():
            print(f"   {team}: {', '.join(players)} ({len(players)} Spieler)")

        # Analysiere Fahrer-WM Tipps
        driver_tips_count = {}
        for p in sorted_participants:
            driver = p['driver_wm_tip']
            if driver not in driver_tips_count:
                driver_tips_count[driver] = []
            driver_tips_count[driver].append(p['name'])

        print(f"\n🏁 Fahrer-WM Tipps:")
        for driver, players in driver_tips_count.items():
            print(f"   {driver}: {', '.join(players)} ({len(players)} Spieler)")

        # WM-Bonus Szenarien
        print("\n" + "=" * 70)
        print("🎯 WM-BONUS SZENARIEN:")
        print("=" * 70)

        for i, p in enumerate(sorted_participants):
            print(f"\n{'🥇' if i == 0 else '📍'} {p['name']} (aktuell {p['points']} Punkte):")

            # Best Case: Alle Rennen perfekt + beide WM-Tipps richtig
            best_case = p['points'] + max_points_remaining + 40
            print(f"   ✅ Best Case: {best_case} Punkte")
            print(f"      → Alle verbleibenden Rennen perfekt ({max_points_remaining} Pkt)")
            print(f"      → Fahrer-WM richtig ({self.wm_bonus} Pkt)")
            print(f"      → Team-WM richtig ({self.wm_bonus} Pkt)")

            # Realistic Case: Rennen perfekt, aber nur Team-WM richtig (weil gleicher Tipp)
            team_shared = len(team_tips_count[p['team_wm_tip']]) > 1
            if team_shared:
                realistic_case = p['points'] + max_points_remaining + 20
                print(f"   ⚠️  Realistischer Fall: {realistic_case} Punkte")
                print(f"      → Alle Rennen perfekt ({max_points_remaining} Pkt)")
                print(
                    f"      → Team-WM richtig ({self.wm_bonus} Pkt) - aber {len(team_tips_count[p['team_wm_tip']])} Spieler haben gleich getippt!")
                print(f"      → Fahrer-WM falsch (0 Pkt)")

            # Worst Case: Keine Punkte mehr
            worst_case = p['points']
            print(f"   ❌ Worst Case: {worst_case} Punkte")
            print(f"      → Alle verbleibenden Rennen: 0 Punkte")
            print(f"      → Beide WM-Tipps falsch: 0 Punkte")

            # Zeige WM-Bonus Vorteil/Nachteil
            print(f"   📊 WM-Bonus Analyse:")
            driver_competitors = len(driver_tips_count[p['driver_wm_tip']]) - 1
            team_competitors = len(team_tips_count[p['team_wm_tip']]) - 1

            if driver_competitors > 0:
                print(
                    f"      ⚠️  Fahrer-WM ({p['driver_wm_tip']}): {driver_competitors} weitere Spieler haben gleich getippt")
                print(f"         → Kein Vorteil wenn richtig!")
            else:
                print(f"      ✅ Fahrer-WM ({p['driver_wm_tip']}): Alleiniger Tipp")
                print(f"         → {self.wm_bonus} Punkte Vorteil wenn richtig!")

            if team_competitors > 0:
                print(
                    f"      ⚠️  Team-WM ({p['team_wm_tip']}): {team_competitors} weitere Spieler haben gleich getippt")
                print(f"         → Kein Vorteil wenn richtig!")
            else:
                print(f"      ✅ Team-WM ({p['team_wm_tip']}): Alleiniger Tipp")
                print(f"         → {self.wm_bonus} Punkte Vorteil wenn richtig!")

        return {
            'leader': leader['name'],
            'leader_points': leader['points'],
            'max_remaining': max_points_with_wm,
            'champion_decided': leader['points'] - sorted_participants[1]['points'] > max_points_with_wm
        }


class F1KicktippCalculator:
    def __init__(self):
        # Punktesystem
        self.race_points = {1: 8, 2: 7, 3: 6, 4: 5, 5: 4, 6: 3, 7: 2, 8: 1}
        self.quali_points = {1: 4, 2: 3, 3: 2, 4: 1}
        self.wm_bonus = 20  # Punkte für richtigen Fahrer- oder Team-WM-Tipp
        self.consolation_point = 1  # 1 Punkt wenn Fahrer in Top X aber falsche Position

    def max_points_per_race(self):
        """Berechnet maximale Punkte pro Rennen (Quali + Rennen)"""
        max_quali = sum(self.quali_points.values())  # 4+3+2+1 = 10
        max_race = sum(self.race_points.values())  # 8+7+6+5+4+3+2+1 = 36
        return max_quali + max_race  # 46 Punkte pro Rennwochenende

    def calculate_race_points(self, tips, actual_result, is_quali=False):
        """
        Berechnet Punkte für ein einzelnes Rennen/Quali

        tips: Liste der getippten Fahrer in Reihenfolge [P1, P2, P3, ...]
        actual_result: Liste der tatsächlichen Fahrer in Reihenfolge [P1, P2, P3, ...]
        is_quali: True für Qualifying (Top 4), False für Rennen (Top 8)

        Returns: Anzahl der Punkte
        """
        points = 0
        points_system = self.quali_points if is_quali else self.race_points
        top_positions = 4 if is_quali else 8

        # Prüfe nur die relevanten Positionen
        tips = tips[:top_positions]
        actual_top = actual_result[:top_positions]

        for pos, tipped_driver in enumerate(tips, start=1):
            # Prüfe ob Fahrer auf richtiger Position
            if pos <= len(actual_result) and actual_result[pos - 1] == tipped_driver:
                # Richtige Position!
                points += points_system[pos]
            # Prüfe ob Fahrer in Top X ist (aber falsche Position)
            elif tipped_driver in actual_top:
                # Fahrer ist in Top X, aber falsche Position
                points += self.consolation_point

        return points

    def calculate_championship_status(self, participants, races_remaining):
        """
        Analysiert den Championship-Status

        participants: Liste von Dicts mit 'name', 'points', 'driver_wm_tip', 'team_wm_tip'
        races_remaining: Anzahl verbleibender Rennen
        """
        max_points_remaining = races_remaining * self.max_points_per_race()
        max_points_with_wm = max_points_remaining + (2 * self.wm_bonus)  # +40 für beide WM-Tipps

        # Sortiere nach Punkten
        sorted_participants = sorted(participants, key=lambda x: x['points'], reverse=True)
        leader = sorted_participants[0]

        print("=" * 70)
        print("🏁 FORMEL 1 KICKTIPP - CHAMPIONSHIP STATUS 🏁")
        print("=" * 70)
        print(f"\n📋 PUNKTESYSTEM:")
        print(f"   Qualifying (Top 4):")
        print(f"      • Richtige Position: P1=4, P2=3, P3=2, P4=1 Punkte")
        print(f"      • Fahrer in Top 4, aber falsche Position: {self.consolation_point} Punkt")
        print(f"   Rennen (Top 8):")
        print(f"      • Richtige Position: P1=8, P2=7, P3=6, P4=5, P5=4, P6=3, P7=2, P8=1")
        print(f"      • Fahrer in Top 8, aber falsche Position: {self.consolation_point} Punkt")
        print(f"   WM-Tipps: Je {self.wm_bonus} Punkte für richtigen Fahrer- und Team-Weltmeister")
        print(f"\n📊 Verbleibende Rennen: {races_remaining}")
        print(f"💯 Maximale Punkte pro Rennen: {self.max_points_per_race()} (Quali: 10 + Rennen: 36)")
        print(f"🏆 WM-Bonus verfügbar: {2 * self.wm_bonus} Punkte (2x {self.wm_bonus})")
        print(f"📈 Maximale Punkte noch zu vergeben: {max_points_with_wm}")

        print("\n" + "-" * 70)
        print("AKTUELLER STAND:")
        print("-" * 70)

        for i, p in enumerate(sorted_participants, 1):
            print(f"{i}. {p['name']}: {p['points']} Punkte")
            print(f"   └─ Fahrer-WM-Tipp: {p['driver_wm_tip']}")
            print(f"   └─ Team-WM-Tipp: {p['team_wm_tip']}")

        print("\n" + "=" * 70)
        print("CHAMPIONSHIP ANALYSE:")
        print("=" * 70)

        # Prüfe für jeden Teilnehmer
        for i, participant in enumerate(sorted_participants):
            print(f"\n🔍 {participant['name']}:")

            if i == 0:
                # Leader
                margin = participant['points'] - sorted_participants[1]['points']
                max_others_can_score = max_points_with_wm

                print(f"   Vorsprung: {margin} Punkte")
                print(f"   Verfolger können maximal holen: {max_others_can_score} Punkte")

                if margin > max_others_can_score:
                    print(f"   ✅ CHAMPION! Uneinholbar vorne!")
                else:
                    points_needed_to_secure = max_others_can_score - margin + 1
                    print(f"   ⚠️  Noch nicht sicher!")
                    print(f"   💪 Benötigt noch {points_needed_to_secure} Punkte um sicher zu sein")
            else:
                # Verfolger
                gap = leader['points'] - participant['points']
                max_can_score = max_points_with_wm
                max_leader_can_score = max_points_with_wm

                print(f"   Rückstand auf {leader['name']}: {gap} Punkte")
                print(f"   Maximal noch zu holen: {max_can_score} Punkte")

                if gap > max_can_score:
                    print(f"   ❌ Mathematisch ausgeschieden")
                else:
                    # Berechne benötigte Punkte (worst case: Leader holt auch alles)
                    min_points_to_win = gap + 1
                    print(f"   ✅ Noch im Rennen!")
                    print(f"   💪 Mindestens {min_points_to_win} Punkte zum Überholen nötig")
                    print(f"   📌 Realistisch: Wenn Leader 0 Punkte macht, reichen {min_points_to_win} Punkte")
                    print(f"   📌 Worst Case: Wenn Leader alles holt, unmöglich einzuholen")

        print("\n" + "=" * 70)
        print("WM-TIPP BONUS ANALYSE:")
        print("=" * 70)

        # Analysiere Team-WM Tipps
        team_tips_count = {}
        for p in sorted_participants:
            team = p['team_wm_tip']
            if team not in team_tips_count:
                team_tips_count[team] = []
            team_tips_count[team].append(p['name'])

        print(f"🏆 Team-WM Tipps:")
        for team, players in team_tips_count.items():
            print(f"   {team}: {', '.join(players)} ({len(players)} Spieler)")

        # Analysiere Fahrer-WM Tipps
        driver_tips_count = {}
        for p in sorted_participants:
            driver = p['driver_wm_tip']
            if driver not in driver_tips_count:
                driver_tips_count[driver] = []
            driver_tips_count[driver].append(p['name'])

        print(f"\n🏁 Fahrer-WM Tipps:")
        for driver, players in driver_tips_count.items():
            print(f"   {driver}: {', '.join(players)} ({len(players)} Spieler)")

        # WM-Bonus Szenarien
        print("\n" + "=" * 70)
        print("🎯 WM-BONUS SZENARIEN:")
        print("=" * 70)

        for i, p in enumerate(sorted_participants):
            print(f"\n{'🥇' if i == 0 else '📍'} {p['name']} (aktuell {p['points']} Punkte):")

            # Best Case: Alle Rennen perfekt + beide WM-Tipps richtig
            best_case = p['points'] + max_points_remaining + 40
            print(f"   ✅ Best Case: {best_case} Punkte")
            print(f"      → Alle verbleibenden Rennen perfekt ({max_points_remaining} Pkt)")
            print(f"      → Fahrer-WM richtig ({self.wm_bonus} Pkt)")
            print(f"      → Team-WM richtig ({self.wm_bonus} Pkt)")

            # Realistic Case: Rennen perfekt, aber nur Team-WM richtig (weil gleicher Tipp)
            team_shared = len(team_tips_count[p['team_wm_tip']]) > 1
            if team_shared:
                realistic_case = p['points'] + max_points_remaining + 20
                print(f"   ⚠️  Realistischer Fall: {realistic_case} Punkte")
                print(f"      → Alle Rennen perfekt ({max_points_remaining} Pkt)")
                print(
                    f"      → Team-WM richtig ({self.wm_bonus} Pkt) - aber {len(team_tips_count[p['team_wm_tip']])} Spieler haben gleich getippt!")
                print(f"      → Fahrer-WM falsch (0 Pkt)")

            # Worst Case: Keine Punkte mehr
            worst_case = p['points']
            print(f"   ❌ Worst Case: {worst_case} Punkte")
            print(f"      → Alle verbleibenden Rennen: 0 Punkte")
            print(f"      → Beide WM-Tipps falsch: 0 Punkte")

            # Zeige WM-Bonus Vorteil/Nachteil
            print(f"   📊 WM-Bonus Analyse:")
            driver_competitors = len(driver_tips_count[p['driver_wm_tip']]) - 1
            team_competitors = len(team_tips_count[p['team_wm_tip']]) - 1

            if driver_competitors > 0:
                print(
                    f"      ⚠️  Fahrer-WM ({p['driver_wm_tip']}): {driver_competitors} weitere Spieler haben gleich getippt")
                print(f"         → Kein Vorteil wenn richtig!")
            else:
                print(f"      ✅ Fahrer-WM ({p['driver_wm_tip']}): Alleiniger Tipp")
                print(f"         → {self.wm_bonus} Punkte Vorteil wenn richtig!")

            if team_competitors > 0:
                print(
                    f"      ⚠️  Team-WM ({p['team_wm_tip']}): {team_competitors} weitere Spieler haben gleich getippt")
                print(f"         → Kein Vorteil wenn richtig!")
            else:
                print(f"      ✅ Team-WM ({p['team_wm_tip']}): Alleiniger Tipp")
                print(f"         → {self.wm_bonus} Punkte Vorteil wenn richtig!")

        return {
            'leader': leader['name'],
            'leader_points': leader['points'],
            'max_remaining': max_points_with_wm,
            'champion_decided': leader['points'] - sorted_participants[1]['points'] > max_points_with_wm
        }

def test_race_calc():
    # Beispiel: Punkte-Berechnung für ein einzelnes Rennen
    print("\n" + "=" * 70)
    print("BEISPIEL: Punkte-Berechnung für ein Rennen")
    print("=" * 70)
    print("Tipp Qualifying: [Verstappen, Norris, Leclerc, Piastri]")
    print("Tatsächlich:     [Norris, Verstappen, Piastri, Leclerc]")

    quali_tips = ["Verstappen", "Norris", "Leclerc", "Piastri"]
    quali_actual = ["Norris", "Verstappen", "Piastri", "Leclerc"]
    quali_points = calculator.calculate_race_points(quali_tips, quali_actual, is_quali=True)

    print(f"→ Punkte: {quali_points}")
    print("  Verstappen: Getippt P1, tatsächlich P2 → in Top 4 → 1 Punkt")
    print("  Norris: Getippt P2, tatsächlich P1 → in Top 4 → 1 Punkt")
    print("  Leclerc: Getippt P3, tatsächlich P4 → in Top 4 → 1 Punkt")
    print("  Piastri: Getippt P4, tatsächlich P3 → in Top 4 → 1 Punkt")
    print("  Gesamt: 4 Punkte (statt 0 ohne Trostpunkt-Regel!)")

    print("\nTipp Rennen: [Verstappen, Norris, Leclerc, Piastri, Sainz, Hamilton, Russell, Alonso]")
    print("Tatsächlich: [Verstappen, Leclerc, Norris, Piastri, Hamilton, Sainz, Alonso, Russell]")

    race_tips = ["Verstappen", "Norris", "Leclerc", "Piastri", "Sainz", "Hamilton", "Russell", "Alonso"]
    race_actual = ["Verstappen", "Leclerc", "Norris", "Piastri", "Hamilton", "Sainz", "Alonso", "Russell"]
    race_points = calculator.calculate_race_points(race_tips, race_actual, is_quali=False)

    print(f"→ Punkte: {race_points}")
    print("  Verstappen: P1 richtig → 8 Punkte")
    print("  Norris: Getippt P2, tatsächlich P3 → in Top 8 → 1 Punkt")
    print("  Leclerc: Getippt P3, tatsächlich P2 → in Top 8 → 1 Punkt")
    print("  Piastri: P4 richtig → 5 Punkte")
    print("  Sainz: Getippt P5, tatsächlich P6 → in Top 8 → 1 Punkt")
    print("  Hamilton: Getippt P6, tatsächlich P5 → in Top 8 → 1 Punkt")
    print("  Russell: Getippt P7, tatsächlich P8 → in Top 8 → 1 Punkt")
    print("  Alonso: Getippt P8, tatsächlich P7 → in Top 8 → 1 Punkt")
    print(f"  Gesamt: {race_points} Punkte")


if __name__ == "__main__":
    calculator = F1KicktippCalculator()

    participants = [
        {
            'name': 'Ich (Du)',
            'points': 415,
            'driver_wm_tip': 'Max Verstappen',
            'team_wm_tip': 'McLaren'
        },
        {
            'name': 'David',
            'points': 337,
            'driver_wm_tip': 'Oscar Piastri',
            'team_wm_tip': 'McLaren'
        }
    ]

    races_remaining = 4

    result = calculator.calculate_championship_status(participants, races_remaining)

    print("\n" + "=" * 70)
    print("ZUSAMMENFASSUNG:")
    print("=" * 70)
    if result['champion_decided']:
        print(f"🎉 {result['leader']} ist bereits CHAMPION! 🎉")
    else:
        print(f"⚔️  Das Rennen ist noch offen! Spannend bis zum Ende!")