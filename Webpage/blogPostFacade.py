
from DB_Object_Creator import BlogPost


class BlogPostFacade:

    def __init__(self) -> None:
        pass

    def getBlogPost(self, ID, SessionID):
        '''
        Check the Blog post with the ID to see if it's a paid or free post
        If the post is free or (the post is paid and the user has a valid session and the 
        If it's paid, verify the SessionID is valid
        Then check the access level of the user
        If the user has privelege to view the post, then create 
        '''
