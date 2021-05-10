from typing import *

from graph.player import Player


class Graph:
    _graph: Dict[Player, Set[Player]]
    _slug_to_player: Dict[str, Player]
    _name_to_slug: Dict[str, List[str]]
    vertices: int
    edges: int

    def __init__(self):
        self._graph = {}
        self.vertices = 0
        self.edges = 0

    def add_player(self, player: Player):
        """
        Adds a player as a vertex and their teammates as edges
        :return: None
        """
        # The vertex is already in the graph
        if player in self._graph:
            return
        # The vertex is not in the graph
        self._graph[player] = set()
        for team in player.teams:
            for year in player.teams[team]:
                self._graph[player].update(year["teammates"])
                self.edges += len(year["teammates"])
        self.vertices += 1

    def get_edges_player(self, player: Player):
        """
        Returns a list of all the teammates of the player, if the player does
        not exist return the empty list
        :param player:
        :return:
        """
        return self._graph.get(player, [])

    def get_player_from_slug(self, slug: str) -> Union[Player, None]:
        """
        Given a player slug, return the corresponding player,
        if the slug is not valid return None
        :param slug:
        :return: The player that has slug <slug> or None
        """
        return self._slug_to_player.get(slug, None)

    def get_players_from_name(self, name: str) -> Set[Player]:
        """
        Return a set of all players with name <name>
        :param name: The name of the player
        :return: A set of all players with that name
        """
        slugs = set()
        players = set()
        for player in self._name_to_slug.get(name, []):
            slugs.add(player)
        for slug in slugs:
            players.add(self._slug_to_player[slug])
        return players

    def is_teammate(self, player1: Player, player2: Player):
        """
        Returns True iff the players have every been teammates, otherwise false
        :param player1: The first player
        :param player2: The second player
        :return: player1 is a teammate of player2
        """
        return player1 in self._graph[player2]

    def search_bfs(self, slug1: str):
        colour, distance, pi = {}, {}, {}
        for vertex in self._graph:
            colour[vertex] = "white"
            distance[vertex] = float("inf")
            pi[vertex] = None
        queue = []
        source_player = self.get_player_from_slug(slug1)
        colour[source_player] = "gray"
        distance[source_player] = 0
        queue.append(source_player)
        while len(queue) > 0:
            current = queue.pop(0)
            for teammate in self.get_edges_player(current):
                if colour[teammate] == "white":
                    colour[teammate] = "gray"
                    distance[teammate] = distance[current] + 1
                    pi[teammate] = current
                    queue.append(teammate)
            colour[current] = "black"

        return distance, pi

    def get_path_p1_p2(self, slug1: str, slug2: str):
        distance, links = self.search_bfs(slug1)
        destination_player = self.get_player_from_slug(slug2)
        path = []
        while destination_player is not None:
            path.append(destination_player)
            destination_player = links[destination_player]
        return list(reversed(path))

    # def get_n_paths_p1_p2(self, slug1: str, slug2: str, n: int):
    #     paths = set()
    #     timeout = 0
    #     while len(paths) < n and timeout < 100:
    #         paths.add(self.get_path_p1_p2(slug1, slug2))
    #         timeout += 1
    #     return list(paths)

    def set_slug_to_player(self, slug_to_player: Dict[str, Player]):
        self._slug_to_player = slug_to_player

    def set_name_to_slug(self, name_to_slug: Dict[str, List[str]]):
        self._name_to_slug = name_to_slug
