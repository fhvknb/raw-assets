# 导入 itertools 库，用于生成字母两两组合
import itertools

# 定义26个字母
letters = "abcdefghijklmnopqrstuvwxyz"

letters2 = 'aehitszuy'
#  a e h i t s z u 
# 生成所有字母的两两组合
combinations = [''.join(pair) for pair in itertools.product(letters2, repeat=3)]

# 以 'ra' 开头，拼接两两组合，并加上 '.com'
domains = [f"ah{pair}.com" for pair in combinations]

# 将生成的域名写入到文件 domain.txt 中
with open("domain.txt", "w") as file:
    for domain in domains:
        file.write(domain + "\n")

print("域名已成功写入到文件 domain.txt 中！")
