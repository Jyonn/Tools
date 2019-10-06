from App.Network.ip_lookup import IPLookup
from Base.router import Router

networkRouter = Router()
networkRouter.register('ip-lookup', IPLookup)
