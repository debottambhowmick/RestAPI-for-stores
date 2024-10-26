"""
blocklist.py
This file just contains the blocklist of the JWT tokens. It will be imported by
app and the logout resource so that tokens can be added to the blocklist when the
user logs out.

redis would be a perfect solution for things like this. but as of now we will use a python set 
"""
BLOCKLIST = set()