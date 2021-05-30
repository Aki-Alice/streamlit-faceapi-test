# 各種ライブラリのインポート
import streamlit as st
import io
import requests
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# タイトルの追加
st.title("顔認識アプリ")

# サブスクリプションキーの設定
subscription_key = "ef721e19afb345b19037541b7cc34a68"
assert subscription_key
# APIのエンドポイントの設定
face_api_url = "https://20210528akialice1018.cognitiveservices.azure.com/face/v1.0/detect"

# 画像をアップロードするエリアを作成
uploaded_file = st.file_uploader("Choose an image...", type="jpg")

# アップデートされた画像を表示する
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    # 画像をバイナリデータに変換する
    with io.BytesIO() as output:
        img.save(output, format="JPEG")
        binary_img = output.getvalue() #バイナリ取得           
    # APIを叩き、画像のパラメータを取徳後、結果をresult変数に格納
    headers = {
        "Content-Type": "application/octet-stream",
        "Ocp-Apim-Subscription-Key": subscription_key
    }
    params = {
        "returnFaceId": True,
        "returnFaceAttributes" : "age, gender, headPose, smile, facialHair, glasses, emotion, hair, makeup, occlusion, accessories, blur, exposure, noise"
    }
    res = requests.post(face_api_url, params=params, 
                        headers=headers, data=binary_img)

    results = res.json()
    # 画像の顔部分の座標を取得
    for result in results:
        rect = result["faceRectangle"]    
        # 認識した顔に矩形を描画
        draw = ImageDraw.Draw(img)
        draw.rectangle([(rect["left"], rect["top"]), (rect["left"]+rect["width"], rect["top"]+rect["height"])], fill=None, outline="green", width=5)
        # 性別・年齢描画の座標設定
        font_size = 50
        font_name = "C:\Windows\Fonts\meiryo.ttc"
        draw_x = rect['left']-10
        draw_y = rect['top']-100
        text = result['faceAttributes']['gender']+'/'+str(result['faceAttributes']['age'])
        font = ImageFont.truetype(font_name, font_size)
        draw.text((draw_x, draw_y), text,font=font, fill='red')

    st.image(img, caption="Uploaded Image.", use_column_width=True)