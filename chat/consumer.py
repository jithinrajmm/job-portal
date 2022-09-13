
############################################
from channels.consumer import AsyncConsumer
from accounts.models import Account
from chat.models import Thread,ChatMessage
#  it can open up to one connection per thread,
# for avoiding this we can use the below decorator
from channels.db import database_sync_to_async
import json

class ChatConsumer(AsyncConsumer):
    
    async def websocket_connect(self,event):
        print('connection established...')
        user = self.scope['user']
        chat_room = f'user_chatroom_{user.id}'
        self.chat_room = chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name 
        )
        await self.send({
            'type':'websocket.accept'
        })
    async def websocket_receive(self,event):
        print('received',event)
        recieved_data = json.loads(event['text'])
        msg = recieved_data.get('message')
        send_by_id = recieved_data.get('send_by')
        send_to_id = recieved_data.get('send_to') 
        thread_id  = recieved_data.get('thread_id') 

        
        if not msg:
            print('no messagess-------------')
            return False
        # database operations    
        send_by_user = await self.get_user_object(send_by_id)
        send_to_user = await self.get_user_object(send_to_id)
        thread_obj = await self.get_thread(thread_id)
        
        if not send_by_user:
            print('not send by user is available')
        if not send_to_user:
            print('not send to user available') 
        if not thread_obj:
            print('Thread is not  available')
            
        await self.create_message(thread_obj,send_by_user,msg)
        # to whom we need to sende the messages
        other_user_chat_room = f'user_chatroom_{send_to_id}'
        
        # who loged in right now
        self_user = self.scope['user']
        # when we send the messages to the front end we need to send the information that
        # who send the purticular message, whenever the user sedn the message from the 
        # front end we need to send two copies of messages.
        # one copy to the loged in user who has send the message
        # another one is who recieve 
        response = {
            'message': msg,
            'send_by': self_user.id,
            'thread_id':thread_id,
        }
        # adding channel layer which update all the browsers
        await self.channel_layer.group_send(
            other_user_chat_room,
            {   
                # creating new event
                'type': 'chat_message',
                'text': json.dumps(response)
            }
        )
        
        await self.channel_layer.group_send(
            self.chat_room,
            {   
                # creating new event
                'type': 'chat_message',
                'text': json.dumps(response)
            }
        )
        
    async def chat_message(self,event):
        # print('chatmessage',event)
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })

        
    async def websocket_disconnect(self,event):
        print('connection is closed......')
        
    @database_sync_to_async
    def get_user_object(self,user_id):
        qs = Account.objects.filter(id=user_id)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj
        
    @database_sync_to_async
    def get_thread(self,thread_id):
        qs = Thread.objects.filter(id=thread_id)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj
        
    @database_sync_to_async
    def create_message(self,thread,user,message):
        print(thread)
        print(user)
        print(message)
        ChatMessage.objects.create(thread=thread,user=user,message=message)
        
