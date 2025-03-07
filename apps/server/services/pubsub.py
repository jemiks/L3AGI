import sentry_sdk
from typing import Dict, Optional, Any
from azure.messaging.webpubsubservice import WebPubSubServiceClient
from azure.core.exceptions import AzureError
from azure.identity import DefaultAzureCredential
from config import Config
from typings.user import UserOutput


class AzurePubSubService:
    def __init__(self):
        self.credential = DefaultAzureCredential()
        self.service = WebPubSubServiceClient.from_connection_string(Config.AZURE_PUBSUB_CONNECTION_STRING, hub=Config.AZURE_PUBSUB_HUB_NAME)

    def send_to_group(self, group: str, message: Any):
        """Sends pubsub message to group"""

        try:
            self.service.send_to_group(group=group, content_type="application/json", message=message)
        except AzureError as err:
            sentry_sdk.capture_exception(err)

    def get_client_access_token(self, user_id):
        """Gets a client access token for the given user_id"""

        try:
            response = self.service.get_client_access_token(
                user_id=user_id,
                roles=["webpubsub.sendToGroup", "webpubsub.joinLeaveGroup"]
            )
            return response
        except AzureError as err:
            sentry_sdk.capture_exception(err)



class ChatPubSubService:
    def __init__(self, session_id: str, user: UserOutput, is_private_chat: bool, team_id: Optional[str] = None, agent_id: Optional[str] = None):
        self.session_id = session_id
        self.user = user
        self.team_id = team_id
        self.agent_id = agent_id
        self.is_private_chat = is_private_chat
        
        self.azure_pubsub_service = AzurePubSubService()

    def send_chat_message(self, chat_message: Dict, local_chat_message_ref_id: Optional[str] = None):
        """Sends chat message object"""

        self.azure_pubsub_service.send_to_group(self.session_id, message={
            'type': 'CHAT_MESSAGE_ADDED',
            'from': str(self.user.id),
            'chat_message': chat_message,
            'is_private_chat': self.is_private_chat,
            'local_chat_message_ref_id': local_chat_message_ref_id,
            'agent_id': self.agent_id,
            'team_id': self.team_id,
        })