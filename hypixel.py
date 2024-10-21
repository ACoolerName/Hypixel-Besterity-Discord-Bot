""" Hypixel API Requester by ACoolerName """
__version__ = '1.0.0'

import grequests
from time import time

# Hypixel and Mojang API URLs
HYPIXEL_API_URL = 'https://api.hypixel.net/v2'
UUID_RESOLVER_API = "https://sessionserver.mojang.com/session/minecraft/profile/"

# Read the API key from a file
with open('api_key.txt', 'r') as file:
    api_key = file.read().strip()

# Cache and request tracking
requestCache = {}
cacheTime = 60
apirequests = 0

class PlayerNotFoundException(Exception):
    """Raised when a player/UUID is not found."""
    pass

class SkyblockUUIDRequired(Exception):
    """Raised when a UUID is required for Skyblock API."""
    pass

class GuildIDNotValid(Exception):
    """Raised when a GuildID is not valid."""
    pass

class HypixelAPIError(Exception):
    """Raised for Hypixel API-related errors."""
    pass

def getJSON(typeOfRequest, **kwargs):
    """ Fetches JSON from the Hypixel API. """
    global apirequests
    requestEnd = ''
    
    # Set request type and URL endpoint
    if typeOfRequest == 'skyblockplayer':
        typeOfRequest = "/skyblock/profiles"
    elif typeOfRequest == 'guild':
        typeOfRequest = '/guild'

    # Append arguments to the request
    for name, value in kwargs.items():
        requestEnd += f'{name}={value}'
    
    # Construct the full URL based on the request type
    if typeOfRequest == '/guild':
        requestURL = f"{HYPIXEL_API_URL}{typeOfRequest}?key={api_key}&{requestEnd}"  # Guild URL format
    elif typeOfRequest == "/skyblock/profiles":
        requestURL = f"{HYPIXEL_API_URL}{typeOfRequest}?{requestEnd}&key={api_key}"  # Skyblock player URL format
    else:
        raise ValueError("Unknown request type")  # Optional: Handle unexpected request types
    
    # Log the request
    apirequests += 1
    print(f'Sent API REQUEST #{apirequests} with url {requestURL}')
    
    # Check cache
    if requestURL in requestCache and requestCache[requestURL]['cacheTime'] > time():
        response = requestCache[requestURL]['data']
    else:
        # Use grequests.map to handle the request and get the response correctly
        response = grequests.map([grequests.get(requestURL)])[0].json()
        
        # Handle API errors
        if not response['success']:
            raise HypixelAPIError(response)
        
        # Cache the response
        requestCache[requestURL] = {
            'data': response,
            'cacheTime': time() + cacheTime
        }
        cleanCache()
    
    return response


def cleanCache():
    """ Cleans the cache of expired objects. """
    expiredItems = [item for item in requestCache if requestCache[item]['cacheTime'] < time()]
    for item in expiredItems:
        requestCache.pop(item)

# UUID Retrieval from Mojang
def getUUID(username):
    """Retrieves a player's UUID from Mojang's API."""
    requestURL = f"{UUID_RESOLVER_API}{username}"
    # Use grequests.map to handle the request and get the response correctly
    response = grequests.map([grequests.get(requestURL)])[0].json()
    
    if 'error' in response:
        raise PlayerNotFoundException(f"Player {username} not found.")
    
    return response['id']

# Skyblock Player Class
class SkyblockPlayer:
    """Represents a Skyblock player, fetching their profiles using UUID."""
    
    def __init__(self, UUID):
        self.UUID = UUID
        if len(UUID) <= 16:
            raise SkyblockUUIDRequired("Skyblock API requires a UUID.")
        self.JSON = getJSON('skyblockplayer', uuid=UUID)
    
    def getProfiles(self):
        """Returns the player's Skyblock profiles.""" 
        return self.JSON

# Guild Class
class Guild:
    """Represents a guild on Hypixel."""
    
    def __init__(self, GuildID):
        self.GuildID = GuildID
        if len(GuildID) != 24:
            raise GuildIDNotValid("Invalid Guild ID")
        self.JSON = getJSON('guild', id=GuildID)
    
    def getMembers(self):
        """Returns the guild members, categorized by role."""

        # Check if 'guild' and 'members' keys exist
        if 'guild' not in self.JSON or 'members' not in self.JSON['guild']:
            raise HypixelAPIError("The response does not contain 'guild' or 'members': " + str(self.JSON))
    
        memberDict = self.JSON['guild']['members']  # Access members correctly
        guildRoles = ['Guild Master', 'Arachne', 'Keeper', 'Spider', 'Brood', 'LEACH']
        allGuildMembers = {role: [] for role in guildRoles}

        for member in memberDict:
            role = member['rank'] if 'rank' in member else 'Unassigned'  # Handle missing 'rank'
            uuid = member['uuid']
            allGuildMembers[role].append(uuid)
    
        return allGuildMembers
