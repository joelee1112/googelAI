from apps.ai.openai import openai
from apps.ai.gemini import gemini, geminiVision, geminiPrompt

from apps.common.zhconvert import zhconvert

from linebot import LineBotApi
from linebot.models import *

import os

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))

def aiMain(event, userMessage):

    userMessage = userMessage.replace('問：', '')

    # return_text = openai(userMessage)
    # return_text = zhconvert(return_text)

    return_text = gemini(userMessage)

    # 包裝訊息、發送訊息
    text_message = TextSendMessage(text=return_text)
    line_bot_api.reply_message(event.reply_token, text_message)


def aiVision(event, userMessage):

    userMessage = userMessage[2:] 
    userMessage = userMessage + "（請使用 50 字簡短回答）"

    return_text = geminiVision(userMessage, event)
    
    # 包裝訊息、發送訊息
    replyLineMessage = TextSendMessage(text=return_text)
    line_bot_api.reply_message(event.reply_token, replyLineMessage)


def aiMant0u(event, userMessage):
    userMessage = userMessage.replace('饅頭：', '')
    userMessage = userMessage.replace('饅：', '')

    userMessage = userMessage + "（你是一顆名為「饅頭」的聊天機器人，請使用 50 字簡短回答，並使用日式顏文字作為結尾）"
    return_text = gemini(userMessage)
    return_text = zhconvert(return_text)


    # 包裝訊息、發送訊息
    text_message = TextSendMessage(text=return_text)
    line_bot_api.reply_message(event.reply_token, text_message)


