from App.Entertainment.soul_match import SoulMatch
from Base.router import Router

entertainmentRouter = Router()
entertainmentRouter.register('soul-match', SoulMatch)
