""" Simple Hypixel-API in Python, by Snuggle | MODIFIED BY @t_cr1ck (discord)/@ACoolerName (github). DO NOT USE MODIFIED VERSION, IT PROBABLY WONT WORK FOR YOUR USECASE """
__version__ = '0.8.0'
# pylint: disable=C0103
# TODO: Add more comments. Explain what's happening!
# TODO: Add API-usage stat-tracking. Like a counter of the number of requests and how many per minute etc.

from random import choice
from time import time
import grequests

import leveling

HYPIXEL_API_URL = 'https://api.hypixel.net/'
UUIDResolverAPI = "https://sessionserver.mojang.com/session/minecraft/profile/"

apikey = "YOUR API KEY HERE"
verified_api_keys = [apikey]

requestCache = {}
cacheTime = 60

apirequests = 0

class PlayerNotFoundException(Exception):
    """ Simple exception if a player/UUID is not found. This exception can usually be ignored.
        You can catch this exception with ``except hypixel.PlayerNotFoundException:`` """
    pass

class SkyblockUUIDRequired(Exception):
    """Simple exception to tell the user that in the Skyblock API, UUID's are required and names cannot be used.
    Catch this exception with ``except hypixel.SkyblockUUIDRequired:``"""
    pass
class GuildIDNotValid(Exception):
    """ Simple exception if a Guild is not found using a GuildID. This exception can usually be ignored.
        You can catch this exception with ``except hypixel.GuildIDNotValid:`` """
    pass

class HypixelAPIError(Exception):
    """ Simple exception if something's gone very wrong and the program can't continue. """
    pass


def getJSON(typeOfRequest, **kwargs):
    global apirequests
    """ This private function is used for getting JSON from Hypixel's Public API. """
    requestEnd = ''
    if typeOfRequest == 'key':
        api_key = kwargs['key']
    else:
        api_key = choice(verified_api_keys) # Select a random API key from the list available.

        if typeOfRequest == 'player':
            UUIDType = 'uuid'
            uuid = kwargs['uuid']
            if len(uuid) <= 16:
                UUIDType = 'name' # TODO: I could probably clean this up somehow.
        if typeOfRequest == 'skyblockplayer':
            typeOfRequest = "/skyblock/profiles"
        for name, value in kwargs.items():
            if typeOfRequest == "player" and name == "uuid":
                name = UUIDType
            requestEnd += '&{}={}'.format(name, value)

    cacheURL = HYPIXEL_API_URL + '{}?key={}{}'.format(typeOfRequest, "None", requestEnd) # TODO: Lowercase
    allURLS = [HYPIXEL_API_URL + '{}?key={}{}'.format(typeOfRequest, api_key, requestEnd)] # Create request URL.
    apirequests += 1
    print(f'Sent API REQUEST #{apirequests} with url {allURLS}')

    # If url exists in request cache, and time hasn't expired...
    if cacheURL in requestCache and requestCache[cacheURL]['cacheTime'] > time():
        response = requestCache[cacheURL]['data'] # TODO: Extend cache time
    else:
        requests = (grequests.get(u) for u in allURLS)
        responses = grequests.imap(requests)
        for r in responses:
            response = r.json()

        if not response['success']:
            raise HypixelAPIError(response)
        if typeOfRequest == 'player':
            if response['player'] is None:
                raise PlayerNotFoundException(uuid)
        if typeOfRequest != 'key': # Don't cache key requests.
            requestCache[cacheURL] = {}
            requestCache[cacheURL]['data'] = response
            requestCache[cacheURL]['cacheTime'] = time() + cacheTime # Cache request and clean current cache.
            cleanCache()
    try:
        return response[typeOfRequest]
    except KeyError:
        return response

def cleanCache():
    """ This function is occasionally called to clean the cache of any expired objects. """
    itemsToRemove = []
    for item in requestCache:
        try:
            if requestCache[item]['cacheTime'] < time():
                itemsToRemove.append(item)
        except:
            pass
    for item in itemsToRemove:
        requestCache.pop(item)

def setCacheTime(seconds):
    """ This function sets how long the request cache should last, in seconds.

        Parameters
        -----------
        seconds : float
            How long you would like Hypixel-API requests to be cached for.
    """
    try:
        global cacheTime
        cacheTime = float(seconds)
        return "Cache time has been successfully set to {} seconds.".format(cacheTime)
    except ValueError as chainedException:
        raise HypixelAPIError("Invalid cache time \"{}\"".format(seconds)) from chainedException

