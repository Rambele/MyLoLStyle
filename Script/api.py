import requests

class RiotAPI:
    def __init__(self, api_key: str, region: str = "euw1", routing: str = "europe"):
        self.api_key = api_key
        self.headers = {"X-Riot-Token": api_key}
        self.region = region
        self.routing = routing

    def get_puuid(self, game_name: str, tag_line: str):
        url = f"https://{self.routing}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
        res = requests.get(url, headers=self.headers)
        return res.json().get("puuid") if res.status_code == 200 else None

    def get_summoner_id(self, puuid: str):
        url = f"https://{self.region}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
        res = requests.get(url, headers=self.headers)
        return res.json().get("id") if res.status_code == 200 else None

    def get_rank_info(self, puuid: str):
        summoner_id = self.get_summoner_id(puuid)
        if not summoner_id:
            return None
        url = f"https://{self.region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}"
        res = requests.get(url, headers=self.headers)
        if res.status_code != 200:
            return None
        for queue in res.json():
            if queue["queueType"] == "RANKED_SOLO_5x5":
                return {
                    "tier": queue["tier"],
                    "rank": queue["rank"],
                    "lp": queue["leaguePoints"],
                    "wins": queue["wins"],
                    "losses": queue["losses"]
                }
        return {"tier": "UNRANKED", "rank": "", "lp": 0, "wins": 0, "losses": 0}

    def get_match_ids(self, puuid: str, count: int = 30, queue: int = None):
        """
        queue (int) : 
        420 = Ranked Solo
        440 = Ranked Flex
        430 = Normale
        450 = ARAM
        None = tous types de parties
        """
        url = f"https://{self.routing}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}"
        if queue is not None:
            url += f"&queue={queue}"
        res = requests.get(url, headers=self.headers)
        return res.json() if res.status_code == 200 else []

    def get_match_data(self, match_id: str):
        url = f"https://{self.routing}.api.riotgames.com/lol/match/v5/matches/{match_id}"
        res = requests.get(url, headers=self.headers)
        return res.json() if res.status_code == 200 else None
