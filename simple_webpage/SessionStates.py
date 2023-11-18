from userTypes import UserFactory, NoUserMember, BasicMember, PremiumMember, AdminMember

class SessionState:
    def __init__(self) -> None:
        # This is a parent class for the SessionStates
        pass

class LoggedInState(SessionState):
    def __init__(self) -> None:
        user = NoUserMember
        super().__init__()
        pass



class LoggedOutState(SessionState):
    def __init__(self) -> None:
        super().__init__()
        pass

    def login():
        pass