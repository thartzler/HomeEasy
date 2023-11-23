class unauthenticatedState():
    def __init__(self):
        # do something like maybe save the 
        pass

    def username(self):
        # Check the DB if the user is there. If so, move state to 
        # otherwise, move to NewUserState?
        pass


class unauthenticatedWithVerifiedUserState():
    def __itit__(self):
        # do something
        self.__username = None


    def username(self):
        self.__username = None


class authentication(Base):
    __table__ = Table('ProductReviews', metadata)#, autoload = True, autoload_with = engine)
    def __init__(self, username, password):
        
        self.__authState = unauthenticatedState()

    def username(self, user):
        self.__authState.username(user)
