from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
from pade.acl.messages import ACLMessage

class ChatAgent(Agent):
    def __init__(self, aid, receiver_agent, start = False):
        super().__init__(aid)
        self.receiver_agent = receiver_agent
        self.start = start

    def react(self, message):
        super().react(message)
        display_message(message.sender.localname, message.content)
        self.receiver_agent = message.sender
        print('-'*50)
        self.send_message()

    def on_start(self):
        if self.start:
            # print(self.aid.localname)
            super().on_start()
            self.send_message()

    def send_message(self):
        # print('Test')
        message = ACLMessage(ACLMessage.INFORM)
        message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        message.add_receiver(self.receiver_agent)
        self.agentInstance.table[self.receiver_agent.localname] = self.receiver_agent
        
        temp = input("Enter your message: ")
        print('-'*50)
        message.set_content(temp)
        self.send(message)


def get_aid(name, IP, port):
    _name = f'{name}@{IP}:{port}'
    return AID(name = _name)

