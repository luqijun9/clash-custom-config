import requests
import yaml

# 原始订阅链接（记得换成自己的）
source_url = 'https://sub.dy.ax/sub?target=clash&url=https%3A%2F%2Fsakuracat1203.xn--3iq226gfdb94q.com%2Fapi%2Fv1%2Fclient%2Fsubscribe%3Ftoken%3D89f3d86f2e045f6cdd2df8a3d8044529&insert=false'

# 自定义规则文件路径
custom_rules_path = 'custom_rules.yaml'

# 最终输出配置文件
output_file = 'sakuracat.yaml'

# 下载原始订阅配置
resp = requests.get(source_url)

# 获取流量统计信息（HTTP 响应头）
userinfo = resp.headers.get('subscription-userinfo')

# 打印信息到 GitHub Actions 日志
if userinfo:
    print(f"[INFO] 订阅流量信息: {userinfo}")
else:
    print("[WARN] 响应头中未包含 subscription-userinfo 字段")

# 解析 YAML 内容
try:
    base_config = yaml.safe_load(resp.text)
except yaml.YAMLError as e:
    print(f"[ERROR] 解析订阅 YAML 出错: {e}")
    exit(1)

# 加载自定义规则
try:
    with open(custom_rules_path, 'r', encoding='utf-8') as f:
        custom = yaml.safe_load(f)
except FileNotFoundError:
    print(f"[ERROR] 未找到自定义规则文件: {custom_rules_path}")
    exit(1)

# 合并规则：自定义在前
base_config['rules'] = custom.get('rules', []) + base_config.get('rules', [])

# 写入合并后的配置文件，顶部保留流量信息
with open(output_file, 'w', encoding='utf-8') as f:
    if userinfo:
        f.write(f"# subscription-userinfo: {userinfo}\n")
    yaml.dump(base_config, f, allow_unicode=True)

print(f"[DONE] 已生成合并配置文件: {output_file}")
