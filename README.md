# youtube_live_comment

This file takes the chat comments from YoutubeLive, stats certain words, and graphs them so that you can visualize the highlighted areas.
このファイルは、YoutubeLiveのチャットコメントを取り込み、特定の単語を統計して、ハイライトされた部分を視覚化できるようにグラフ化したものです。

##Usage

1. Run main.py and enter the video ID in Input.
   A CSV file with the comments will be created.
   main.pyを実行し、Inputに動画IDを入力します。
   コメントの入ったCSVファイルが作成されます。

2. graph.py inputs the ID of the video from which the comment was taken, and displays a graph showing which words are posted how many times in how many seconds.
   graph.pyは、コメントが投稿された動画のIDを入力し、どの単語が何秒に何回投稿されたかをグラフで表示します。
