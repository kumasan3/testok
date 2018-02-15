%rebase("base.tpl",title="掲示板 | 月木でわかる HTML5 &amp; CSS3")

<div>

<p>{{user_name}}さん こんにちは</p><br>
<img class="user_image" src="/static/img/{{user_image}}" />

<form action="/update_image" method="post" enctype="multipart/form-data">
    <input type="file" name="user_image">
    <input type="submit" name="save" value="画像送信">
    </form>

  <form action="/add" method="post">
    投稿者：{{user_name}}<br>
    内容：<textarea name="comment" cols="30" rows="5"></textarea><br>

    <input type="submit" name="save" value="送信">
  </form>


    %for item in comment_list:
  <div class="bbs_content">
    <p>{{item["comment"]}}</p>
        <p>{{item["datetime"]}}</p>
      <a href="/edit/{{item['id']}}">編集</a>
  <a class="confirm_link" href="/del/{{item['id']}}">削除</a><br><br>

  </div>
  %end


</div>


<div>
  <a href="/logout">ログアウト</a>
</div>
