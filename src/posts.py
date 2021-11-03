from google.cloud import ndb


class Posts(ndb.Model):
    """
    **Class Posts**
        this is for the blog
    """
    _summary_len: int = 36
    post_url = ndb.StringProperty()
    post_title = ndb.StringProperty()
    post_description = ndb.StringProperty()
    post_body = ndb.StringProperty()

    post_date = ndb.DateProperty()
    post_time = ndb.TimeProperty()

    post_category = ndb.StringProperty()
    post_seo_description = ndb.StringProperty()

    @property
    def body_summary(self) -> str:
        """
            returns a summarized version of post_body        
        """
        if len(self.post_body) > self._summary_len:
            return self.post_body[0:self._summary_len]
        return self.post_body

