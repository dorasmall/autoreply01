from flask import Flask, request, make_response
import xml.etree.ElementTree as ET
import time

app = Flask(__name__)

# 微信 Token（需与微信公众平台配置一致）
WECHAT_TOKEN = 'your_token'

@app.route('/wechat', methods=['GET', 'POST'])
def wechat():
    if request.method == 'GET':
        # 验证服务器
        signature = request.args.get('signature', '')
        timestamp = request.args.get('timestamp', '')
        nonce = request.args.get('nonce', '')
        echostr = request.args.get('echostr', '')

        # 验证签名
        if check_signature(signature, timestamp, nonce):
            return echostr
        else:
            return '验证失败'
    else:
        # 处理用户消息
        xml_data = request.data
        xml_tree = ET.fromstring(xml_data)
        msg_type = xml_tree.find('MsgType').text
        if msg_type == 'text':
            user_input = xml_tree.find('Content').text
            # 解析用户输入
            parts = user_input.split('+')
            if len(parts) == 3:
                username, project_name, password = parts
                # 根据项目名字匹配图片
                image_url = match_image(project_name)
                # 返回图片消息
                response = generate_image_response(xml_tree, image_url)
                return response
            else:
                # 输入格式错误
                return generate_text_response(xml_tree, "输入格式错误，请按照'用户名+项目名字+四位数字'格式输入。")

def check_signature(signature, timestamp, nonce):
    # 验证微信签名
    tmp_list = sorted([WECHAT_TOKEN, timestamp, nonce])
    tmp_str = ''.join(tmp_list)
    import hashlib
    hash_str = hashlib.sha1(tmp_str.encode('utf-8')).hexdigest()
    return hash_str == signature

def match_image(project_name):
    # 根据项目名字匹配图片 URL
    image_mapping = {
        'project1': 'https://example.com/image1.jpg',
        'project2': 'https://example.com/image2.jpg',
        # 更多项目与图片的映射
    }
    return image_mapping.get(project_name, 'https://example.com/default.jpg')

def generate_image_response(xml_tree, image_url):
    # 生成图片消息的 XML 响应
    return f"""
    <xml>
        <ToUserName><![CDATA[{xml_tree.find('FromUserName').text}]]></ToUserName>
        <FromUserName><![CDATA[{xml_tree.find('ToUserName').text}]]></FromUserName>
        <CreateTime>{int(time.time())}</CreateTime>
        <MsgType><![CDATA[image]]></MsgType>
        <Image>
            <MediaId><![CDATA[{image_url}]]></MediaId>
        </Image>
    </xml>
    """

def generate_text_response(xml_tree, text):
    # 生成文本消息的 XML 响应
    return f"""
    <xml>
        <ToUserName><![CDATA[{xml_tree.find('FromUserName').text}]]></ToUserName>
        <FromUserName><![CDATA[{xml_tree.find('ToUserName').text}]]></FromUserName>
        <CreateTime>{int(time.time())}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{text}]]></Content>
    </xml>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
