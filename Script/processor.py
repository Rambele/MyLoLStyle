
from typing import List

class ImpactProcessor:

    def __init__(self, match_data: dict):
        self.participants = match_data.get("info", {}).get("participants", [])

    def _get_player(self, puuid: str):
        return next((p for p in self.participants if p.get("puuid") == puuid), None)

    def _get_teammates(self, team_id):
        return [p for p in self.participants if p.get("teamId") == team_id]

    def _get_opponent(self, team_id, role):
        return next((p for p in self.participants if p.get("teamId") != team_id and p.get("individualPosition") == role), None)

    def _percent(self, player_val, group_val):
        return round((player_val / group_val) * 100, 2) if group_val else 0.0

    def calculate_impact_vs_team(self, puuid: str, stat_keys: List[str]) -> dict:
        player = self._get_player(puuid)
        if not player:
            return {}

        team_id = player.get("teamId")
        teammates = self._get_teammates(team_id)

        results = {}
        for key in stat_keys:
            player_val = player.get(key, 0)
            team_total = sum(p.get(key, 0) for p in teammates)
            results[f"{key}_vs_team_%"] = self._percent(player_val, team_total)

        return results

    def compare_vs_opponent(self, puuid: str, stat_keys: List[str]) -> dict:
        player = self._get_player(puuid)
        if not player:
            return {}

        team_id = player.get("teamId")
        role = player.get("individualPosition")
        opponent = self._get_opponent(team_id, role)
        if not opponent:
            return {}

        player_team_impact = self.calculate_impact_vs_team(puuid, stat_keys)
        opponent_team_impact = self.calculate_impact_vs_team(opponent.get("puuid"), stat_keys)

        comparison = {}
        for key in stat_keys:
            player_impact = player_team_impact.get(f"{key}_vs_team_%", 0)
            opponent_impact = opponent_team_impact.get(f"{key}_vs_team_%", 0)
            comparison[f"{key}_impact_diff"] = round(player_impact - opponent_impact, 2)

        return comparison
