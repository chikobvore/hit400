
#this script handles the database connections
import pymongo

# client = pymongo.MongoClient("mongodb+srv://ladsroot:ladsroot@lads.f97uh.mongodb.net/tau?retryWrites=true&w=majority")
# db = client.tau


# client = pymongo.MongoClient("mongodb+srv://ladsroot:ladsroot@lads.f97uh.mongodb.net/tau?retryWrites=true&w=majority")
# db = client.tau

client = pymongo.MongoClient("mongodb+srv://root:Tech_Team@coverlink.uj2zx.mongodb.net/coverlink?retryWrites=true&w=majority")
db = client.coverlink       
