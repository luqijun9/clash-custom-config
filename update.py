import requests
import yaml
import base64
import urllib.parse

# 订阅链接（替换成你的）
source_url = 'https://sakuracat1203.xn--3iq226gfdb94q.com/api/v1/client/subscribe?token=89f3d86f2e045f6cdd2df8a3d8044529'

# 自定义规则路径
custom_rules_path = 'custom_rules.yaml'

# 输出文件名
output_file = 'sakuracat_combined.yaml'

def parse_trojan_link(link):
    # 解析trojan链接为Clash格式节点字典
    parsed = urllib.parse.urlparse(link)
    userinfo, hostport = parsed.netloc.split('@')
    host, port = hostport.split(':')
    params = urllib.parse.parse_qs(parsed.query)

    allow_insecure = params.get('allowInsecure', ['0'])[0] == '1'
    sni = params.get('sni', [''])[0]
    remark = urllib.parse.unquote(parsed.fragment) if parsed.fragment else f"{host}:{port}"

    node = {
        'name': remark,
        'type': 'trojan',
        'server': host,
        'port': int(port),
        'password': userinfo,
        'udp': True,
        'skip-cert-verify': allow_insecure,
    }
    if sni:
        node['sni'] = sni

    return node

def main():
    # 1. 请求订阅，得到的是base64编码的文本
    resp = requests.get(source_url)
    resp.raise_for_status()
    encoded_text = resp.text.strip()

    # 2. base64解码，得到原始节点链接文本（通常一行一个链接）
    decoded_bytes = base64.b64decode(encoded_text)
    decoded_text = decoded_bytes.decode('utf-8').strip()

    # 3. 拆分成节点链接列表（每行一个）
    node_links = [line.strip() for line in decoded_text.splitlines() if line.strip()]

    # 4. 解析所有trojan节点
    nodes = []
    for link in node_links:
        if link.startswith('trojan://'):
            node = parse_trojan_link(link)
            nodes.append(node)
        else:
            # 如果有其他协议可以扩展解析逻辑
            pass

    # 5. 生成基础 Clash 配置结构
    clash_config = {
        'proxies': nodes,
        'proxy-groups': [
            {
                'name': 'Auto',
                'type': 'select',
                'proxies': [node['name'] for node in nodes]
            }
        ],
        'rules': []
    }

    # 6. 载入自定义规则文件
    with open(custom_rules_path, 'r', encoding='utf-8') as f:
        custom_rules = yaml.safe_load(f)

    # 7. 合并规则，优先使用自定义规则，然后加上clash_config已有规则（一般为空）
    clash_config['rules'] = custom_rules.get('rules', []) + clash_config.get('rules', [])

    # 8. 保存最终合并的YAML配置
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump(clash_config, f, allow_unicode=True)

    print(f"完成！已生成合并配置文件：{output_file}")

if __name__ == '__main__':
    main()
