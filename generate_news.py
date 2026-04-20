import os
import json
from datetime import datetime
import anthropic

def get_daily_info():
    # 连接 Claude
    client = anthropic.Anthropic(api_key=os.environ.get("CLAUDE_API_KEY"))
    
    # 【注意】这里是你对 Claude 说的话，你可以自己修改引号里面的内容！
    prompt = "请给我今天的一句话鼓励，以及3条全球最重要的科技新闻简述。" 
    
    # 发送请求
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022", # 使用最新的模型
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text

def save_to_json(content):
    date_str = datetime.now().strftime("%Y-%m-%d")
    new_data = {"date": date_str, "content": content}
    
    file_path = "data.json"
    data = []
    
    # 如果以前有数据，就先读出来
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
    # 把今天的新数据插到最前面
    data.insert(0, new_data)
    
    # 保存文件
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    content = get_daily_info()
    save_to_json(content)
