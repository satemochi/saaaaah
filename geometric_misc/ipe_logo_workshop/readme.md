# Ipe logo workshop (unofficial)

<img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/point_location_with_shape_of_Ipe.png" width=25%><img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/constrained_triangulations_with_shape_of_Ipe.png" width=25%><img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/visibility_graph_with_shape_of_Ipe.png" width=25%><img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/approximated_geodesic_voronoi_in_Ipe.png" width=25%>
<img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/tsp_art_with_polygonalization_in_ipe.png" width=25%><img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/quadtree_for_shape_of_Ipe.png" width=25%><img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/circle_packing_with_descartes_theorem_in_Ipe.png" width=25%><img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/contour_polygons_with_shape_of_Ipe.png" width=25%>
<img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/medial_axis_with_segment_voronoi.png" width=25%><img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/art_gallery_problem_in_shape_of_ipe.png" width=25%>





## Description

This workshop specializes in creating (unofficial) logos for the drawing tool
[Ipe](https://ipe.otfried.org).
We generate `.ipe` files
using a combination of
Python, Matplotlib, and `backend_ipe.py`.
These `.ipe` files are full compatible with Ipe
for further editing.

Each subject uses the glyphs of the string "Ipe" as input polygons and
draws various objects (points, segments, circles, polygons, curves etc.)
based on typical topics in computational geometry.
This approach not only serves as a statement of gratitude for
the versatile tool Ipe but also pays tribute to its developer,
Professor [Otfried Cheong](https://otfried.org),
by exploring the rich field of computational geometry.


**Precautions**
Please note that this work is being conducted by a third party 
not affiliated with the original owner.

For any questions or requests.
please report them
[here](https://github.com/satemochi/saaaaah/issues).
Additionally, if you discover any bugs or errors in our artworks or staff,
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
[BSD licenses](https://github.com/rougier/freetype-py/blob/master/LICENSE.txt).

- Finally, for Boolean operations on polygons,
we would use
[shapely](https://github.com/shapely/shapely).
This is also
[BSD licensed](https://github.com/shapely/shapely/blob/main/LICENSE.txt).






## Gallery and stuff


### Polygonal boolean operations and Inclusion test

We begin with
[Boolean operations on polygons](https://en.wikipedia.org/wiki/Boolean_operations_on_polygons)
and
[point-in-polygon](https://en.wikipedia.org/wiki/Point_in_polygon) tests.
This logo is designed to help understand the basic usage of APIs and
data structures.
In this context, Ipe is represented as a single polygon with
two holes.
The exterior is defined by a clockwise-ordered point sequence
(where the last point is not repeat the first),
and the interiors are defined in a counter-clockwise order.

To resolve the point-in-polygon problem,
we utilized the 
[contains](https://shapely.readthedocs.io/en/stable/reference/shapely.Polygon.html#shapely.Polygon.contains)
method from `shapely`-polygon.
We have 3,000 points, each colored abased on whether they are
inside or outside of the Ipe polygon.
Although it is possible to plot more points within 10 seconds,
but resulting `.ipe` file would become
excessively large,
so we opted not to proceed for economic reasons.

- python: [point_location_with_shape_of_Ipe.py](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/point_location_with_shape_of_Ipe.py)
- ipe: [point_location_with_shape_of_Ipe.ipe](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/point_location_with_shape_of_Ipe.ipe)

<div align="center">
<img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/point_location_with_shape_of_Ipe.png" width=75%></div>







### Mesh Generation

The second step involves 
[mesh generation](https://en.wikipedia.org/wiki/Mesh_generation) or 
performing constrained
[polygon triangulation](https://en.wikipedia.org/wiki/Polygon_triangulation),
as these (geometric / combinatorial) structures are
highly beneficial for solving various problems.
We will use the [triangle](https://rufat.be/triangle/) module,
which is  licensed under
[LGPL-3](https://github.com/drufat/triangle/blob/master/LICENSE),
to create different meshes.
In this project,
we have specified that no triangles should have an angle less than 30 degrees.



- python: [constrained_triangulations_with_shape_of_Ipe.py](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/constrained_triangulations_with_shape_of_Ipe.py)
- ipe: [constrained_triangulations_with_shape_of_Ipe.ipe](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/constrained_triangulations_with_shape_of_Ipe.ipe)



<div align="center">
<img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/constrained_triangulations_with_shape_of_Ipe.png" width=75%></div>









### Visibility Graph

We just wanted to see 
[visibility graphs](https://en.wikipedia.org/wiki/Visibility_graph#:~:text=In%20computational%20geometry%20and%20robot,a%20visible%20connection%20between%20them.), then plot them!
For generating visibility graphs,
we use the module
[Visilibity](https://karlobermeyer.github.io/VisiLibity1/).
`Visilibity` is
[LGPL-3](https://github.com/karlobermeyer/VisiLibity1#license).
Since the English alphabet consists of many curved lines
and there are a lot of subdivision points on each curve,
we apply the
[RDP algorithm](https://en.wikipedia.org/wiki/Ramer–Douglas–Peucker_algorithm)
in order to decimate points within a tolerance error threshold.
For this purpose, we use the module [rdp](https://pypi.org/project/rdp/).
This is licensed under
[MIT license](https://github.com/fhirschmann/rdp/blob/master/LICENSE.txt).

- python: [visibility_graph_with_shape_of_Ipe.py](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/visibility_graph_with_shape_of_Ipe.py)
- ipe: [visibility_graph_with_shape_of_Ipe.ipe](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/visibility_graph_with_shape_of_Ipe.ipe)


<div align="center">
<img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/visibility_graph_with_shape_of_Ipe.png" width=75%></div>






### Geodesic Voronoi Diagram

We wanted to draw the tessellation under proximity in a polygon,
specifically known as  geodesic
[Voronoi diagrams](https://en.wikipedia.org/wiki/Voronoi_diagram).
All the artworks shown so far are for this application!

We created anapproximated version,
an [additively weighted](https://en.wikipedia.org/wiki/Weighted_Voronoi_diagram)
Voronoi drawing, using
[OpenGL](https://ja.wikipedia.org/wiki/OpenGL) and
[GLFW](https://en.wikipedia.org/wiki/GLFW).
Indeed, to extract polygons (Voronoi cells) for each input point,
we wrote many cones into the (OpenGL) color buffer, then
computed (8-neighbor)
[boundary tracing](https://en.wikipedia.org/wiki/Boundary_tracing)
on the image.
Therefore,
some users might be frustrated due to the pronounced zigzag errors.
Please try opening it with Ipe and zoom in and out
to confirm the significant error.



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
of Andres Ariza-Triana.
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
must be connected.
However, we are still uncertain about this approach.


- python: [art_gallery_problem_in_shape_of_ipe.py](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/art_gallery_problem_in_shape_of_ipe.py)
- ipe: [art_gallery_problem_in_shape_of_ipe.ipe](https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/art_gallery_problem_in_shape_of_ipe.ipe)

<div align="center">
<img src="https://github.com/satemochi/saaaaah/blob/master/geometric_misc/ipe_logo_workshop/art_gallery_problem_in_shape_of_ipe.png" width=75%></div>










