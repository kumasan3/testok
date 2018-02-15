import os
import sqlite3
from bottle import route, run, debug, template, request, static_file, error, redirect, response,datetime



@route('/')
def index():
    return template('index')


# GET  /register => 登録画面を表示
# POST /register => 登録処理をする
@route('/register',method=["GET", "POST"])
def register():
    if request.method == "GET":
        name = request.get_cookie("name" , secret="startupcafekoza")
        if name is None:
            return template("register")
        else:
            return redirect("/bbs")
    # ここからPOSTの処理
    else:
        name = request.POST.getunicode("name")
        password = request.POST.getunicode("password")

        conn = sqlite3.connect('service.db')
        c = conn.cursor()
        c.execute("insert into user values(null,?,?,'0.png')", (name,password))
        conn.commit()
        conn.close()
        return redirect('/login')


# GET  /login => ログイン画面を表示
# POST /login => ログイン処理をする
@route("/login", method=["GET", "POST"])
def login():
    if request.method == "GET":
        user_id = request.get_cookie("user_id", secret="startupcafekoza")
        if user_id is None:
            return template("login")
        else:
            return redirect("/bbs")
    else:
        # ブラウザから送られてきたデータを受け取る
        name = request.POST.getunicode("name")
        password = request.POST.getunicode("password")

        # ブラウザから送られてきた name ,password を userテーブルに一致するレコードが
        # 存在するかを判定する。レコードが存在するとuser_idに整数が代入、存在しなければ nullが入る
        conn = sqlite3.connect('service.db')
        c = conn.cursor()
        c.execute("select id from user where name = ? and password = ?", (name, password) )
        user_id = c.fetchone()
        conn.close()

        # user_id が NULL(PythonではNone)じゃなければログイン成功
        if user_id is not None:
            user_id = user_id[0]
            # クッキー(ブラウザ側に)にnameを記憶させる
            # これで誰が今ログインしているのか判定できる
            response.set_cookie("user_id", user_id, secret='startupcafekoza')
            return redirect("/bbs")
        else:
            # ログイン失敗すると、ログイン画面に戻す
            return template("login")

@route("/logout")
def logout():
    # ログアウトはクッキーに None を設定してあげるだけ
    response.set_cookie("user_id", None, secret='startupcafekoza')
    return redirect("/login") # ログアウト後はログインページにリダイレクトさせる


@route('/bbs')
def bbs():
    # クッキーからuser_idを取得
    user_id = request.get_cookie("user_id", secret="startupcafekoza")
    conn = sqlite3.connect('service.db')
    c = conn.cursor()
    # # DBにアクセスしてログインしているユーザ名と投稿内容を取得する
    # クッキーから取得したuser_idを使用してuserテーブルのnameを取得
    c.execute("select name, user_image from user where id = ?", (user_id,))
    # fetchoneはタプル型
    user_info = c.fetchone()
    user_name = user_info[0]
    user_image = user_info[1]
    c.execute("select id,comment,datetime from bbs where flag = 0 and userid = ? order by id", (user_id,))
    comment_list = []
    for row in c.fetchall():
        comment_list.append({"id": row[0], "comment": row[1], "datetime":row[2]})
    c.close()
    return template('bbs' , user_name = user_name , comment_list = comment_list, user_image = user_image)




@route('/add', method=["POST"])
def add():
        d = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        # クッキーから user_id を取得
        user_id = request.get_cookie("user_id", secret="startupcafekoza")
        # POSTアクセスならDBに登録する
        # フォームから入力されたアイテム名の取得(Python2ならrequest.POST.getunicodeを使う)
        comment = request.POST.getunicode("comment")
        conn = sqlite3.connect('service.db')
        c = conn.cursor()
        # DBにデータを追加する
        c.execute("insert into bbs values(null,?,?,0,?)", (user_id, comment,d))
        conn.commit()
        conn.close()
        return redirect('/bbs')


@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static', download=True)



@route("/update_image", method=["POST"])
def update_image():
    d = datetime.now().strftime("%Y:%m:%d:%H:%M:%S")
    user_id = request.get_cookie("user_id", secret="startupcafekoza")
    upload = request.files.get('user_image', "") #画像自体を代入
    name, ext = os.path.splitext(upload.filename) #画像の拡張子をextに代入
    upload.filename = d+str(user_id) + ext #画像自体の名前をユーザーid.拡張子　に変更
    if not upload.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        return " '.png', '.jpg', '.jpeg'形式のファイルのみをアップロードしてください"
    save_path = get_save_path() #保存する時の相対パスを取得。get_save_pathは下に定義されてる
    conn = sqlite3.connect('service.db')
    c = conn.cursor()
    c.execute("select user_image from user where id=?", (user_id,)) #古い（現時点の）画像の名前を取得。除去するのに必要
    current_image_name = c.fetchone()[0] #古い（現時点の）画像の名前を代入
    if current_image_name != "0.png":  #デフォルトの画像は消させない
        os.remove(save_path+current_image_name) #古い（現時点の）画像を除去
    c.execute("update user set user_image =? where id=?", (d+str(user_id)+ext, user_id)) #データベースに画像の名前をユーザーidで保存
    conn.commit()
    conn.close()

    upload.save(save_path) #画像自体を/static/imgに保存
    return redirect('/bbs')

def get_save_path():
    path_dir = "./static/img/"
    return path_dir


@route('/edit/<id:int>')
def edit(id):
    conn = sqlite3.connect('service.db')
    c = conn.cursor()
    c.execute("select comment from bbs where id = ?", (id,) )
    comment = c.fetchone()
    conn.close()

    if comment is not None:
        # None に対しては インデクス指定できないので None 判定した後にインデックスを指定
        comment = comment[0]
        # "りんご" ○   ("りんご",) ☓
        # fetchone()で取り出したtupleに 0 を指定することで テキストだけをとりだす
    else:
        return "アイテムがありません" # 指定したIDの name がなければときの対処

    item = { "id":id, "comment":comment }

    return template("edit", comment=item)


# /add ではPOSTを使ったので /edit ではあえてGETを使う
@route("/edit")
def update_item():
    # ブラウザから送られてきたデータを取得
    item_id = request.GET.getunicode("item_id") # id
    item_id = int(item_id)# ブラウザから送られてきたのは文字列なので整数に変換する
    comment = request.GET.getunicode("comment") # 編集されたテキストを取得する

    # 既にあるデータベースのデータを送られてきたデータに更新
    conn = sqlite3.connect('service.db')
    c = conn.cursor()
    c.execute("update bbs set comment = ? where id = ?",(comment,item_id))
    conn.commit()
    conn.close()

    # アイテム一覧へリダイレクトさせる
    return redirect("/bbs")


# /del/100 -> item_id = 100
# /del/50 -> item_id = 50
# /del/one -> HTTPError 404 文字列にするとエラーが出る
# /del/stacafe -> HTTPError 404
# /del/koza -> HTTPError 404
@route("/del/<id:int>")
def del_item(id):
    conn = sqlite3.connect('service.db')
    c = conn.cursor()
    # 指定されたitem_idを元にDBデータを削除
    c.execute("update bbs set flag=1 where id=?", (id,))
    conn.commit()
    conn.close()
    # 処理終了後に一覧画面に戻す
    return redirect("/bbs")

@error(403)
def mistake403(code):
    return 'There is a mistake in your url!'

@error(404)
def mistake404(code):
    return '404だよ!URL間違ってない！？'






run(port="8080" ,debug=True, reloader=True)
