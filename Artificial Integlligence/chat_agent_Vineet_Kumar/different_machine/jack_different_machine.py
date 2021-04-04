from chat_agent import *

if __name__ == "__main__":

    #jack->laptop
    #jill->mobile
    jack_aid = get_aid(name = 'jack', IP = '192.168.0.111', port = 30000)
    jill_aid = get_aid(name = 'jill', IP = '192.168.0.106', port = 30001)

    jack = ChatAgent(jack_aid, receiver_agent = jill_aid, start = True)
    # jill = ChatAgent(jill_aid, receiver_agent = jack_aid)

    agents = [jack]

    start_loop(agents)