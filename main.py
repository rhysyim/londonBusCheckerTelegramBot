import os
import telegram.ext
import requests
import string
from keep_alive import keep_alive

def replaceStop(stop):
    return str(stop).replace(' dr ', ' drive ').replace(' rd', ' road ').replace(' st  ', ' street ').replace(' blvd', ' boulevard ').replace(' ln',' lane ').replace(' av ',' avenue ')

def start(update, context):
    update.message.reply_text("Welcome to LondonBusChecker Telegram Bot\nUse /help to get help")

def help(update, context):
    update.message.reply_text("Use 'route' to search for a line (e.g. route 1)\n\nUse 'time' for arrivals at a stop in the coming 30 minutes (e.g. time New Oxford Street)\n\nUse 'stop' to search for lines stopping at a stop (e.g. stop New Oxford Street)\n\nYou can use the following abbreviations: blvd, dr, st, av, ln, rd. \n - For st, please add two spaces after the abbreviation \n - For dr and av, please add a space after the abbreviation\n\nYou can use uppercase or lowercase for your requests")

def about(update,context):
    update.message.reply_text("This is a Telegram Bot of London Buses\nUse /start to start\nPowered by TfL Open Data\nContains OS data © Crown copyright and database rights 2016 and Geomni UK Map data © and database rights [2019]")

