%rebase("base.tpl",title="編集 | 月木でわかる HTML5 &amp; CSS3")

<div>
  <form action="/edit">
    <input type="hidden" value="{{comment['id']}}" name="item_id">
    内容：<textarea name="comment" cols="30" rows="5">{{comment["comment"]}}</textarea><br>
    <input type="submit" name="save" value="編集する">
  </form>
</div>