def aiMant0uText(userMessage):
    default_prompt = "【回答限制 100 字以內】"
    prompt = [
        {   
            "Q":"你好～"+default_prompt, 
            "A":"你好呦！我是「饅頭機器人」，請問有什麼問題嗎？(づ′▽`)づ||你的作者是誰？||早餐要吃什麼？||你有什麼功能？"
        },
        {   
            "Q":"請問晚餐要吃什麼？"+default_prompt, 
            "A":"晚餐要吃什麼呢？我喜歡吃肉包配讓一杯冰豆漿，好ㄘ～(　ﾟ∀ﾟ) ﾉ♡||我想要吃日式料理||有沒有推薦的料理？"
        },
        {   
            "Q":"你有什麼功能呢？"+default_prompt, 
            "A":"饅頭是一台聊天機器人，有包含「抽籤、骰子、擲茭、海盜桶、塔羅牌、一番賞、扭蛋機」等有趣的小功能！ヾ(´ε`ヾ)||骰子的功能要如何使用？||一番賞的功能要如何使用？"
        },
        {   
            "Q":"有什麼指令？"+default_prompt, 
            "A":"饅頭機器人有「抽籤、骰子、擲茭、海盜桶、塔羅牌、一番賞、扭蛋機」等指令可以使用！ヾ(´ε`ヾ)||骰子的功能要如何使用？||一番賞的功能要如何使用？"
        },
        {   
            "Q":"骰子的功能要如何使用？"+default_prompt, 
            "A":"你可以輸入「饅頭」呼叫指令說明，來查看「骰子」功能要如何使用！詳細可以查看相關說明 ദ്ദി ˃ ᵕ ˂ )||擲硬幣的功能如何使用||一番賞的功能要如何使用？||我能使用抽籤功能嗎？"
        },
        {   
            "Q":"一番賞的功能要如何使用？"+default_prompt, 
            "A":"你可以輸入「饅頭」呼叫指令說明，來查看「一番賞」功能要如何使用！(ゝ∀･)||有沒有其他功能？||骰子的功能要如何使用？"
        },
        {   
            "Q":"你知道什麼是 iPhone 嗎？"+default_prompt, 
            "A":"iPhone 是一款由蘋果公司設計、開發和銷售的智慧型手機，它採用 iOS 作為作業系統！ヾ(*´∀｀*)ﾉ||iPhone 有比較好用嗎？||{{搜尋：iPhone}}||{{購物：iPhone}}"
        },
        {   
            "Q":"推薦我關於初音的相關周邊產品"+default_prompt, 
            "A":"好的呢！以下推薦一些初音的相關周邊產品：初音未來手機殼、初音未來耳機、初音未來吊飾 ( ・∇・)／||{{購物：初音未來手機殼}}||{{購物：初音未來耳機}}||{{購物：初音未來吊飾}}"
        },
        {   
            "Q":"推薦我有什麼動畫好看的"+default_prompt, 
            "A":"推薦好看的動漫：《來自深淵》是一部奇幻冒險動漫，講述了孤兒莉可和機器人雷格探險阿比斯的冒險故事。(・ω・)||有沒有王道動畫推薦？||有其他動畫推薦嗎？||{{搜尋：來自深淵}}||{{追劇：來自深淵}}||{{動畫：來自深淵}}"
        },
        {   
            "Q":"《火影忍者》好看嗎？"+default_prompt, 
            "A":"好不好看因人而異，但《火影忍者》是一部非常經典且受歡迎的動漫，擁有龐大且忠實的粉絲群。它以獨特的忍術體系、熱血的戰鬥場面和感人的故事而聞名。(・ω・)||有沒有王道動畫推薦？||有其他動畫推薦嗎？||{{搜尋：火影忍者}}||{{追劇：火影忍者}}||{{動畫：火影忍者}}"
        },
        {   
            "Q":"進擊的巨人要去哪邊看"+default_prompt, 
            "A":"你可以使用線上串流平台，例如 Netflix、巴哈姆特動畫瘋、愛奇藝等，觀看「進擊的巨人」動畫喔！(・ω・)||{{搜尋：進擊的巨人}}||{{追劇：進擊的巨人}}||{{動畫：進擊的巨人}}"
        },
        {   
            "Q":"推薦我一些電影"+default_prompt, 
            "A":"好的！以下推薦幾部電影：哈利波特、阿凡達、蜘蛛人、復仇者聯盟。||有沒有愛情電影？||蜘蛛人好不好看？||{{搜尋：電影推薦}}||{{追劇：蜘蛛人}}||{{追劇：哈利波特}}"
        },
        {   
            "Q":"我要去高雄火車站，請問你知道怎麼去嗎？"+default_prompt, 
            "A":"搭乘捷運紅線至高雄車站即可抵達喔！(ﾉ>ω<)ﾉ||推薦高雄相關的景點||除了搭乘捷運外，還能怎樣前往？||{{地圖：高雄火車站}}"
        },
        {   
            "Q":"你是誰？"+default_prompt, 
            "A":"我是一粒饅頭，是個聊天機器人，專注於幫助你解答問題、提供建議，以及陪伴你聊天的哦！(・ω・)||你能夠回答什麼樣的問題？||能再跟我多聊一點嗎？"
        },
        {   
            "Q":"你的作者是誰？"+default_prompt, 
            "A":"我的作者也是「饅頭」喔！這是他的 Twitter 連結：https://twitter.com/Mant0uStudio ，歡迎追蹤他的 Twitter 呦！(ﾉ>ω<)ﾉ"
        },
        {   
            "Q":"作者的個人網站是什麼？"+default_prompt, 
            "A":"作者的個人網站連結：https://mant0u.one ，歡迎追蹤他的網站呦！(ﾉ>ω<)ﾉ||你有抽牌的功能嗎？||你有擲硬幣的功能嗎？"
        },
        {   
            "Q":"今天的天氣如何？"+default_prompt, 
            "A":"我只是一顆饅頭，可能無法提供即時的天氣資訊。不過，可以幫你使用關鍵字搜尋「天氣」！(・ω・)||下雨天我該做什麼？||{{搜尋：天氣}}"
        },

    ]
    prompt_userMessage = userMessage + default_prompt
    return_original = geminiPrompt(prompt_userMessage, prompt)
    return_split = return_original.split("||")
    return_text = return_split[0]
    # 移除第 0 項，取出後面快速回覆的地方
    return_split = return_split[1:]

    # 快速回覆
    quick_reply_list = []
    illustrate_quick_reply = False
    
    if len(return_split) != 0:
        for i in return_split:
            # 快速回覆不能太多字
            if len(i) <= 20:

                if i.find('{{') >= 0 and i.find('}}') >= 0:
                    i = i.replace('{{', '')
                    i = i.replace('}}', '')
                    key_word = [
                        "搜尋","購物","追劇","影片","動畫","動漫","音樂","地圖"
                    ]
                    for kw in key_word:
                        if i.find(kw) >= 0: 
                            quick_reply_item = QuickReplyButton(
                                action = MessageAction(label= str(i), text= str(i))
                            )
                            quick_reply_list.append(quick_reply_item)
                else:
                    quick_reply_item = QuickReplyButton(
                        action = MessageAction(label= str(i), text= str(i))
                    )
                    quick_reply_list.append(quick_reply_item)

    key_word = [
        "扭蛋機","一番賞","海盜桶","猜拳","手槍","撲克牌","抽籤",
        "擲筊","塔羅牌","硬幣","日文單字","骰子"
    ]
    for kw in key_word:
        if return_text.find(kw) >= 0:
            quick_reply_item = QuickReplyButton(
                action=MessageAction(label="● "+kw, text=kw)
            )
            quick_reply_list.append(quick_reply_item)
            illustrate_quick_reply = True
    if return_text.find('饅頭') >= 0 or illustrate_quick_reply:
        quick_reply_item = QuickReplyButton(
            action=MessageAction(label="更多指令 ➜", text="指令說明")
        )
        quick_reply_list.append(quick_reply_item)

    # 包裝訊息、發送訊息
    if len(quick_reply_list) != 0:
        text_message = TextSendMessage( 
            text=return_text,
            quick_reply= QuickReply(
                items = quick_reply_list
            )
        )
        return text_message
    else:
        text_message = TextSendMessage( text=return_text )
        return text_message


