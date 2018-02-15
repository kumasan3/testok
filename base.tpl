<!DOCTYPE HTML>
<html lang="ja">

<head>
	<meta charset="utf-8">
	<meta name="keywords" content="サイトをキーワードで説明">
	<meta name="description" content="どんなサイトかを短い文章で説明">
	<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=1">
	<link rel="icon" href="staic/favicon.ico">
	<link rel="stylesheet" type="text/css" media="screen and ( min-width:769px )" href="/static/css/style_pc.css">
	<link rel="stylesheet" type="text/css" media="screen and ( max-width:768px )" href="/static/css/style_sp.css">
	<title>{{title or 'No title'}}</title>

<script type="text/javascript" src="/static/js/jquery-3.2.1.min.js"></script>
<script type="text/javascript" src="/static/js/jquery.fadethis.min.js"></script>
<!-- drawer.css -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/drawer/3.2.2/css/drawer.min.css">
<!-- jquery & iScroll -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/iScroll/5.2.0/iscroll.min.js"></script>
<!-- drawer.js -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/drawer/3.2.2/js/drawer.min.js"></script>

<script type="text/javascript" src="/static/js/common.js"></script>

</head>

<body class="drawer drawer--right">

	<header>
		<button type="button" class="drawer-toggle drawer-hamburger">
    <span class="sr-only">toggle navigation</span>
    <span class="drawer-hamburger-icon"></span>
  </button>

	<nav class="drawer-nav" role="navigation">

		<ul class="drawe-menu">
			<li><a class="drawer-menu-item" href="/#sec1" id="menu-sec1">見出しのエリア</a></li>
			<li><a class="drawer-menu-item" href="/#sec2" id="menu-sec2">flexのエリア</a></li>
			<li><a class="drawer-menu-item" href="/#sec3" id="menu-sec3">センタリングエリア</a></li>
			<li><a class="drawer-menu-item" href="/#sec4" id="menu-sec4">制作実績</a></li>
						<!-- 追加した箇所↓ -->
			<li>
				<a class="drawer-menu-item" href="#" id="lng-ja">日本語</a>
				<a class="drawer-menu-item" href="#" id="lng-en">English</a>
			</li>
			<li>
				<a class="drawer-menu-item" href="#" id="bg-blue">Blue</a>
				<a class="drawer-menu-item" href="#" id="bg-red">Red</a>
			</li>
			<!-- 追加した箇所ここまで -->
			<li>
				<a class="drawer-menu-item" href="/register">ご登録はこちら</a>
			</li>
		</ul>
	</nav>
	</header>

{{!base}}
<div class="delete">削除
</div>
  <footer>
		<p class="copyright">Copyright &copy; DEMO all rights reserved.</p>
	</footer>

</body>

</html>
