import bcrypt

def hash_password(password: str) -> str:
    """
    使用 bcrypt 对密码进行加密并返回加密后的哈希值。
    
    :param password: 需要加密的密码（字符串）
    :return: 加密后的哈希值（字符串）
    """
    # 将密码编码为字节
    password_bytes = password.encode('utf-8')
    
    # 生成盐值
    salt = bcrypt.gensalt()
    
    # 使用 bcrypt 生成哈希
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    
    # 返回哈希值（解码为字符串）
    return hashed_password.decode('utf-8')



def verify_password(password: str, hashed: str) -> bool:
    """
    验证密码是否与加密后的哈希值匹配。
    
    :param password: 用户输入的密码（字符串）
    :param hashed: 数据库中存储的哈希值（字符串）
    :return: 是否匹配（布尔值）
    """
    # 将密码编码为字节
    password_bytes = password.encode('utf-8')
    
    # 将哈希值编码为字节
    hashed_bytes = hashed.encode('utf-8')
    
    # 验证密码
    return bcrypt.checkpw(password_bytes, hashed_bytes)


# 示例用法
if __name__ == "__main__":
    # 输入需要加密的密码
    password = "my_secure_password"
    
    # 调用加密方法
    hashed = hash_password(password)
    
    print(f"原始密码: {password}")  
    print(f"加密后的哈希值: {hashed}")


     # 原始密码
    # password = "my_secure_password"
    
    # # 加密后的哈希值
    # hashed = hash_password(password)
    
    # # 验证密码
    # is_valid = verify_password("my_secure_password", hashed)
    # print(f"密码验证结果: {is_valid}")
