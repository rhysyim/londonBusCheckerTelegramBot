import os
import telegram.ext
import requests
from keep_alive import keep_alive

ID = os.environ['ID']

def replaceStop(stop):
    return str(stop).replace(' dr', ' drive').replace(' rd', ' road').replace(' stn',' station').replace(' str', ' street').replace(' blvd', ' boulevard').replace(' ln',' lane').replace(' stn',' station').replace(' av',' avenue')

def start(update, context):
    update.message.reply_text("Welcome to LondonBusChecker Telegram Bot")

def help(update, context):
    update.message.reply_text("Use 'route' to search for a line (e.g. route 1)\nUse 'time' for arrivals at a stop in the coming 30 minutes (e.g. time New Oxford Street)\nUse 'stop' to search for lines stopping at a stop (e.g. stop New Oxford Street)")

def handle_message(update, context):
    message = update.message.text
    if message.startswith('time'):
        station = str(message).replace("time ", "")
        replaced = replaceStop(station)
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
                update.message.reply_text(str(name+ " - " + str(lineid) + " - " + "No bus in 30 minutes"))
            for j in arrivalResponse:
                if j["stationName"] == name:
                    update.message.reply_text(str(j["stationName"] + " - " + j["lineName"] + " --> " + j["destinationName"] + " : " + str(int(j["timeToStation"]/60)).replace(".",":") + " min"))
    
    if message.startswith('stop'):
        station = str(message).replace("stop ", "")
        replaced = replaceStop(station)
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
                update.message.reply_text(str(str(lineid).capitalize() + ": " + str(j["originationName"]) + " --> " + str(j["destinationName"]) + " (" + str(j["direction"]).capitalize() + ")"))
    
    if message.startswith('outbound'):
        route = str(message).replace("outbound ", "")
        outbound = requests.get("https://api.tfl.gov.uk/Line/" + str(route) + "/Route/Sequence/Outbound").json()
        update.message.reply_text("Outbound")
        stations = outbound["stopPointSequences"][0]["stopPoint"]
        j = 1
        for i in stations:
            update.message.reply_text(" " + str(j) + ". " + i["name"])
            j = j + 1

    if message.startswith('inbound'):
        route = str(message).replace("inbound ", "")
        outbound = requests.get("https://api.tfl.gov.uk/Line/" + str(route) + "/Route/Sequence/Inbound").json()
        update.message.reply_text("Inbound")
        stations = outbound["stopPointSequences"][0]["stopPoint"]
        j = 1
        for i in stations:
            update.message.reply_text(" " + str(j) + ". " + i["name"])
            j = j + 1
    
    if message.startswith('route'):
        route = str(message).replace("route ", "")
        response = requests.get("https://api.tfl.gov.uk/line/" + route +"/route").json()
        routes = response["routeSections"]
        for i in routes:
            update.message.reply_text(route + " (" + i["direction"] + ") : " + i["originationName"] + " --> " + i["destinationName"])
            update.message.reply_text("For more information about the route, use '" + i["direction"] + " " + route + "'")

keep_alive()
updater = telegram.ext.Updater(ID, use_context=True)
disp = updater.dispatcher

disp.add_handler(telegram.ext.CommandHandler("start", start))
disp.add_handler(telegram.ext.CommandHandler("help", help))
disp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))

updater.start_polling()
updater.idle()
