from urllib.request import urlopen
from playsound import playsound
import urllib.parse
import json
import sys
import os


def getMusic():
    keyword = urllib.parse.urlencode({"keyword": input("输入音乐名:")})
    keyword = keyword[keyword.find("=") + 1 :]
    url = (
        "https://songsearch.kugou.com/song_search_v2?callback=jQuery1124042761514747027074_1580194546707&keyword="
        + keyword
        + "&page=1&pagesize=30&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filter=0&_=1580194546709"
    )
    content = urlopen(url=url)
    content = content.read().decode("utf-8")
    str_1 = content[content.find("(") + 1 : -2]
    str_2 = json.loads(str_1)
    Music_Hash = {}
    Music_id = {}
    for dict_1 in str_2["data"]["lists"]:
        Music_Hash[dict_1["FileName"]] = dict_1["FileHash"]
        Music_id[dict_1["FileName"]] = dict_1["AlbumID"]
    list_music_1 = [music for music in Music_Hash]
    list_music = [music for music in Music_Hash]
    for i in range(len(list_music)):
        if "- <em>" in list_music[i]:
            list_music[i] = list_music[i].replace("- <em>", "-")
        if "</em>" in list_music[i]:
            list_music[i] = list_music[i].replace("</em>", "")
        if "<em>" in list_music[i]:
            list_music[i] = list_music[i].replace("<em>", "")
    for i in range(len(list_music)):
        print("{}-:{}".format(i + 1, list_music[i]))
        
    music_id_1 = int(input("输入数字:"))
    url = (
        "https://wwwapi.kugou.com/yy/index.php?r=play/getdata&hash="
        + Music_Hash[list_music_1[music_id_1 - 1]]
        + "&album_id="
        + Music_id[list_music_1[music_id_1 - 1]]
        + "&dfid=2SSV0x4LWcsx0iylej1F6w7P&mid=44328d3dc4bfce21cf2b95cf9e76b968&platid=4"
    )
    
    js_content = urlopen(url=url)
    str_3 = js_content.read().decode("utf-8")
    dict_2 = json.loads(str_3)
    try:
        music_href = dict_2["data"]["play_backup_url"]
        music_content = urlopen(url=music_href).read()

        music_path = list_music[music_id_1 - 1] + ".mp3"
            
        with open(music_path, "wb") as f:
            print("下载中...")
            f.write(music_content)
            print("{}.mp3 下载成功!".format(list_music[music_id_1 - 1]))
    except:
        print("对不起,该歌曲无权下载!")
    else:
        if input("你希望播放吗('y'或 'n'):") == 'y':
            print("开始播放{}.mp3".format(list_music[music_id_1 - 1]))
            while True:
                try:
                    playsound(r"./{}.mp3".format(list_music[music_id_1 - 1]))
                except:
                    playsound(r"./{}.mp3".format(list_music[music_id_1 - 1]))
                else:
                    break
if __name__ == "__main__":
    while True:
        returnValue = os.system("cls")
        del returnValue
        
        getMusic()
