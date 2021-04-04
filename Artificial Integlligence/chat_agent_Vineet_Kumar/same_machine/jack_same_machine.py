from chat_agent import *

if __name__ == "__main__":

    jack_aid = get_aid(name = 'jack', IP = 'localhost', port = 30000)
    jill_aid = get_aid(name = 'jill', IP = 'localhost', port = 30001)

    jack = ChatAgent(jack_aid, receiver_agent = jill_aid, start = True)
    # jill = ChatAgent(jill_aid, receiver_agent = jack_aid)

    agents = [jack]

    start_loop(agents)