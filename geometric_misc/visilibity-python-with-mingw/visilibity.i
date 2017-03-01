%module visilibity

%{
#include "visilibity.hpp"
%}

%include std_vector.i
namespace std {
        %template(pointList) vector<VisiLibity::Point>;
        %template(polygonList) vector<VisiLibity::Polygon>;
}

%include visilibity.hpp

%extend VisiLibity::Polygon {
        Point __getitem__(unsigned i) {
                return (*self)[i];

        }
};
