from collections import Counter


class GitHubUser:
    def __init__(self, username, followers=0, repos=None):
        self.username = username
        self.followers = followers
        self.repos = repos if repos else []

    def get_most_used_language(self):
        """
        returns the most used language in all of the repos
        """
        if not self.repos:
            return None
        
        languages = [r["language"] for r in self.repos if r["language"]]
        if not languages:
            return None
            
        return Counter(languages).most_common(1)[0][0]

    def get_all_technologies(self):
        """
        returns a list of all unique languages used in the repos
        """
        languages = {r["language"] for r in self.repos if r["language"]}
        return sorted(list(languages))

    def to_dict(self):
        return {
            "username": self.username,
            "followers": self.followers,
            "most_used_language": self.get_most_used_language(),
            "all_technologies": self.get_all_technologies(),
            "repos": self.repos
        }