def handle_message(update, context):
    message = update.message.text
    if message.startswith('time') or message.startswith('Time'):
        station = str(message).replace("time ", "", 1).replace("Time ", "", 1)
        replaced = replaceStop(station)
        thisdict = {}
        searchResponse = requests.get("https://api.tfl.gov.uk/StopPoint/Search?query=" + replaced).json()
        if searchResponse["total"] == 0:
            update.message.reply_text(str(station + " not found"))
            return
        id = searchResponse["matches"][0]["id"]
        name = searchResponse["matches"][0]["name"]
        lineResponse = requests.get("https://api.tfl.gov.uk/StopPoint/" + id).json()
        line = lineResponse["lines"]
        for i in line:
            lineid = i["id"]
            arrivalResponse = requests.get("https://api.tfl.gov.uk/Line/" + str(lineid) + "/Arrivals").json()
            if arrivalResponse == []:
                tempid = str(lineid) + " - No bus in 30 mins"
                thisdict[tempid] = 2000
                # update.message.reply_text(str(name+ " - " + str(lineid) + " - " + "No bus in 30 minutes"))
            for j in arrivalResponse:
                if j["stationName"] == name:
                    tempid = str(str(int(j["timeToStation"]/60)).replace(".",":") + " min(s): " + str(j["lineName"]).upper() + " --> " + j["destinationName"])
                    thisdict[tempid] = j["timeToStation"]
                    # update.message.reply_text(str(j["stationName"] + " - " + j["lineName"] + " --> " + j["destinationName"] + " : " + str(int(j["timeToStation"]/60)).replace(".",":") + " min"))
        marklist = sorted(thisdict.items(), key=lambda x:x[1])
        sortdict = dict(marklist)
        keys = sortdict.keys()
        for i in keys:
            update.message.reply_text(i)

    elif message.startswith('stop') or message.startswith('Stop'):
        station = str(message).replace("stop ", "", 1).replace("Stop ", "", 1)
        replaced = replaceStop(station)
        thatdict = {}
        searchResponse = requests.get("https://api.tfl.gov.uk/StopPoint/Search?query=" + replaced).json()
        if searchResponse["total"] == 0:
            update.message.reply_text(str(station + " not found"))
            return
        id = searchResponse["matches"][0]["id"]
        lineResponse = requests.get("https://api.tfl.gov.uk/StopPoint/" + id).json()
        line = lineResponse["lines"]
        for i in line:
            lineid = str(i["id"])
            route = requests.get("https://api.tfl.gov.uk/Line/" + lineid + "/Route").json()
            sections = route["routeSections"]
            for j in sections:
                tempid2 = str(str(lineid).capitalize() + ": " + str(j["originationName"]) + " --> " + str(j["destinationName"]) + " (" + str(j["direction"]).capitalize() + ")")
                if lineid != "avanti-west-coast" and lineid != 'bakerloo' and lineid != "northern" and lineid != "c2c" and lineid != "victoria" and lineid != "circle" and lineid != "central" and lineid != "district" and lineid != "jubilee" and lineid != "great-western-railway" and lineid != "great-northern" and lineid != "cross-country" and lineid != "city-cruises" and lineid != "chiltern-railways" and lineid != "east-midlands-railway" and lineid != "greater-anglia" and lineid != "emirates-air-line" and lineid != "first-hull-trains" and lineid != "grand-central" and lineid != "gatwick-express" and lineid != "first-transpennine-express" and lineid != "metropolitan" and lineid != "piccadilly" and lineid != "waterloo-city" and lineid != "hammersmith-city" and lineid != "dlr" and lineid != "west-midlands-trains" and lineid != "woolwich-ferry" and lineid != "transport-for-wales" and lineid != "tram" and lineid != "thames-river-services" and lineid != "thameslink" and lineid != "tfl-rail" and lineid != "south-western-railway" and lineid != "southern" and lineid != "southeastern" and lineid != "scotrail" and lineid != "rb6" and lineid != "rb5" and lineid != "rb4" and lineid != "rb3" and lineid != "rb2" and lineid != "rb1" and lineid != "northern-rail" and lineid != "merseyrail" and lineid != "london-overground" and lineid !="london-north-eastern-railway" and lineid != "island-line" and lineid != "heathrow-express":
                    if re.search('a|b|c|d|el|e|g|h|k|p|n|r|s|u|w|x', lineid):
                        if lineid.startswith('el'):
                            lineid2 = lineid.replace('el','el00')
                        elif len(lineid) < 3:
                            for i in string.ascii_lowercase:
                                lineid2 = lineid.replace(i,i+'00')
                        elif len(lineid) < 4:
                            for i in string.ascii_lowercase:
                                lineid2 = lineid.replace(i,i+'0')
                        else:
                            lineid2 = lineid
                    else:
                        lineid2 = lineid
                    key = int(lineid2.replace('a','100').replace('b','101').replace('c','102').replace('d','103').replace('el','105').replace('e','104').replace('g','106').replace('h','107').replace('k','108').replace('n','109').replace('p','110').replace('r','111').replace('s','112').replace('u','113').replace('w','114').replace('x','115'))
                    thatdict[tempid2] = key
        marklist = sorted(thatdict.items(), key=lambda x:x[1])
        sortdict = dict(marklist)
        keys = sortdict.keys()
        for i in keys:
            update.message.reply_text(i)

    elif message.startswith('outbound') or message.startswith('Outbound'):
        route = str(message).replace("outbound ", "", 1).replace("Outbound ", "", 1)
        outbound = requests.get("https://api.tfl.gov.uk/Line/" + str(route) + "/Route/Sequence/Outbound")
        if outbound.status_code == 404:
            update.message.reply_text("Route " + route + " not found")
        else:
            outbound = outbound.json()
            update.message.reply_text("Start of route " + route + " (Outbound)")
            stations = outbound["stopPointSequences"][0]["stopPoint"]
            j = 1
            for i in stations:
                update.message.reply_text(" " + str(j) + ". " + i["name"])
                j = j + 1
            update.message.reply_text("End of route " + route + " (Outbound)")

    elif message.startswith('inbound') or message.startswith('Inbound'):
        route = str(message).replace("inbound ", "", 1).replace("Inbound ", "", 1)
        inbound = requests.get("https://api.tfl.gov.uk/Line/" + str(route) + "/Route/Sequence/Inbound")
        if inbound.status_code == 404:
            update.message.reply_text("Route " + route + " not found")
        else:
            inbound = inbound.json()
            update.message.reply_text("Start of route " + route + " (Inbound)")
            stations = inbound["stopPointSequences"][0]["stopPoint"]
            j = 1
            for i in stations:
                update.message.reply_text(" " + str(j) + ". " + i["name"])
                j = j + 1
            update.message.reply_text("End of route " + route + " (Inbound)")
    
    elif message.startswith('route') or message.startswith('Route'):
        route = str(message).replace("route ", "", 1).replace("Route ", "", 1)
        response = requests.get("https://api.tfl.gov.uk/line/" + route +"/route")
        if response.status_code == 404:
            update.message.reply_text("Route " + str(route).upper() + " not found")
        else:
            response = response.json()
            routes = response["routeSections"]
            for i in routes:
                update.message.reply_text(str(route).upper() + " (" + str(i["direction"]).capitalize() + ") : " + i["originationName"] + " --> " + i["destinationName"])
                update.message.reply_text("For more information about the route, use '" + str(i["direction"]).capitalize() + " " + route + "'")
    elif message.startswith('map') or message.startswith('Map'):
        station = str(message).replace("map ", "", 1).replace("Map ", "", 1)
        replaced = replaceStop(station)
        searchResponse = requests.get("https://api.tfl.gov.uk/StopPoint/Search?query=" + replaced).json()
        if searchResponse["total"] == 0:
            update.message.reply_text(str(station + " not found"))
        else:
            lat = str(searchResponse["matches"][0]["lat"])
            long = str(searchResponse["matches"][0]["lon"])
            update.message.reply_text("https://www.google.com/maps/search/" + lat + "," + long)
    else:
        update.message.reply_text("Not a valid command")
                
keep_alive()
updater = telegram.ext.Updater(os.environ['ID'], use_context=True)
disp = updater.dispatcher

disp.add_handler(telegram.ext.CommandHandler("start", start))
disp.add_handler(telegram.ext.CommandHandler("help", help))
disp.add_handler(telegram.ext.CommandHandler("about", about))
disp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))

updater.start_polling()
updater.idle()
