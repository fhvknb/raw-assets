import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2
from mutagen.flac import FLAC
from mutagen.asf import ASF  # 添加对WMA文件的支持

def batch_update_titles(folder_path):
    """批量更新文件夹中所有MP3、FLAC和WMA文件的标题为文件名(不含扩展名)"""
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        # 使用文件名作为新标题(去掉扩展名)
        new_title = os.path.splitext(filename)[0]
        
        if filename.lower().endswith('.mp3'):
            update_mp3_title(file_path, new_title)
        elif filename.lower().endswith('.flac'):
            update_flac_title(file_path, new_title)
        elif filename.lower().endswith('.wma'):
            update_wma_title(file_path, new_title)

def update_mp3_title(file_path, new_title, artist=None, album=None):
    """修改MP3文件的标题和其他元数据"""
    try:
        # 尝试加载现有的ID3标签
        try:
            tags = ID3(file_path)
        except:
            tags = ID3()
        
        # 更新标题
        tags["TIT2"] = TIT2(encoding=3, text=new_title)
        
        # 如果提供了艺术家信息，也更新它
        if artist:
            from mutagen.id3 import TPE1
            tags["TPE1"] = TPE1(encoding=3, text=artist)
        
        # 如果提供了专辑信息，也更新它
        if album:
            from mutagen.id3 import TALB
            tags["TALB"] = TALB(encoding=3, text=album)
            
        tags.save(file_path)
        print(f"已更新MP3: {os.path.basename(file_path)} -> 标题: {new_title}")
        
    except Exception as e:
        print(f"处理MP3文件 {os.path.basename(file_path)} 时出错: {e}")

def update_flac_title(file_path, new_title, artist=None, album=None):
    """修改FLAC文件的标题和其他元数据"""
    try:
        audio = FLAC(file_path)
        
        # 更新标题
        audio["title"] = new_title
        
        # 如果提供了艺术家信息，也更新它
        if artist:
            audio["artist"] = artist
        
        # 如果提供了专辑信息，也更新它
        if album:
            audio["album"] = album
        
        # 保存更改
        audio.save()
        print(f"已更新FLAC: {os.path.basename(file_path)} -> 标题: {new_title}")
        
    except Exception as e:
        print(f"处理FLAC文件 {os.path.basename(file_path)} 时出错: {e}")

def update_wma_title(file_path, new_title, artist=None, album=None):
    """修改WMA文件的标题和其他元数据"""
    try:
        audio = ASF(file_path)

        # 更新标题
        audio["title"] = [new_title]
        audio["WM/AlbumTitle"] = [new_title]
        
        # 如果提供了艺术家信息，也更新它
        if artist:
            audio["author"] = [artist]
            audio["Author"] = [ "ZiYi" ]

        
        # 如果提供了专辑信息，也更新它
        if album:
            audio["album"] = [album]

        if artist and album:
            audio["WM/AlbumArtist"] = [f'{artist}/{album}']
        
        # 保存更改
        audio.save()
        print(f"已更新WMA: {os.path.basename(file_path)} -> 标题: {new_title}")
        
    except Exception as e:
        print(f"处理WMA文件 {os.path.basename(file_path)} 时出错: {e}")

# 扩展函数，支持批量更新所有类型文件的标题、艺术家和专辑信息
def batch_update_metadata(folder_path, update_artist=None, update_album=None):
    """批量更新文件夹中所有音频文件的元数据"""
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        # 使用文件名作为新标题(去掉扩展名)
        new_title = os.path.splitext(filename)[0]
        
        if filename.lower().endswith('.mp3'):
            update_mp3_title(file_path, new_title, update_artist, update_album)
        elif filename.lower().endswith('.flac'):
            update_flac_title(file_path, new_title, update_artist, update_album)
        elif filename.lower().endswith('.wma'):
            update_wma_title(file_path, new_title, update_artist, update_album)

# 使用示例
if __name__ == "__main__":
    # 只更新标题
    batch_update_metadata("/Users/shawnxiang/Desktop/hanlaoshi/Season3", "ZiYi", "Phoenix")
    
    # 或者更新标题、艺术家和专辑信息
    # batch_update_metadata("/path/to/your/music/folder", "艺术家名称", "专辑名称")
