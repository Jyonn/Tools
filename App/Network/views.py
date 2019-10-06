from App.Network.ip import IPLookup
from Base.router import Router

networkRouter = Router()
networkRouter.register('ip-lookup', IPLookup)
