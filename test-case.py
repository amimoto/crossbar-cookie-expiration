import time
import asyncio
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner

from http.cookies import SimpleCookie

AUTHID = 'joe'
TICKET = 'secret!!!'
REALM = 'realm1'
COOKIE_STORE = SimpleCookie()
COOKIE_NAME = 'cbtid'
WAIT = 2
URL = "ws://localhost:8080/ws"

#############################################################
# First login to get the COOKIE_NAME
#############################################################

print("\n\nFirst connection should succeed")
print("-----------------------------------\n\n")

class GetCookieComponent(ApplicationSession):
    """
    An application component using the time service.
    """

    def onConnect(self):
        self.join(self.config.realm, ["cookie", "ticket"], AUTHID)

    def onChallenge(self, challenge):
        return TICKET

    async def onJoin(self, details):
        print("JOINED! COOKIES:", self._transport.http_headers)
        COOKIE_STORE.load(self._transport.http_headers['set-cookie'])
        self.leave()

    def onDisconnect(self):
        asyncio.get_event_loop().stop()

    def onLeave(self, details):
        self.disconnect()

    def onDisconnect(self):
        asyncio.get_running_loop().stop()

runner = ApplicationRunner(URL, REALM)
runner.run(GetCookieComponent)

#############################################################
# Second attempt with Cookie
#############################################################

print("\n\nSecond connection should not succeed")
print("-----------------------------------\n\n")

class SetCookieComponent(ApplicationSession):

    def onConnect(self):
        self.join(self.config.realm, ["cookie"], AUTHID)

    async def onJoin(self, details):
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("onJoin should not be invoked")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(details)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        self.leave()

    def onDisconnect(self):
        asyncio.get_event_loop().stop()

    def onLeave(self, details):
        print("Client session left: {}".format(details))
        self.disconnect()

    def onDisconnect(self):
        print("Client session disconnected.")
        asyncio.get_running_loop().stop()

# Delay for WAIT seconds to ensure it exceeds max_age=1
print(f"Waiting {WAIT} seconds")
time.sleep(WAIT)

# Then attempt to login with the cookie
cookie = COOKIE_STORE[COOKIE_NAME]
headers = {
            'cookie': cookie.OutputString([COOKIE_NAME]),
        }
runner_cookied = ApplicationRunner(URL, REALM, headers=headers)
runner_cookied.run(SetCookieComponent)

