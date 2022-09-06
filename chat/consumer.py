
############################################
from channels.consumer import AsyncConsumer
from accounts.models import Account
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

        
        if not msg:
            print('no messagess-------------')
            return False
            
        send_by_user = await self.get_user_object(send_by_id)
        send_to_user = await self.get_user_object(send_to_id)
        if not send_by_user:
            print('not send by user is available')
        if not send_to_user:
            print('not send to user available') 
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
            'send_by': self_user.id
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

# class ChatConsumer(AsyncWebsocketConsumer):
    
#     async def connect(self):
#         print('connection is accepted')
#         user = self.scope['user']
#         chat_room = f'user_chatroom_{user.id}'
#         self.room_chat_group = chat_room
#         await self.accept()
        
#         await self.channel_layer.group_add(
#             # he gave simple chat_room
#             self.room_chat_group,
#             self.channel_name
#         )    
            
#     async def receive(self,text_data):
        
#         recieved_data = json.loads(text_data)
#         message = recieved_data.get('message')
#         send_by_id = recieved_data.get('send_by')
#         send_to_id = recieved_data.get('send_to')
        
#         if not message:
#             print('empty messages ........................')
#             return False
            
#         send_by_user = await self.get_user_object(send_by_id)
#         send_to_user = await self.get_user_object(send_to_id)
        
#         if not send_by_user:
#             print('not send by user is available')
#         if not send_to_user:
#             print('not send to user available')
            
#         # this group for other user, not the registerd user
#         # to whom we need to send the messages
#         other_user_chat_room = f'user_chatroom_{send_to_id}'
#         # who is loged in rightnow
#         self_user = self.scope['user']
        
#         # we need to send two copies of message, one message is who send the message
#         # second one is whoe receive the message
        
#         response = json.dumps({
#             'message': message,
#             'send_by': self_user.id
#         })
#         # now we will call the channel layer to send the messages
#         # on copy to the other user
#         # await self.channel_layer.group_send(
#         #     other_user_chat_room,
#         #     {
#         #         'type': 'chat_message',
#         #         'text': response
#         #     }
#         # )
#         # one copy to the send by user
#         await self.channel_layer.group_send(
#             self.room_chat_group,
#             {
#                 'type': 'chat_message',
#                 'text': response
#             }
#         )
        
        
#         # await self.send(response)
          
#     async def chat_message(self,message):
#         print(message,'))))))))))))))))))))))))))))))))))))))))))))))))))))))')
#         tester = message['text']
#         print(tester, 'send to the user__________________')
#         await self.send(tester)
        
        
        
#     async def disconnect(self, message):
#         await self.channel_layer.group_discard(
#             self.room_chat_group,
#             self.channel_name
#         )
        
    # @database_sync_to_async
    # def get_user_object(self,user_id):
    #     qs = Account.objects.filter(id=user_id)
    #     if qs.exists():
    #         obj = qs.first()
    #     else:
    #         obj = None
    #     return obj