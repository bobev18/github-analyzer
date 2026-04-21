from collections import Counter


class GitHubUser:
    def __init__(self, username, followers=0, repos=None, bio=None, company=None, location=None, blog=None):
        self.username = username
        self.followers = followers
        self.repos = repos if repos else []
        self.bio = bio
        self.company = company
        self.location = location
        self.blog = blog
        self._languages = [r["language"] for r in self.repos if r.get("language")]

    def get_most_used_language(self):
        """
        returns the most used language in all of the repos
        """
        if not self.repos:
            return None
        
        if not self._languages:
            return None
            
        return Counter(self._languages).most_common(1)[0][0]

    def get_all_technologies(self):
        """
        returns a list of all unique languages used in the repos
        """
        return sorted(list(set(self._languages)))

    def to_dict(self):
        return {
            "username": self.username,
            "followers": self.followers,
            "bio": self.bio,
            "company": self.company,
            "location": self.location,
            "blog": self.blog,
            "most_used_language": self.get_most_used_language(),
            "all_technologies": self.get_all_technologies(),
            "repos": self.repos
        }
