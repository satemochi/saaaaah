<html>
<head>
<title>comics</title>
<style>
body{font-family: Meiryo UI, Osaka, 'MS PGothic', sans-serif;}
a:visited {color: #338833;}
</style>
</head>

<body>

<table width="100%"> <tr><td>
<b> 読んでる漫画の新刊情報まとめ ({{len(rows)}}タイトル)</b>
</td>
<td align="right">
<form action="/sort_request" method="get">
sorted by:
<select name="no" onchange="submit(this.form)">
%opnames = [u'登録日', u'タイトル', u'巻数', u'出版日', u'出版社', u'★',\
%           u'レビュー数', u'次巻出版予定日']
%for i in range(8):
		<option value={{i}}
		%if no == i:
				selected
		%end
		> {{opnames[i]}}</option>
%end
</select>
</form>
<div align="right"><i>last update: {{last_update}}</i></div>
</td></tr></table>


<hr>
%from datetime import datetime
%td = datetime.now()
%recent = 30
%for _, title, vol, pubd, pub, star, nrev, nd, author, uid, isbn, rev in rows:
		%base_url = "http://alert.shop-bell.com/comic/" + str(uid)
		%url = base_url
		%if isbn != None and isbn != "":
				%url = "http://www.amazon.co.jp/dp/" + isbn
		%end

		%pd = datetime.strptime('2001/1/1', '%Y/%m/%d')
		%if pubd != None:
				%pd = datetime.strptime(pubd, '%Y/%m/%d')
		%end
		%title_string = ""
		%if vol != None:
				%title_string = title + " (" + str(vol) + "), " + author \
				%				+ ", " + pubd + ", " + nd
				%if pub != None and pub != "":
						%title_string = title_string + ", " + pub 
				%end
				%if star != 0.0:
						%title_string = title_string + u", ★" + str(star) \
						%				+ ", " + str(nrev) + ", " + rev
				%end
		%else:
				%title_string = title + ", " + author 
		%end
		%if (td - pd).days < recent:
				<b>
		%end
<a href="{{url}}" target="_blank" title="{{title_string[:400]}}"> {{title}} </a>
(<a href="{{base_url}}" target="_blank">{{vol}}</a>)</b> /
		%if (td - pd).days < recent:
				</b>
		%end
%end


<hr>

<ul>
<li> 最新刊が出版されてから{{recent}}日未満の作品はボールド体で表示しています。
<li> <a href="http://www.kurage-bunch.com/" target="_blank">  くらげ </a> /
<a href="http://plus.shonenjump.com/" target="_blank"> ジャンプ+ </a> /
<a href="http://www.ganganonline.com/" target="_blank">  ガンガン・オンライン </a> /
<a href="http://www.tonarinoyj.jp/" target="_blank">  となりのYJ </a> /
<a href="http://sai-zen-sen.jp/comics/twi4/tomochan/" target="_blank"> ともちゃん </a> /
</ul>


</body>
</html>

