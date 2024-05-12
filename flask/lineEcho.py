from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
from linebot.v3.webhooks import MessageEvent, TextMessageContent

# 將載入的flask模組實例化，即建立了flask伺服器
app = Flask(__name__)


# 設定 Channel access token 及 Channel secret
configuration = Configuration(access_token='Channel_access_token')
handler = WebhookHandler('Channel_secret')
# 或
# parser = linebot.v3.WebhookParser('YOUR_CHANNEL_SECRET')


# 建立 callback 路由，接 POST 需求
# 檢查LINE Bot 的資料是否正確
# 記得在 Webhook URL 網址後面加上 "/callback"
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line_Signature']
    
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    try:
        # 丟到 handler 去處理訊息
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'



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


# If there is no handler for an event,
# this default handler method is called.
@handler.default()
def default(event):
    print("這是 default handler method.")


if __name__=='__main__':
    app.run()
    # 加入 debug=True 開啟除錯模式，
    # 好處是當程式執行期間，您對程式內容的任何修改都會及時讓開啟的服務更新