# f1_kicktipp_cli.py
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

console = Console()

class F1KicktippCLI:
    def __init__(self):
        self.race_points = {1: 8, 2: 7, 3: 6, 4: 5, 5: 4, 6: 3, 7: 2, 8: 1}
        self.quali_points = {1: 4, 2: 3, 3: 2, 4: 1}
        self.wm_bonus = 20
        self.consolation_point = 1

    def max_points_per_race(self):
        return sum(self.race_points.values()) + sum(self.quali_points.values())

    def calculate_race_points(self, tips, actual_result, is_quali=False):
        points = 0
        points_system = self.quali_points if is_quali else self.race_points
        top_positions = 4 if is_quali else 8
        tips = tips[:top_positions]
        actual_top = actual_result[:top_positions]

        for pos, tipped_driver in enumerate(tips, start=1):
            if pos <= len(actual_result) and actual_result[pos - 1] == tipped_driver:
                points += points_system[pos]
            elif tipped_driver in actual_top:
                points += self.consolation_point
        return points

    def calculate_championship_status(self, participants, races_remaining):
        max_points_remaining = races_remaining * self.max_points_per_race()
        max_points_with_wm = max_points_remaining + (2 * self.wm_bonus)
        sorted_participants = sorted(participants, key=lambda x: x["points"], reverse=True)
        leader = sorted_participants[0]

        console.print("\n")
        console.rule("[bold red]🏁 FORMEL 1 KICKTIPP STATUS 🏁[/bold red]")

        # Punktesystem Übersicht
        console.print(
            f"[bold yellow]Punktesystem:[/bold yellow]\n"
            f"• Quali (Top 4): 4–3–2–1 + [bold]{self.consolation_point}[/bold] Trostpunkt\n"
            f"• Rennen (Top 8): 8–7–6–5–4–3–2–1 + [bold]{self.consolation_point}[/bold] Trostpunkt\n"
            f"• WM-Tipps: je [bold]{self.wm_bonus}[/bold] Punkte\n"
        )

        console.print(
            f"📊 Verbleibende Rennen: [bold]{races_remaining}[/bold]\n"
            f"💯 Max. Punkte pro Rennen: [bold]{self.max_points_per_race()}[/bold]\n"
            f"🏆 WM-Bonus verfügbar: [bold]{2 * self.wm_bonus}[/bold]\n"
            f"📈 Noch maximal zu vergeben: [bold]{max_points_with_wm}[/bold]\n"
        )

        # Rangliste
        table = Table(title="Aktueller Punktestand", style="bold cyan")
        table.add_column("Pos", justify="center")
        table.add_column("Name")
        table.add_column("Punkte", justify="right")
        table.add_column("Fahrer-WM Tipp")
        table.add_column("Team-WM Tipp")

        for i, p in enumerate(sorted_participants, 1):
            table.add_row(str(i), p["name"], str(p["points"]), p["driver_wm_tip"], p["team_wm_tip"])
        console.print(table)

        console.rule("📊 Championship Analyse")

        for i, participant in enumerate(sorted_participants):
            if i == 0:
                margin = participant["points"] - sorted_participants[1]["points"]
                if margin > max_points_with_wm:
                    status = "[bold green]✅ Uneinholbar – Champion![/bold green]"
                else:
                    status = "[bold yellow]⚠️ Noch nicht sicher![/bold yellow]"
                    need = max_points_with_wm - margin + 1
                    status += f"\n💪 Benötigt noch [bold]{need}[/bold] Punkte zur sicheren Meisterschaft."
                console.print(Panel(f"[bold]{participant['name']}[/bold] führt mit [bold]{margin}[/bold] Punkten.\n{status}", title="🏆 Leader"))
            else:
                gap = leader["points"] - participant["points"]
                if gap > max_points_with_wm:
                    status = "[bold red]❌ Mathematisch ausgeschieden[/bold red]"
                else:
                    need = gap + 1
                    status = f"[bold green]✅ Noch im Rennen![/bold green]\nBenötigt mindestens [bold]{need}[/bold] Punkte zum Überholen."
                console.print(Panel(f"[bold]{participant['name']}[/bold]: Rückstand [bold]{gap}[/bold] Punkte.\n{status}", title="🏁 Herausforderer"))

        console.rule("🎯 WM-Bonus Szenarien")

        for p in sorted_participants:
            best = p["points"] + max_points_remaining + 40
            worst = p["points"]
            console.print(
                Panel(
                    f"[bold]{p['name']}[/bold]:\n"
                    f"🏆 Aktuell: {p['points']} Punkte\n"
                    f"✅ Best Case: {best}\n"
                    f"❌ Worst Case: {worst}",
                    title="📈 Szenarien",
                )
            )

        champion_decided = leader["points"] - sorted_participants[1]["points"] > max_points_with_wm

        console.rule("[bold red]ERGEBNIS[/bold red]")
        if champion_decided:
            console.print(f"🎉 [bold green]{leader['name']}[/bold green] ist bereits CHAMPION! 🏆")
        else:
            console.print(f"⚔️ Das Rennen ist noch offen! [bold]{leader['name']}[/bold] führt derzeit.")

        return {
            "leader": leader["name"],
            "leader_points": leader["points"],
            "max_remaining": max_points_with_wm,
            "champion_decided": champion_decided,
        }


if __name__ == "__main__":
    calculator = F1KicktippCLI()

    participants = [
        {"name": "Ich (Du)", "points": 415, "driver_wm_tip": "Max Verstappen", "team_wm_tip": "McLaren"},
        {"name": "David", "points": 337, "driver_wm_tip": "Oscar Piastri", "team_wm_tip": "McLaren"},
    ]

    races_remaining = 4

    calculator.calculate_championship_status(participants, races_remaining)