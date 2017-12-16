# -*- coding: utf-8 -*-

# Copyright (c) 2016 Jeremy Low
# License: MIT


try:
    import oauth as Oauth
    from twitter import Twitter
    import turtle
    import twitter
    import json
    import sys
    from time import sleep
except ImportError as whoops:
    print("Sorry, one of the required packages did not import properly. try running pip install with the package name", str(whoops))
    # sleep(8) # display error message so they can gather the needed info, can add in logging, and log it to a file.
    # sys.exit(1) # because of error with importing, set exit status as 1 because of an error.

turtle.hideturtle()
screen = turtle.Screen() # setting up screen ratio's
screen.setup(1000,1000)
# screen.background('White') # can be changed to a background picture with screen.bgpic('')

print('Please be aware, none of this information will be shared with anyone,\n'
        'this is to help you unblock your access to twitter.\n'
        'AND WILL ONLY BE USED FOR THAT PURPOSE.\n'
        'this message will display for 15 seconds.') # for the non tech savy.
turtle.write("Please refer to the floating black window AKA(Terminal,Console,etc)",
             False, align='center', font=('Arial', 12, 'bold')) # disclaimer text, alignement, and text def.
sleep(15) # display the message for 15 seconds.
turtle.clear()

# switched to TextInput, to solve an error generated by turtles default Floating point number.
CONSUMER_KEY = turtle.textinput("CONSUMER KEY", "Enter or copy your Consumer key please!")
CONSUMER_SECRET = turtle.textinput("CONSUMER SECRET", "Enter your consumer secret key please!")
ACCESS_KEY = turtle.textinput("ACCESS KEY","Enter your access key please!")
ACCESS_SECRET = turtle.textinput("ACCESS SECRET","Please enter your Access Secret Key please!")

# debugging purposes.
print(CONSUMER_KEY)
print(CONSUMER_SECRET)
print(ACCESS_KEY)
print(ACCESS_SECRET)

# convert to int, see if that cleans up some of this and makes it passable to OAuth.
CONSUMER_KEY = int(CONSUMER_KEY)
CONSUMER_SECRET = int(CONSUMER_SECRET)
ACCESS_KEY = int(ACCESS_KEY)
ACCESS_SECRET = int(ACCESS_SECRET)

# debugging purposes.
print(CONSUMER_KEY)
print(CONSUMER_SECRET)
print(ACCESS_KEY)
print(ACCESS_SECRET)

# inside this call, im not exactly sure if they can be passed as a string, or as an int, so i figured for ease of use,
# set as string and if it fails handle as necessary.
api = twitter.Api(CONSUMER_KEY,
                  CONSUMER_SECRET,
                  ACCESS_KEY,
                  ACCESS_SECRET,
                  tweet_mode='extended',
                  sleep_on_rate_limit=True))


def get_blocks(filename):
    with open(filename, 'w+') as f:
        blocks = api.GetBlocksIDs()
        f.write(json.dumps(blocks))
    return True


def unblock(blocklist):
    with open(blocklist, 'r') as f:
        blocks = json.loads(f.read())
    while blocks:
        block = str(blocks.pop())
        try:
            result = api.DestroyBlock(user_id=block)
            if result:
                with open('successfully_unblocked.txt', 'a+') as unblocked_list:
                    unblocked_list.write(block + '\n')
        except Exception as e:
            with open('errors.txt', 'a+') as error_log:
                error_log.write(repr(e) + '\n')
            with open('faied_to_unblock.txt', 'a+') as fail_list:
                fail_list.write(block + '\n')
            continue
        with open(blocklist, 'w+') as f:
            f.write(json.dumps(blocks))


if __name__ == '__main__':
    if get_blocks('blocklist.json'):
        unblock('blocklist.json')