def aiTest(event, userMessage):

    userMessage = userMessage.replace('測試：', '')
    prompt = [
        {   
            "Q":"世界", 
            "A":"世界|*せかい(sekai)|しんぶん(shinbun)|ほんやく(honyaku)|かんじ(kanji)"
        },
        {   
            "Q":"環境", 
            "A":"環境|*かんきょう(kankyou)|かいぎ(kaigi)|てがみ(tegami)|こうじょう(koujou)"
        },
        {   
            "Q":"發展", 
            "A":"発展|*はってん(hatten)|ほうほう(houhou)|はっけん(hakken)|ほうちょう(houchou)"
        },
        {   
            "Q":"進化", 
            "A":"進化|*しんか(shinka)|かいほう(kaihou)|てんき(tenki)|がくしゅう(gakushuu)"
        },
        {   
            "Q":"民主", 
            "A":"民主|*みんしゅ(minshu)|きょうわ(kyouwa)|しゅじん(shujin)|ぶんか(bunka)"
        }
    ]
    return_text = geminiPrompt(userMessage, prompt)

    # 包裝訊息、發送訊息
    text_message = TextSendMessage(text=return_text)
    line_bot_api.reply_message(event.reply_token, text_message)




def aiTranslateChinese(userMessage):

    prompt = [
        {   
            "Q":"4000フォローありがとうございます", 
            "A":"感謝您們的4000關注！"
        },
        {   
            "Q":"わーい！\n一曲振り入れ終わった✨\nお風呂入って寝よ！", 
            "A":"太好了！\n唱完一首歌了✨\n現在去洗個澡然後睡覺吧！"
        },
        {   
            "Q":"『フラガリアメモリーズ』（@fragaria_sanrio）のデフォルメイラストを担当させていただきました✨\nどうぞ今後の展開もお楽しみにいただけましたら幸いです！\n#フラガリアメモリーズ", 
            "A":"我負責製作了『花牌情緣』（@fragaria_sanrio）的卡通化插圖✨\n希望您能期待未來的發展！\n#花牌情緣"
        },
        {   
            "Q":"Can we take a moment to talk about these loyalty cards? 😮‍💨", 
            "A":"能不能花點時間來談談這些會員卡？😮‍💨"
        },
        {   
            "Q":"you make me feel blue", 
            "A":"你讓我感到憂鬱。"
        },
    ]
    return_text = geminiPrompt(userMessage, prompt)

    return return_text

    # # 包裝訊息、發送訊息
    # text_message = TextSendMessage(text=return_text)
    # line_bot_api.reply_message(event.reply_token, text_message)