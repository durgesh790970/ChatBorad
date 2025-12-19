"""
Django Channels WebSocket consumer for real-time chat.
"""
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for handling real-time chat messages.
    """

    async def connect(self):
        """
        Called when a WebSocket connection is established.
        """
        try:
            self.user = self.scope['user']
            self.other_user_id = self.scope['url_route']['kwargs']['user_id']
            self.room_name = self.get_room_name(self.user.id, int(self.other_user_id))
            self.room_group_name = f'chat_{self.room_name}'

            print(f'✅ WebSocket connecting: User={self.user}, Other User ID={self.other_user_id}, Room={self.room_group_name}')

            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()
            print(f'✅ WebSocket connection accepted for room: {self.room_group_name}')
        except Exception as e:
            print(f'❌ Connection error: {e}')
            await self.close()

    async def disconnect(self, close_code):
        """
        Called when a WebSocket connection is closed.
        """
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Called when the WebSocket receives a message from the client.
        """
        try:
            print(f'📨 WebSocket message received: {text_data}')
            data = json.loads(text_data)
            message_text = data.get('message', '').strip()

            if not message_text:
                print('⚠️ Empty message received, ignoring')
                return

            print(f'💬 Processing message: {message_text}')

            # Save message to database
            try:
                receiver = await self.get_user(int(self.other_user_id))
                if not receiver:
                    error_msg = f'Receiver not found: {self.other_user_id}'
                    print(f'❌ {error_msg}')
                    await self.send(text_data=json.dumps({
                        'error': error_msg
                    }))
                    return

                print(f'✅ Receiver found: {receiver.username}')

                # Create message in database
                message = await self.create_message(
                    self.user,
                    receiver,
                    message_text
                )
                
                print(f'✅ Message saved to DB: ID={message.id}')

                # Broadcast message to room group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message_id': str(message.id),
                        'sender_id': message.sender.id,
                        'sender_username': message.sender.username,
                        'receiver_id': message.receiver.id,
                        'receiver_username': message.receiver.username,
                        'message': message.message_text,
                        'timestamp': message.timestamp.isoformat(),
                    }
                )
                print(f'✅ Message broadcasted to room: {self.room_group_name}')
                
            except Exception as e:
                error_msg = f'Error processing message: {str(e)}'
                print(f'❌ {error_msg}')
                import traceback
                traceback.print_exc()
                await self.send(text_data=json.dumps({
                    'error': error_msg
                }))

        except json.JSONDecodeError as e:
            error_msg = f'Invalid JSON format: {str(e)}'
            print(f'❌ {error_msg}')
            await self.send(text_data=json.dumps({
                'error': error_msg
            }))
        except Exception as e:
            error_msg = f'Unexpected error: {str(e)}'
            print(f'❌ {error_msg}')
            import traceback
            traceback.print_exc()
            await self.send(text_data=json.dumps({
                'error': error_msg
            }))

    async def chat_message(self, event):
        """
        Called when a message is sent to the room group.
        Forwards the message to the WebSocket.
        """
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message_id': event['message_id'],
            'sender_id': event['sender_id'],
            'sender_username': event['sender_username'],
            'receiver_id': event['receiver_id'],
            'receiver_username': event['receiver_username'],
            'message': event['message'],
            'timestamp': event['timestamp'],
        }))

    @staticmethod
    def get_room_name(user_id1, user_id2):
        """Generate a unique room name for two users"""
        ids = sorted([user_id1, user_id2])
        return f"{ids[0]}_{ids[1]}"

    @staticmethod
    async def get_user(user_id):
        """Fetch user from database asynchronously"""
        def fetch_user():
            try:
                return User.objects.get(id=user_id)
            except User.DoesNotExist:
                return None
        
        return await database_sync_to_async(fetch_user)()

    @staticmethod
    async def create_message(sender, receiver, message_text):
        """Create message in database asynchronously"""
        def save_message():
            return Message.objects.create(
                sender=sender,
                receiver=receiver,
                message_text=message_text
            )

        return await database_sync_to_async(save_message)()
