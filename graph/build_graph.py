import json
from typing import *
from datetime import datetime
from graph.player import Player
from graph.graph import Graph


def add_team(d_roster: List[Dict[str, str]], name: str, year: int, all_players:
             Dict[str, Player], name_to_slug: Dict[str, List[str]]) \
             -> Set[Player]:
    roster = set()
    for player in d_roster:
        if player["slug"] in all_players:
            roster.add(all_players[player["slug"]])
        else:
            dob = datetime.strptime(player["dob"], "%B %d, %Y")
            p = Player(player["name"], player["slug"], dob)
            all_players[player["slug"]] = p
            if player["name"] not in name_to_slug:
                name_to_slug[player["name"]] = []
            name_to_slug[player["name"]].append(player["slug"])
            roster.add(p)
    for player in roster:
        # Add everyone as a teammate except for myself
        player.add_team(name, year, roster.difference({player}))
    return roster


def build_graph() -> Graph:
    # Load the data and open the file
    f = open("../data.json", "r")
    data = json.load(f)
    f.close()
    # A map from slug to player object of all players (Player) to ever play
    all_players: Dict[str, Player] = {}
    # Player name to possible slugs
    name_to_slug: Dict[str, List[str]] = {}
    # For each season for each team, add their players to the set
    for season in data:
        for team in data[season]:
            add_team(team["roster"], team["team"], int(season),
                     all_players, name_to_slug)
    # Initialize and populate the graph
    graph = Graph()
    graph.set_name_to_slug(name_to_slug)
    graph.set_slug_to_player(all_players)
    for slug in all_players:
        graph.add_player(all_players[slug])

    return graph

    # if __name__ == "__main__":
    #
    #     minn = float('inf')
    #     player = None

    # slug1 = "townska01"
    # slug2 = "antetgi01"
    # result = graph.get_path_p1_p2(slug1, slug2)
    # print(result, len(result) - 1)

    # for source_slug in all_players:
    #     distance, path = graph.search_bfs(source_slug)
    #     if float("inf") not in distance.values():
    #         d = max(distance, key=distance.get)
    #         if distance[d] <= minn:
    #             minn = distance[d]
    #             player = graph.get_player_from_slug(source_slug)
    #             print(minn, player)
    # print(player, minn)
