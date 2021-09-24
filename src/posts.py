from google.cloud import ndb


class Posts(ndb.Model):
    """
        this is for the blog
    """

    post_url = ndb.StringProperty()
    post_title = ndb.StringProperty()
    post_description = ndb.StringProperty()
    post_body = ndb.StringProperty()

    post_date = ndb.DateProperty()
    post_time = ndb.TimeProperty()

    post_category = ndb.StringProperty()
    post_seo_description = ndb.StringProperty()

