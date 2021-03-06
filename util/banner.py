from colorama import Fore, Back, Style


def printBanner():
    print(Fore.LIGHTGREEN_EX + '''                                                                     
     @@@@@@   @@@       @@@            @@@   @@@@@@@@  @@@  @@@  @@@@@@@@  @@@@@@@@  
    @@@@@@@@  @@@       @@@           @@@@   @@@@@@@@  @@@  @@@  @@@@@@@@  @@@@@@@@  
    @@!  @@@  @@!       @@!          @@!@!   @@!       @@!  @@@       @@!       @@!  
    !@!  @!@  !@!       !@!         !@!!@!   !@!       !@!  @!@      !@!       !@!   
    @!@!@!@!  @!!       @!!        @!! @!!   @!!!:!    @!@  !@!     @!!       @!!    
    !!!@!!!!  !!!       !!!       !!!  !@!   !!!!!:    !@!  !!!    !!!       !!!     
    !!:  !!!  !!:       !!:       :!!:!:!!:  !!:       !!:  !!!   !!:       !!:      
    :!:  !:!   :!:       :!:      !:::!!:::  :!:       :!:  !:!  :!:       :!:       
    ::   :::   :: ::::   :: ::::       :::    ::       ::::: ::   :: ::::   :: ::::  
    :   : :  : :: : :  : :: : :       :::    :         : :  :   : :: : :  : :: : : 
    
    Good for api's and tea...
    ''' + Fore.RESET)


def printHelp():
    print(Fore.LIGHTGREEN_EX+'''

    ###############################################################################
    |                                                                             |
    |                            One 4 Fuzz help page                             |
    |                            --------------------                             |
    |                                                                             |
    |   -u, --url              Target url, must have http or https                |
    |   -l, --limit            Request 'per second' limit to send, minimun of 1   |
    |   -L, --limit-ph         Limit request per host                             |
    |   -f, --filter           Filtered request response, default 404             |
    |   -e, --error            Error message in request body                      |
    |   -R                     Print the request body                             |
    |   -i, --start-index      Wordlist start index, in case of connection error  |
    |   -w, --wordlist         Wordlist location                                  |
    |   -m, --method           Request method GET, POST, OPTION, PUT, PATCH, HEAD |
    |                          ps: GET is the default method                      |
    |   --output               File output                                        |
    |                                                                             |
    ###############################################################################  


    Examples
    > all4fuzz -u https://site.com/*F* -w ~/wordlist.txt -m GET -l 20
    > all4fuzz -u https://site.com/api/v1/*F* -w ~/wordlist.txt -m POST -l 100 -R -e "Not Found"
    
    '''+Fore.RESET)