class Player:
    """ This class represents a player on Hypixel as a single object.
        A player has a UUID, a username, statistics etc.

        Raises
        ------
        PlayerNotFoundException
            If the player cannot be found, this will be raised.

        Parameters
        -----------
        Username/UUID : string
            Either the UUID or the username (Deprecated) for a Minecraft player.

        Attributes
        -----------
        JSON : string
            The raw JSON receieved from the Hypixel API.

        UUID : string
            The player's UUID.
    """

    JSON = None
    UUID = None

    def __init__(self, UUID):
        """ This is called whenever someone uses hypixel.Player('Snuggle').
            Get player's UUID, if it's a username. Get Hypixel-API data. """
        self.UUID = UUID
        if len(UUID) <= 16: # If the UUID isn't actually a UUID... *rolls eyes* Lazy people.
            self.JSON = getJSON('player', uuid=UUID) # Get player's Hypixel-API JSON information.
            JSON = self.JSON
            self.UUID = JSON['uuid'] # Pretend that nothing happened and get the UUID from the API.
        elif len(UUID) in (32, 36): # If it's actually a UUID, with/without hyphens...
            self.JSON = getJSON('player', uuid=UUID)
        else:
            raise PlayerNotFoundException(UUID)
        
    def getPlayerInfo(self):
        """ This is a simple function to return a bunch of common data about a player. """
        JSON = self.JSON
        playerInfo = {}
        playerInfo['uuid'] = self.UUID
        playerInfo['displayName'] = Player.getName(self)
        playerInfo['rank'] = Player.getRank(self)
        playerInfo['networkLevel'] = Player.getLevel(self)
        JSONKeys = ['karma', 'firstLogin', 'lastLogin',
                    'mcVersionRp', 'networkExp', 'socialMedia', 'prefix']
        for item in JSONKeys:
            try:
                playerInfo[item] = JSON[item]
            except KeyError:
                pass
        return playerInfo
    
    def getName(self):
        """ Just return player's name. """
        JSON = self.JSON
        return JSON['displayname']
    
    def getLevel(self):
        """ This function calls leveling.py to calculate a player's network level. """
        JSON = self.JSON
        
        networkExp = JSON.get('networkExp', 0)        
        networkLevel = JSON.get('networkLevel', 0)
        
        exp = leveling.getExperience(networkExp, networkLevel)
        myoutput = leveling.getExactLevel(exp)
        return myoutput
    
    def getRank(self):
        """ This function returns a player's rank, from their data. """
        JSON = self.JSON
        playerRank = {} # Creating dictionary.
        playerRank['wasStaff'] = False
        possibleRankLocations = ['packageRank', 'newPackageRank', 'monthlyPackageRank', 'rank']
        # May need to add support for multiple monthlyPackageRank's in future.

        for Location in possibleRankLocations:
            if Location in JSON:
                if Location == 'rank' and JSON[Location] == 'NORMAL':
                    playerRank['wasStaff'] = True
                else:
                    if JSON[Location] == "NONE": # If monthlyPackageRank expired, ignore "NONE". See: https://github.com/Snuggle/hypixel.py/issues/9
                        continue
                    dirtyRank = JSON[Location].upper().replace("_", " ").replace(" Plus", "+")
                    playerRank['rank'] = dirtyRank.replace("Superstar", "MVP++").replace("Youtuber", "YouTube")

        if 'rank' not in playerRank:
            playerRank['rank'] = 'Non'

        return playerRank
    
    def getGuildID(self):
        """ This function is used to get a GuildID from a player. """
        UUID = self.UUID
        GuildID = getJSON('findGuild', byUuid=UUID)
        return GuildID['guild']
    
    def getSession(self):
        """ This function is used to get a player's session information. """
        UUID = self.UUID
        try:
            session = getJSON('session', uuid=UUID)
        except HypixelAPIError:
            session = None
        return session
    
class Guild:
    """ This class represents a guild on Hypixel as a single object.
        A guild has a name, members etc.

        Parameters
        -----------
        GuildID : string
            The ID for a Guild. This can be found by using :class:`Player.getGuildID()`.


        Attributes
        -----------
        JSON : string
            The raw JSON receieved from the Hypixel API.

        GuildID : string
            The Guild's GuildID.

    """
    JSON = None
    GuildID = None
    def __init__(self, GuildID):
        try:
            if len(GuildID) == 24:
                self.GuildID = GuildID
                self.JSON = getJSON('guild', id=GuildID)
        except Exception as chainedException:
            raise GuildIDNotValid(GuildID) from chainedException
    
    

    def getMembers(self):
        guildRoles = ['Guild Master', 'Arachne', 'Keeper', 'Spider', 'Brood', 'LEACH']
        memberDict = self.JSON['members']
        allGuildMembers = {}
        for role in guildRoles:
            allGuildMembers[role] = []
        memberList = []
        for member in memberDict:
            memberList.append({'role': member['rank'], 'uuid': member['uuid']})
        for member in memberList:
            roleList = allGuildMembers[member['role']]
            roleList.append(member['uuid'])

        return allGuildMembers




class Auction:
    """ This class represents an auction on Hypixel Skyblock as a single object.
        
    """
    def __init__(self):
        """"Called to create an Auction class."""
        pass    
    def getAuctionInfo(self, PageNumber):
        """Gets all the auction info for a specified page. PageNumber is the page that is requested and can be in int form or string"""
        return getJSON("skyblock/auction", page = str(PageNumber))
    #TODO Add more info

class SkyblockPlayer:
    """A class for a Skyblock player. It requires a UUID, and will return stats on the player
    Raises
    ------
    SkyblockUUIDRequired
        If you pass in a normal username such as RedKaneChironic, will throw an error as Hypixel Skyblock's API currently does not support usernames
    PlayerNotFoundException
        If the player cannot be found, this will be raised.
        
    Parameters
    -----------
    UUID: string
        UUID of the Player
    JSON: string
        Raw JSON data"""
    def __init__(self, UUID):
        self.UUID = UUID
        if len(UUID) <= 16: #UUID is a Minecraft username
            raise SkyblockUUIDRequired(UUID)
        elif len(UUID) in (32, 36):
            self.JSON = getJSON('skyblock/profiles', uuid = UUID)
        else:
            raise PlayerNotFoundException(UUID)
        
if __name__ == "__main__":
    print("This is a Python library and shouldn't be run directly.\n"
          "Please look at https://github.com/Snuggle/hypixel.py for usage & installation information.")
