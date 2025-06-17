# Ipe logo workshop (unofficial)

<img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/point_location_with_shape_of_Ipe.png" width=25%><img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/constrained_triangulations_with_shape_of_Ipe.png" width=25%><img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/visibility_graph_with_shape_of_Ipe.png" width=25%><img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/approximated_geodesic_voronoi_in_Ipe.png" width=25%>
<img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/tsp_art_with_polygonalization_in_ipe.png" width=25%><img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/quadtree_for_shape_of_Ipe.png" width=25%><img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/circle_packing_with_descartes_theorem_in_Ipe.png" width=25%><img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/contour_polygons_with_shape_of_Ipe.png" width=25%>
<img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/medial_axis_with_segment_voronoi.png" width=25%><img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/art_gallery_problem_in_shape_of_ipe.png" width=25%>





## Description

This is a workshop that produces (unofficial) logos for the draw tool
[Ipe](https://ipe.otfried.org).
We have produced outputs as `.ipe` files with
python + matplotlib + `backend_ipe.py`.
The .ipe files published here can be opened and edited by Ipe.

Each subject uses the glyphs of the string "Ipe" as input polygons, and
draws various objects (points, segments, circles, polygons, curves etc.)
based on typical topics in computational geometry.
The reason for using Ipe as a motif is a statement of gratitude.
The reason for choosing a topic in computational geometry as the theme
is a tribute to the author of Ipe,
professor [Otfried Cheong](https://otfried.org).


**Precautions**
This work is being done by a third party who is not affiliated with
the original owner.
You can report [here](https://github.com/satemochi/saaaaah/issues)
for any questions and requests.
In addition, if you have found any bugs and errors in our artworks or staff,
we would appreciate your report.



## Polygon generation for each input


We would like to mention fonts and tools we used during
the input generation phase.

- For the font,
we would use [Alice font](https://fonts.google.com/specimen/Alice/license).
This is licensed under [Open Font License](https://openfontlicense.org).

- For managing the combinatorial structure behind the geometric structure,
we use [networkx](https://networkx.org).
`networkx` is licensed under the
[BSD license](https://raw.githubusercontent.com/networkx/networkx/master/LICENSE.txt).

- For extracting outlines of font-glyphs, we would use
[glyph-vector.py](https://github.com/rougier/freetype-py/blob/master/examples/glyph-vector.py) (slightly modified) of
[freetype-py](https://github.com/rougier/freetype-py).
This is
[BSD license](https://github.com/rougier/freetype-py/blob/master/LICENSE.txt).

- Finally, for Boolean operations on polygons,
we would use
[shapely](https://github.com/shapely/shapely).
This is also
[BSD license](https://github.com/shapely/shapely/blob/main/LICENSE.txt).




## Gallery and stuff



### Polygonal boolean operations and Inclusion test

[Boolean operations on polygons](https://en.wikipedia.org/wiki/Boolean_operations_on_polygons)
and [point-in-polygon](https://en.wikipedia.org/wiki/Point_in_polygon#:~:text=In%20computational%20geometry%2C%20the%20point,%2Daided%20design%20(CAD).&text=An%20early%20description%20of%20the,of%20the%20Ray%20Tracing%20News.)
are our first step.
This logo is for understanding the basic usage of APIs and data structures.
So, Ipe is as single polygon with two holes.
The exterior is a clockwise-ordered point sequence
(the last point is not the first), and the interiors are counter-clockwise).

For resolving point-in-polygon,
we have used `shapely`-polygon's method
[contains](https://shapely.readthedocs.io/en/stable/reference/shapely.Polygon.html#shapely.Polygon.contains).
There are 3,000 points colored according to the inside/outside of Ipe.
It could plot more points within 10 seconds,
but file `.ipe` will become too large, so we gave up in an economic sense.

- python: [point_location_with_shape_of_Ipe.py](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/point_location_with_shape_of_Ipe.py)
- ipe: [point_location_with_shape_of_Ipe.ipe](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/point_location_with_shape_of_Ipe.ipe)

<div align="center">
<img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/point_location_with_shape_of_Ipe.png" width=75%></div>







### Mesh Generation

The second step is 
[mesh generation](https://en.wikipedia.org/wiki/Mesh_generation) /
(constrained)
[polygon triangulation](https://en.wikipedia.org/wiki/Polygon_triangulation),
since this (geometric / combinatorial) structure is so useful and fruitful
for solving other problems.
We would use the module
[triangle](https://rufat.be/triangle/)
for various meshes.
`triangle` is licensed under
[LGPL-3](https://github.com/drufat/triangle/blob/master/LICENSE).
In this artwork,
we have specified to restrict no triangles with less than 30 degree angle.


- python: [constrained_triangulations_with_shape_of_Ipe.py](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/constrained_triangulations_with_shape_of_Ipe.py)
- ipe: [constrained_triangulations_with_shape_of_Ipe.ipe](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/constrained_triangulations_with_shape_of_Ipe.ipe)



<div align="center">
<img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/constrained_triangulations_with_shape_of_Ipe.png" width=75%></div>









### Visibility Graph

We just wanted to see 
[visibility graphs](https://en.wikipedia.org/wiki/Visibility_graph#:~:text=In%20computational%20geometry%20and%20robot,a%20visible%20connection%20between%20them.), then plot it!
For generating visibility graphs,
we use the module
[Visilibity](https://karlobermeyer.github.io/VisiLibity1/).
`visilibity` is
[LGPL-3](https://github.com/karlobermeyer/VisiLibity1#license).
Since English alphabet consist of many curved lines
and there are a lot of subdivision points on each curve,
we apply 
[RDP algorithm](https://en.wikipedia.org/wiki/Ramer–Douglas–Peucker_algorithm)
in order to decimate points within a tolerance error threshold.
For this purpose, we use the module [rdp](https://pypi.org/project/rdp/).
This is
[MIT license](https://github.com/fhirschmann/rdp/blob/master/LICENSE.txt).

- python: [visibility_graph_with_shape_of_Ipe.py](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/visibility_graph_with_shape_of_Ipe.py)
- ipe: [visibility_graph_with_shape_of_Ipe.ipe](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/visibility_graph_with_shape_of_Ipe.ipe)


<div align="center">
<img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/visibility_graph_with_shape_of_Ipe.png" width=75%></div>






### Geodesic Voronoi Diagram

We wanted to draw the territory under control in a polygon,
that is (geodesic)
[Voronoi diagrams](https://en.wikipedia.org/wiki/Voronoi_diagram).
All artworks shown so far are for this application!

We drew approximated version,
[additively weighted](https://en.wikipedia.org/wiki/Weighted_Voronoi_diagram)
Voronoi drawing, with 
[OpenGL](https://ja.wikipedia.org/wiki/OpenGL) and
[GLFW](https://en.wikipedia.org/wiki/GLFW).
Indeed, for extracting polygons (Voronoi region) for each input point,
we have written a lot of cones into (OpenGL) color buffer, then
computed (8-neighbor)
[boundary tracing](https://en.wikipedia.org/wiki/Boundary_tracing)
on the picture.
Therefore,
someone might be angered because of the hard zigzag errors.
Please try to open it with Ipe and zoom in and out
to confirm the fatal error.



- python: [approximated_geodesic_voronoi_in_Ipe.py](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/approximated_geodesic_voronoi_in_Ipe.py)
- ipe: [approximated_geodesic_voronoi_in_Ipe.ipe](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/approximated_geodesic_voronoi_in_Ipe.ipe)



<div align="center">
<img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/approximated_geodesic_voronoi_in_Ipe.png" width=75%></div>






### TSP art
Precisely, this artwork is not a
[TSP art](https://www2.oberlin.edu/math/faculty/bosch/tspart-page.html),
but we wrote a code that generates a visual similar to it,
specifically creating at least one stroke polygon on a given triangulation.

According to
[depth first search](https://en.wikipedia.org/wiki/Depth-first_search),
triangles are concatenated; however,
the rule with
[breadth first search](https://en.wikipedia.org/wiki/Breadth-first_search)
might result in a smaller perimeter,
which could be more TSP alike,
but we don't know.

- python: [tsp_art_with_polygonalization_in_ipe.py](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/tsp_art_with_polygonalization_in_ipe.py)
- ipe: [tsp_art_with_polygonalization_in_ipe.ipe](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/tsp_art_with_polygonalization_in_ipe.ipe)


<div align="center">
<img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/tsp_art_with_polygonalization_in_ipe.png" width=75%></div>







### Quadtree

We applied [quadtree](https://en.wikipedia.org/wiki/Quadtree)
data structure for vertices of the Ipe polygon.
That's it!

- python: [quadtree_for_shape_of_Ipe.py](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/quadtree_for_shape_of_Ipe.py)
- ipe: [quadtree_for_shape_of_Ipe.ipe](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/quadtree_for_shape_of_Ipe.ipe)


<div align="center">
<img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/quadtree_for_shape_of_Ipe.png" width=75%></div>








### Circle packing with Descartes Theorem

We tried to [pack circles](https://en.wikipedia.org/wiki/Circle_packing)
with different radii into the Ipe polygon.
This code has been embedded a part of (modified)
[circpacker: Circle Packer](https://github.com/aarizat/circpacker/tree/master)
by Andres Ariza-Triana.
`circpacker` is BSD license.


- python: [circle_packing_with_descartes_theorem_in_Ipe.py](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/circle_packing_with_descartes_theorem_in_Ipe.py)
- ipe: [circle_packing_with_descartes_theorem_in_Ipe.ipe](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/circle_packing_with_descartes_theorem_in_Ipe.ipe)


<div align="center">
<img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/circle_packing_with_descartes_theorem_in_Ipe.png" width=75%></div>





### Contour polygons with Minkowski sums

We wanted to draw something like contour lines inside the Ipe polygon.
It is fun to use `shapely.buffer` 
([api](https://shapely.readthedocs.io/en/stable/reference/shapely.buffer.html))
to easily obtain
[Minkowski sums](https://en.wikipedia.org/wiki/Minkowski_addition).
The Boolean product of the polygons (the original with the buffered polygon)
is taken to make the contour lines come inside the polygons.
Eleven such buffered polygons are drawn.


- python: [contour_polygons_with_shape_of_Ipe.py](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/contour_polygons_with_shape_of_Ipe.py)
- ipe: [contour_polygons_with_shape_of_Ipe.ipe](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/contour_polygons_with_shape_of_Ipe.ipe)

<div align="center">
<img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/contour_polygons_with_shape_of_Ipe.png" width=75%></div>








### Medial axis with Voronoi diagrams for segments

We wanted to take [medial axis](https://en.wikipedia.org/wiki/Medial_axis)
of the Ipe polygon.
The error was so bad that it made us dizzy,
but we decided ok because it looked somewhat like Moomin.

We need to design more carefully how to subdivide each line segment and
which ridges to keep from the resulting Voronoi diagram.
We think the imbalance between curvature and subdivision granularity is
causing each vertex of the curve section to be corner-qualified from
a micro perspective.
With adjustment, the whiskers can be reduced considerably.

In this artwork, computing Voronoi diagrams can be done by the package
[Scipy](https://scipy.org).
Scipy is [BSD license](https://github.com/scipy/scipy/blob/main/LICENSE.txt).



- python: [medial_axis_with_segment_voronoi.py](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/medial_axis_with_segment_voronoi.py)
- ipe: [medial_axis_with_segment_voronoi.ipe](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/medial_axis_with_segment_voronoi.ipe)

<div align="center">
<img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/medial_axis_with_segment_voronoi.png" width=75%></div>




### Art Gallery Problem with vertex-guards 

We wanted to do something with
[visibility polygons](https://en.wikipedia.org/wiki/Visibility_polygon).
So, we tried the
[art gallery problem](https://en.wikipedia.org/wiki/Art_gallery_problem)
with the Ipe polygon.
Visibility polygons can be computed by using the module
[Visilibity](https://karlobermeyer.github.io/VisiLibity1/)
as well as visibility graph.
Again, `visilibity` is 
[LGPL-3 license](https://github.com/karlobermeyer/VisiLibity1#license).

One of the optimal configuration of guards can be computed by the modules
[PuLP + COIN-OR CLP](https://pypi.org/project/PuLP/),
the solver of (mixed) integer linear programming.
These may be
[MIT license](https://github.com/coin-or/pulp/blob/master/LICENSE).
Indeed, we have formulated with
[dominating set problem](https://en.wikipedia.org/wiki/Dominating_set)
on the visibility graph of the Ipe polygon.
However, instead of considering the ordinal dominating set,
we might need to reformulate our approach by adding constraints
to ensure that the subgraph of the visibility graph,
induced by points in the set,
is connected.
However, we are still uncertain about this approach.


- python: [art_gallery_problem_in_shape_of_ipe.py](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/art_gallery_problem_in_shape_of_ipe.py)
- ipe: [art_gallery_problem_in_shape_of_ipe.ipe](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/art_gallery_problem_in_shape_of_ipe.ipe)

<div align="center">
<img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/art_gallery_problem_in_shape_of_ipe.png" width=75%></div>










