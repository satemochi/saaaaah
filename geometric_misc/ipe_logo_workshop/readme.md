# Ipe logo workshop

<img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/point_location_with_shape_of_Ipe.png" width=25%><img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/constrained_triangulations_with_shape_of_Ipe.png" width=25%><img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/visibility_graph_with_shape_of_Ipe.png" width=25%><img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/approximated_geodesic_voronoi_in_Ipe.png" width=25%>
<img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/tsp_art_with_polygonalization_in_ipe.png" width=25%><img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/quadtree_for_shape_of_Ipe.png" width=25%></div><img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/circle_packing_with_descartes_theorem_in_Ipe.png" width=25%></div>



## Description

ここは Ipe のロコを制作している工房です。
python + matplotlib + `backend_ipe.py`　で `.ipe` ファイルを制作しています。
基本的に、文字列 Ipe のグリフを入力多角形として
計算幾何学で代表的なトピックでいろいろと図形を描画しています。
Ipe をモチーフにしているのは日頃の感謝の表明です。
計算幾何学のトピックから選んで作成している理由は Ipe の作者であるオットフリードさんへのオマージュです。



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

## Gallery and stuff

### Polygonal boolean operations and Inclusion test
多角形のブール演算および多角形の包囲テストの基本を確認したかったので作成したロゴです。
出力は下図のようになります。
包囲テストは shapely 多角形のメソッドを利用しています。

- python: [point_location_with_shape_of_Ipe.py](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/point_location_with_shape_of_Ipe.py)
- ipe: [point_location_with_shape_of_Ipe.ipe](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/point_location_with_shape_of_Ipe.ipe)

<div align="center">
<img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/point_location_with_shape_of_Ipe.png" width=75%></div>




### Mesh Generation
多角形内部を三角形分割しておくと何かと便利なのでメッシュ生成モジュール triangle を利用してやってみました。今回は３０度未満の鋭角三角形を禁止するようなメッシュを生成しています。

- python: [constrained_triangulations_with_shape_of_Ipe.py](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/constrained_triangulations_with_shape_of_Ipe.py)
- ipe: [constrained_triangulations_with_shape_of_Ipe.ipe](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/constrained_triangulations_with_shape_of_Ipe.ipe)



<div align="center">
<img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/constrained_triangulations_with_shape_of_Ipe.png" width=75%></div>



### Visivility Graph
可視グラフが見たかったのでやってみました。
可視グラフの生成には Visilibity を利用しています。
英語多角形の曲線部分は頂点が密集しているので RDP アルゴリズムを適用して
いくつかの頂点を間引いています。
この際 rdp パッケージを利用しています。

- python: [visibility_graph_with_shape_of_Ipe.py](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/visibility_graph_with_shape_of_Ipe.py)
- ipe: [visibility_graph_with_shape_of_Ipe.ipe](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/visibility_graph_with_shape_of_Ipe.ipe)


<div align="center">
<img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/visibility_graph_with_shape_of_Ipe.png" width=75%></div>


### Geodesic Voronoi Diagram
Ipe 多角形内でボロノイ図が書きたかったのでやってみました。
OpenGL や GLFW を利用してボロノイ描画をカラーバッファに吐き出して
境界抽出して各母点の勢力圏多角形を取得しています。

- python: [approximated_geodesic_voronoi_in_Ipe.py](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/approximated_geodesic_voronoi_in_Ipe.py)
- ipe: [approximated_geodesic_voronoi_in_Ipe.ipe](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/approximated_geodesic_voronoi_in_Ipe.ipe)




<div align="center">
<img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/approximated_geodesic_voronoi_in_Ipe.png" width=75%></div>


### TSP art
正確には TSP アートではないのですがそれっぽい多角形を生成するコードを作成しました。
- python: [tsp_art_with_polygonalization_in_ipe.py](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/tsp_art_with_polygonalization_in_ipe.py)
- ipe: [tsp_art_with_polygonalization_in_ipe.ipe](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/tsp_art_with_polygonalization_in_ipe.ipe)


<div align="center">
<img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/tsp_art_with_polygonalization_in_ipe.png" width=75%></div>


### Quadtree
Ipe 多角形の頂点を入力として四分木を適用してみました。それだけなんですけど。
- python: [quadtree_for_shape_of_Ipe.py](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/quadtree_for_shape_of_Ipe.py)
- ipe: [quadtree_for_shape_of_Ipe.ipe](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/quadtree_for_shape_of_Ipe.ipe)


<div align="center">
<img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/quadtree_for_shape_of_Ipe.png" width=75%></div>



### Circle packing with Descartes Theorem
Ipe 多角形内部に異なる半径の円を充填してみました。
このコードは aarizat さんの [circpacker: Circle Packer](https://github.com/aarizat/circpacker/tree/master) を利用しています。
下記の python コードに必要箇所を埋め込んでいますが、普通に使うなら pip でインストールするとよいかと思います。
BSD ライセンスです。
- python: [circle_packing_with_descartes_theorem_in_Ipe.py](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/circle_packing_with_descartes_theorem_in_Ipe.py)
- ipe: [circle_packing_with_descartes_theorem_in_Ipe.ipe](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/circle_packing_with_descartes_theorem_in_Ipe.ipe)


<div align="center">
<img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/circle_packing_with_descartes_theorem_in_Ipe.png" width=75%></div>





### おしまい
今回はここまでです。
気が向いたら計算幾何学のトピックから選んでログ作成していきたいと思います。




