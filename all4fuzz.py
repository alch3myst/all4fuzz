import aiohttp
import asyncio
import warnings
import sys
import util.helpers as h
import util.banner as banner
import getopt
import json

#
# Don't look here it's ugly ;o
#

# Init
warnings.filterwarnings('ignore')  # R.I.P anoyng warnings
_limit = 10  # default rps
_limit_per_host = 0  # default conections per host 0 = unlimited
data = ''  # sintax "{'parameter': *F*}"
HEADERS = '' # sintax "{'header': 'name'}"
COOKIES = '' # sintax "{'cookie': 'value'}"
err_message = '*all4fuzz love u :D´*'  # error displayed in request [wip]
print_request = False  # print the request body, userfull for api fuzzing
_status = 404  # Default request filter
start_index = 0  # the wordlist start index
proxy = None  # the wordlist start index
output = False

# Args definition
try:
    # Define options u, w, h
    options, remainder = getopt.gnu_getopt(
        sys.argv[1:],  # terminal arguments
        'u:w:l:L:f:hm:de:Ri:H:p:c:',  # Shotr options
        [  # Long arguments
            'url=',
            'wordlist=',
            'limit=',
            'limit-ph=',
            'filter=',
            'method=',
            'data=',
            'error=',
            'start-index=',
            'output=',
            'headers=',
            'cookies=',
            'proxy='
        ])
# Catch errors from malformed input
except getopt.GetoptError as err:
    print('Nope, ', err)
    sys.exit(1)

# set the variables with arguments values
for opt, arg in options:
    # Define URL
    if opt in ('-u', '--url'):
        url = arg

    # Define Data to send
    elif opt in ('-d', '--data'):
        data = json.loads(str(arg).replace("'", '"'))
    
    # Define Cookies to send
    elif opt in ('-c', '--cookies'):
        COOKIES = json.loads(str(arg).replace("'", '"'))

    # Define Data to send
    elif opt in ('-p', '--proxy'):
        data = str(arg)

    # Request limit
    elif opt in ('-l', '--limit'):
        _limit = int(arg)

    # Request limit per host
    elif opt in ('-L', '--limit-per-host'):
        _limit_per_host = int(arg)

    # Filter requests
    elif opt in ('-f', '--filter'):
        _status = int(arg)

    # Filter requests
    elif opt in ('-e', '--error'):
        err_message = arg

    elif opt == '-R':
        print_request = True

    # Start index
    elif opt in ('-i', '--start-index'):
        start_index = int(arg)

    # Start index
    elif opt in ('-H', '--headers'):
        HEADERS = json.loads(str(arg).replace("'", '"'))

    # Output file
    elif opt == '--output':
        output = arg

    # Return the help text
    elif opt in ('-h', '--help'):
        banner.printBanner()
        banner.printHelp()
        sys.exit(2)

# Work around not geting the correct index
# it's ugly, but work c:
for opt, arg in options:
    # Define wordlist path
    if opt in ('-w', '--wordlist'):
        # Create array from file
        wordlist, wordlist_length = h.loadWordlist(arg, start_index)

# Init network stuff
loop = asyncio.get_event_loop()  # create the main loop event
# Create a tcp connector with limit and all the good stuff
tcp = aiohttp.TCPConnector(
    limit=_limit, limit_per_host=_limit_per_host, loop=loop)
# Make a session using the new tcp config
session = aiohttp.ClientSession(connector=tcp)

# Default method
method = session.get

# Request method
for opt, arg in options:
    # Define request method
    if opt in ('-m', '--method'):
        if arg == 'POST':
            method = session.post
        elif arg == 'GET':
            method = session.get
        elif arg == 'OPTION':
            method = session.options
        elif arg == 'PUT':
            method = session.put
        elif arg == 'PATCH':
            method = session.patch
        elif arg == 'HEAD':
            method = session.head
        else:
            loop.run_until_complete(asyncio.sleep(0.300))
            tcp.close()
            print('\nWtf is ' + arg + '??\n')
            sys.exit(7)


# Main Function
async def api(param):
    try:
        # make the request
        async with method(url.replace('*F*', param), proxy=proxy, data=data, headers=HEADERS, cookies=COOKIES) as res:
            # Count variable acess and increment
            global i
            i += 1

            # Fast as f boy
            if res.status == 429:
                tcp.close()
                print('Too fast for this server, u got a 429 :l  ')
                sys.exit(3)

            # get the response body
            r = await res.text()

            if res.status != _status and err_message not in r:
                # print the requested url
                print(template.format('# URL ', url.replace('*F*', param), ' Status  ' + str(res.status)))

                # if -R print the request body
                print('- Response: ' + r + '  ') if print_request == True else False

                # Open the output file
                if output != False:
                    out.write(template.format('# URL ', url.replace('*F*', param), ' Status  ' + str(res.status))+'\n')
                    out.write('- Response: ' + r + '  \n') if print_request == True else False

            # print the current request and keep it in line, a little bit buggy :l
            sys.stdout.write('Trying: ' + '[' + str(i) + '/' + str(
                wordlist_length) + '] ' + url.replace('*F*', param) + ' '*10 + '\r')
            sys.stdout.flush()

    # Catch connection erros, ssl errors etc...
    except aiohttp.ClientConnectionError:
        pass
    except UnicodeError as e:
        print('Last Index: ' + '[' + str(i) + '/' + str(wordlist_length) + '] ' + url.replace('*F*', param) + ' '*10 + '\r')
        print(' Unicode error: label empty or too long')
        pass
    # Catch any other exception and print it
    except:
        # Save the output file
        if output != False:
            out.close()
        print(e)

# Starter
try:
    # Banner & info
    banner.printBanner()
    template = "{0:5}{1:40}{2:5}"
    # Table info
    print('\nTotal atempts: ' + str(wordlist_length)+'\n')
    # print('-'*60)
    # print(template.format('| URL |', '', '| Status |'))
    # print('-'*60)

    # Progress count
    i = start_index

    # Open the output file
    if output != False:
        out = open(output, 'a')

    # Main loop initialize
    loop.run_until_complete(
        asyncio.gather(*(api(param) for param in wordlist))
    )

    # Save the output file
    if output != False:
        out.close()

    # Info
    print('\nClosing connections...')
    # sleep the connections for 300ms
    loop.run_until_complete(asyncio.sleep(0.300))
    # close connections
    tcp.close()
except KeyboardInterrupt:
    # Save the output file
    if output != False:
        out.close()
    # Message for CRTL+C cancelation
    print('\n\nCTRL+C huummm\n')
    sys.exit(1)
except:
    print('Last Index: ' + '[' + str(i) + '/' + str(wordlist_length) + '] ' + url + ' '*10 + '\r')
    print("Some other error")
    sys.exit(9)
