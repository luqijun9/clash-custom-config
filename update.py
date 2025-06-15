import yaml

# === 你的订阅链接 ===
subscribe_url = "https://sakuracat1203.xn--3iq226gfdb94q.com/api/v1/client/subscribe?token=89f3d86f2e045f6cdd2df8a3d8044529"

# === 自定义规则文件 ===
custom_rules_path = 'custom_rules.yaml'

# === 最终输出文件 ===
output_path = 'sakuracat.yaml'

# 加载自定义规则
with open(custom_rules_path, 'r', encoding='utf-8') as f:
    custom = yaml.safe_load(f)

# 构造完整配置
final_config = {
    'mixed-port': 7890,
    'allow-lan': True,
    'mode': 'Rule',
    'log-level': 'info',
    'external-controller': '127.0.0.1:9090',
    'proxy-providers': {
        'sakura': {
            'type': 'http',
            'url': subscribe_url,
            'interval': 3600,
            'path': './providers/sakura.yaml'
        }
    },
    'proxy-groups': [
        {
            'name': '节点选择',
            'type': 'select',
            'use': ['sakura']
        }
    ],
    'rules': custom.get('rules', []) + [
        'MATCH,节点选择'
    ]
}

# 写入配置文件
with open(output_path, 'w', encoding='utf-8') as f:
    yaml.dump(final_config, f, allow_unicode=True)
