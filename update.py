import requests
import yaml

# 原始订阅链接（你要换成你自己的）
source_url = 'https://你的订阅链接/clash.yaml'

# 自定义规则文件路径
custom_rules_path = 'custom_rules.yaml'

# 最终输出文件
output_file = 'sakuracat.yaml'

# 下载原始配置
resp = requests.get(source_url)
base_config = yaml.safe_load(resp.text)

# 加载自定义规则
with open(custom_rules_path, 'r', encoding='utf-8') as f:
    custom = yaml.safe_load(f)

# 合并规则
base_config['rules'] = custom.get('rules', []) + base_config.get('rules', [])

# 保存合并后的配置
with open(output_file, 'w', encoding='utf-8') as f:
    yaml.dump(base_config, f, allow_unicode=True)
