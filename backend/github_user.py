from collections import Counter


class GitHubUser:
    def __init__(self, username, followers=0, repos=None, bio=None, company=None, location=None, blog=None, is_partial=False):
        self.username = username
        self.followers = followers
        self.repos = repos if repos else []
        self.bio = bio
        self.company = company
        self.location = location
        self.blog = blog
        self.is_partial = is_partial
        
        # Collect all languages from either the primary language field or the detailed 'languages' dict
        self._languages_list = []
        self._all_technologies_set = set()
        
        for r in self.repos:
            primary = r.get("language")
            if primary:
                self._languages_list.append(primary)
                self._all_technologies_set.add(primary)
                
            detailed_langs = r.get("languages", {})
            if detailed_langs:
                for lang in detailed_langs.keys():
                    self._all_technologies_set.add(lang)

    def get_most_used_language(self):
        """
        returns the most used language based on primary language of each repo
        """
        if not self.repos or not self._languages_list:
            return None
            
        return Counter(self._languages_list).most_common(1)[0][0]

    def get_all_technologies(self):
        """
        returns a sorted list of all unique languages used in the repos
        """
        return sorted(list(self._all_technologies_set))

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
            "repos": self.repos,
            "is_partial": self.is_partial
        }
