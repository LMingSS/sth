from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
from linebot.v3.webhooks import MessageEvent, TextMessageContent


import json
import os


# 設定 Channel access token 及 Channel secret
configuration = Configuration(access_token=os.environ['Channel_access_token'])
handler = WebhookHandler(os.environ['Channel_secret'])


def lambda_handler(event, context):
    
    # 如果接到使用者傳送的訊息，就將接到的文字訊息傳回。
    # Add a handler method by using this decorator.
    @handler.add(MessageEvent, message=TextMessageContent)
    def handle_message(event):
        print(event.message.text)
        
        with ApiClient(configuration) as api_client:
            
            line_bot_api = MessagingApi(api_client)
            
            line_bot_api.reply_message_with_http_info(
                # 回傳 User 剛剛所傳的訊息 (Echo Bot)
                ReplyMessageRequest(
                    # 每則訊息 LINE Sever 都賦予的獨特 token ，僅供觸發一次不能重複使用。
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=event.message.text)]
                )
            )
    
    # get X-Line-Signature header value
    signature = event['headers']['x-line-signature']
    
    # get request body as text
    body = event['body']
    # app.logger.info("Request body: " + body)
    
    
    try:
        # 丟到 handler 去處理訊息
        handler.handle(body, signature)
        
    except InvalidSignatureError:
        return {
            'statusCode': 400,
            'body': json.dumps("Invalid signature. Please check your channel access token/channel secret."),
            }
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
        }

