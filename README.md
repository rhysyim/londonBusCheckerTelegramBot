# londonBusCheckerTelegramBot
A Telegram bot for London buses about arrivals and bus routes.

## Usage
Go to Telegram and send /start to @londonBusChecker_bot or go to https://t.me/londonBusChecker_bot

Use /help for more information about the bot

### Commands
#### Time - Arrival times at a stop
```
Time Waterloo Bridge / South Bank

// 0 min(s): 176 --> Tottenham Court Road
// 0 min(s): 76 --> Tottenham Hale, Bus Station
// 1 min(s): 1 --> Canada Water
// 2 min(s): 59 --> Streatham Hill, Telford Avenue
```
#### Stop - Lines at a stop
```
Stop Waterloo Bridge / South Bank

// 1: Canada Water Bus Station --> Tottenham Court Road (Inbound)
// 1: New Oxford Street --> Canada Water Bus Station (Outbound)
// 26: Waterloo Station / Waterloo Road --> St Mary of Eton Church (Inbound)
// 26: St Mary of Eton Church --> Waterloo Station   / Waterloo Road (Outbound)
```
#### Inbound / Outbound - Stations of a line
```
Outbound 1

// 1. New Oxford Street
// 2. Kingsway / Holborn Station
// 3. Aldwych / Drury Lane
// 4. Waterloo Bridge / South Bank
```
#### Route - More information about a line
```
Route 1

// 1 (inbound) : Canada Water Bus Station --> Tottenham Court Road
// For more information about the route, use 'inbound 1'
```
#### Map - A Google Map link of the stop
```
Map Waterloo Bridge / South Bank

// https://www.google.com/maps/search/51.506509,-0.114864
```

- Lowercase and uppercase are accepted

## API Reference
Transport for London API - https://api-portal.tfl.gov.uk/

Telegram API - https://core.telegram.org/bots/api

## Acknowledgments
Powered by TfL Open Data

Contains OS data © Crown copyright and database rights 2016 and Geomni UK Map data © and database rights [2019]
