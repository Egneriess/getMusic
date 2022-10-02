import json
import urllib.parse
from urllib.request import urlopen

import pygame


def get_music():
    try:
        keyword = urllib.parse.urlencode({"keyword": input("输入音乐名:")})
        keyword = keyword[keyword.find("=") + 1:]
        url = (
                "https://songsearch.kugou.com/song_search_v2?callback=jQuery1124042761514747027074_1580194546707&keywor"
                "d="
                + keyword
                + "&page=1&pagesize=30&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege"
                  "_filter=0&_=1580194546709"
        )
        content = urlopen(url=url)
        content = content.read().decode("utf-8")
        str_1 = content[content.find("(") + 1: -2]
        str_2 = json.loads(str_1)
        music_hash = {}
        music_id = {}
        for dict_1 in str_2["data"]["lists"]:
            music_hash[dict_1["FileName"]] = dict_1["FileHash"]
            music_id[dict_1["FileName"]] = dict_1["AlbumID"]
        list_music_1 = [music for music in music_hash]
        list_music = [music for music in music_hash]
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
                + music_hash[list_music_1[music_id_1 - 1]]
                + "&album_id="
                + music_id[list_music_1[music_id_1 - 1]]
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
        except KeyError:
            input("对不起,该歌曲无权下载!")
        else:
            if input("你希望播放吗('y'或 'n'):") == "y":
                print("开始播放{}.mp3".format(list_music[music_id_1 - 1]))
                pygame.init()
                pygame.mixer.init()
                pygame.mixer.music.load(
                    r"{}.mp3".format(list_music[music_id_1 - 1])
                )
                pygame.mixer.music.play()
    except KeyboardInterrupt:
        get_music()


if __name__ == "__main__":
    while True:
        get_music()
