# Ipe logo workshop (unofficial)

<img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/point_location_with_shape_of_Ipe.png" width=25%><img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/constrained_triangulations_with_shape_of_Ipe.png" width=25%><img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/visibility_graph_with_shape_of_Ipe.png" width=25%><img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/approximated_geodesic_voronoi_in_Ipe.png" width=25%>
<img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/tsp_art_with_polygonalization_in_ipe.png" width=25%><img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/quadtree_for_shape_of_Ipe.png" width=25%><img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/circle_packing_with_descartes_theorem_in_Ipe.png" width=25%><img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/contour_polygons_with_shape_of_Ipe.png" width=25%>
<img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/medial_axis_with_segment_voronoi.png" width=25%> <img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/art_gallery_problem_in_shape_of_ipe.png" width=25%>





## Description

ここはドローツール
[Ipe](https://ipe.otfried.org)
の非公式ロゴを制作している工房です。
python + matplotlib + `backend_ipe.py`　で `.ipe` ファイルを生成しています。
ここで公開している .ipe ファイルは
Ipe で開いて編集することができます。

文字列 Ipe のグリフを入力多角形とし
計算幾何学で代表的なトピックを題材にいろいろな図形を描画しています。
Ipe をモチーフにしている理由は日頃の感謝の表明です。
計算幾何学のトピックをテーマに選んでいる理由は
Ipe の作者である
[オットフリード先生](https://otfried.org)
へのオマージュです。

**お願い**
この作業は本家さまとは一切関係がない第三者の赤の他人が勝手にやっています。
提示している作品やスタッフに不備がある場合や質問等は
[ここ](https://github.com/satemochi/saaaaah/issues)で
報告して頂けると助かります。
できれば日本語で。



## Polygon generation for each input

入力生成のフェーズで利用させて頂いたフォントやツールについて明記しておきます。
- フォントとして
[Alice フォント](https://fonts.google.com/specimen/Alice/license)を
利用しています。
[Open Font License](https://openfontlicense.org) です。
- アウトラインの取得は [freetype-py](https://github.com/rougier/freetype-py) の
[glyph-vector.py](https://github.com/rougier/freetype-py/blob/master/examples/glyph-vector.py) を
少し改変して使用しています。
[BSD ライセンス](https://github.com/rougier/freetype-py/blob/master/LICENSE.txt)
です。
- それから英語多角形のブール演算は [shapely](https://github.com/shapely/shapely)
を利用しています。
[BSD ライセンス](https://github.com/shapely/shapely/blob/main/LICENSE.txt)です。




## Gallery and stuff



### Polygonal boolean operations and Inclusion test

[多角形のブール演算](https://en.wikipedia.org/wiki/Boolean_operations_on_polygons)および[包囲テスト](https://en.wikipedia.org/wiki/Point_in_polygon#:~:text=In%20computational%20geometry%2C%20the%20point,%2Daided%20design%20(CAD).&text=An%20early%20description%20of%20the,of%20the%20Ray%20Tracing%20News.)の基本を確認したかったので作成したロゴです。
出力は下図のようになります。
包囲テストは shapely 多角形の
[contains](https://shapely.readthedocs.io/en/stable/reference/shapely.Polygon.html#shapely.Polygon.contains)
メソッドを利用しています。

- python: [point_location_with_shape_of_Ipe.py](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/point_location_with_shape_of_Ipe.py)
- ipe: [point_location_with_shape_of_Ipe.ipe](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/point_location_with_shape_of_Ipe.ipe)

<div align="center">
<img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/point_location_with_shape_of_Ipe.png" width=75%></div>







### Mesh Generation
多角形内部を[三角形分割](https://en.wikipedia.org/wiki/Polygon_triangulation)しておくと何かと便利なので[メッシュ生成](https://en.wikipedia.org/wiki/Mesh_generation)モジュール
[triangle](https://rufat.be/triangle/)
を利用してやってみました。[LGPL-3 ライセンス](https://github.com/drufat/triangle/blob/master/LICENSE)です。
今回は $30$ 度未満の鋭角三角形を禁止するようなメッシュを生成しています。

- python: [constrained_triangulations_with_shape_of_Ipe.py](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/constrained_triangulations_with_shape_of_Ipe.py)
- ipe: [constrained_triangulations_with_shape_of_Ipe.ipe](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/constrained_triangulations_with_shape_of_Ipe.ipe)



<div align="center">
<img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/constrained_triangulations_with_shape_of_Ipe.png" width=75%></div>









### Visivility Graph
[可視グラフ](https://en.wikipedia.org/wiki/Visibility_graph#:~:text=In%20computational%20geometry%20and%20robot,a%20visible%20connection%20between%20them.)が見たかったのでやってみました。
可視グラフの生成には
[Visilibity](https://karlobermeyer.github.io/VisiLibity1/)
を利用しています。
[LGPL-3 ライセンス](https://github.com/karlobermeyer/VisiLibity1#license)です。
英語多角形の曲線部分は頂点が密集しているので
[RDP アルゴリズム](https://en.wikipedia.org/wiki/Ramer–Douglas–Peucker_algorithm)
を適用していくつかの頂点を間引いています。
[MIT ライセンス](https://github.com/fhirschmann/rdp/blob/master/LICENSE.txt)です。
この際 [rdp パッケージ](https://pypi.org/project/rdp/)を利用しています。

- python: [visibility_graph_with_shape_of_Ipe.py](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/visibility_graph_with_shape_of_Ipe.py)
- ipe: [visibility_graph_with_shape_of_Ipe.ipe](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/visibility_graph_with_shape_of_Ipe.ipe)


<div align="center">
<img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/visibility_graph_with_shape_of_Ipe.png" width=75%></div>






### Geodesic Voronoi Diagram
Ipe 多角形内で[ボロノイ図](https://en.wikipedia.org/wiki/Voronoi_diagram)が描きたかったのでやってみました。
[OpenGL](https://ja.wikipedia.org/wiki/OpenGL) や
[GLFW](https://en.wikipedia.org/wiki/GLFW) を利用して
([加法重みの](https://en.wikipedia.org/wiki/Weighted_Voronoi_diagram))
ボロノイ描画をカラーバッファに吐き出しつつ
[境界抽出](https://en.wikipedia.org/wiki/Boundary_tracing)して各母点の勢力圏多角形を取得しています。

- python: [approximated_geodesic_voronoi_in_Ipe.py](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/approximated_geodesic_voronoi_in_Ipe.py)
- ipe: [approximated_geodesic_voronoi_in_Ipe.ipe](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/approximated_geodesic_voronoi_in_Ipe.ipe)



<div align="center">
<img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/approximated_geodesic_voronoi_in_Ipe.png" width=75%></div>






### TSP art
正確には
[TSP アート](https://www2.oberlin.edu/math/faculty/bosch/tspart-page.html)
ではないのですが
それっぽい多角形を生成するコードを作成しました。
少なくとも一筆書きにはなっています。
[深さ優先探索](https://en.wikipedia.org/wiki/Depth-first_search)で三角形を結合していますが[幅優先探索](https://en.wikipedia.org/wiki/Breadth-first_search)の方が
周囲長が短くなるような気がしますので、
より TSP の最適解に近づけるならそういう改善もありかも知れません。

- python: [tsp_art_with_polygonalization_in_ipe.py](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/tsp_art_with_polygonalization_in_ipe.py)
- ipe: [tsp_art_with_polygonalization_in_ipe.ipe](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/tsp_art_with_polygonalization_in_ipe.ipe)


<div align="center">
<img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/tsp_art_with_polygonalization_in_ipe.png" width=75%></div>







### Quadtree
Ipe 多角形の頂点を入力として[四分木](https://en.wikipedia.org/wiki/Quadtree)を適用してみました。
それだけなんですけど。

- python: [quadtree_for_shape_of_Ipe.py](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/quadtree_for_shape_of_Ipe.py)
- ipe: [quadtree_for_shape_of_Ipe.ipe](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/quadtree_for_shape_of_Ipe.ipe)


<div align="center">
<img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/quadtree_for_shape_of_Ipe.png" width=75%></div>








### Circle packing with Descartes Theorem
Ipe 多角形内部に異なる半径の[円を充填](https://en.wikipedia.org/wiki/Circle_packing)してみました。
このコードは Andres Ariza-Triana さんの
[circpacker: Circle Packer](https://github.com/aarizat/circpacker/tree/master)
を利用しています。
下記の python コードに必要箇所を埋め込んでいますが、
普通に使うなら pip でインストールすると良いかと思います。
BSD ライセンスです。

- python: [circle_packing_with_descartes_theorem_in_Ipe.py](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/circle_packing_with_descartes_theorem_in_Ipe.py)
- ipe: [circle_packing_with_descartes_theorem_in_Ipe.ipe](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/circle_packing_with_descartes_theorem_in_Ipe.ipe)


<div align="center">
<img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/circle_packing_with_descartes_theorem_in_Ipe.png" width=75%></div>





### Contour polygons with Minkowski sums
Ipe 多角形内部に等高線みたいな描画がしたくて描いてみました。
shapely.buffer を利用すると容易に[ミンコフスキ和](https://en.wikipedia.org/wiki/Minkowski_addition)が得られて楽しいです。
多角形内部に等高線が来るようにするために多角形のブール積をとっています。
そんなバッファード多角形を11個も描画しています。

- python: [contour_polygons_with_shape_of_Ipe.py](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/contour_polygons_with_shape_of_Ipe.py)
- ipe: [contour_polygons_with_shape_of_Ipe.ipe](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/contour_polygons_with_shape_of_Ipe.ipe)

<div align="center">
<img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/contour_polygons_with_shape_of_Ipe.png" width=75%></div>




### Medial axis with Voronoi diagrams for segments

Ipe 多角形の[中心軸](https://en.wikipedia.org/wiki/Medial_axis)をとりたかったのでやってみました。
誤差がひどくて目眩がしますが、なんとなくムーミンぽかったので ok にしました。
各線分をどのように細分するかとか、
得られたボロノイ図からどのリッジを残すか
などをもう少し丁寧に設計しないといけません。
曲率と細分粒度のアンバランスから、
ミクロ視点で曲線部分の各頂点がコーナー認定されているのだと思います。
調整するとヒゲはかなり削減することはできます。
今回のボロノイ図計算は
[scipy](https://scipy.org) を利用させて頂きました。
[BSD ライセンス](https://github.com/scipy/scipy/blob/main/LICENSE.txt)です。


- python: [medial_axis_with_segment_voronoi.py](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/medial_axis_with_segment_voronoi.py)
- ipe: [medial_axis_with_segment_voronoi.ipe](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/medial_axis_with_segment_voronoi.ipe)

<div align="center">
<img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/medial_axis_with_segment_voronoi.png" width=75%></div>




### Art Gallery Problem with vertex-guards 

可視多角形で何かやりたかったので美術館問題の簡単な例をテーマにしてみました。
可視多角形は可視グラフのときと同様に 
[Visilibity](https://karlobermeyer.github.io/VisiLibity1/)
を利用しています。
[LGPL-3 ライセンス](https://github.com/karlobermeyer/VisiLibity1#license)です。
最適配置の解決には線形計画ソルバの
[PuLP + COIN-OR CLP](https://pypi.org/project/PuLP/) を利用しています。
[MIT ライセンス](https://github.com/coin-or/pulp/blob/master/LICENSE)
のようです。


- python: [art_gallery_problem_in_shape_of_ipe.py](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/art_gallery_problem_in_shape_of_ipe.py)
- ipe: [art_gallery_problem_in_shape_of_ipe.ipe](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/art_gallery_problem_in_shape_of_ipe.ipe)

<div align="center">
<img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/art_gallery_problem_in_shape_of_ipe.png" width=75%></div>






## おしまい
今回はここまでです。
気が向いたら計算幾何学のトピックから選んで随時ロゴ作成していきたいと思います。
さよーならー。




