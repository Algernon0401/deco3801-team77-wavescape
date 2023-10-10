/**
    Created by Samuel Sticklen (46962487)
*/
thickness = 1.5;
size = 60;
module shape_rectangle() {
    cube([size, size, thickness]);
}

module shape_cylinder() {
    cylinder(thickness, size/2, size/2);
}

module shape_triangle() {
    cylinder(thickness, size/2, size/2, $fn=3);
}

module shape_arrow() {
    rotate([0,0,45]) {
        cube([size/2+10, 10, thickness]);
    }
    rotate([0,0,-45]) {
        cube([size/2, 10, thickness]);
    }
}

module shape_plus() {
    cube([size, size/6, thickness], center=true);
    cube([size/6, size, thickness], center=true);
}

module shape_star(points=5) {
    cylinder(thickness, size/4, size/4, $fn=points);
    
    for (i=[0:1:points]) {
        rotate([0,0,i*(360/points)]) {
            translate([size/4,0,0]) {
            cylinder(thickness, size/4, size/4, $fn=3);
            }
        }
    }
}

shape_plus();