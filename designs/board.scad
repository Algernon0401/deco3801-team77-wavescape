module mimic_board() {
    cube([74.04, 53, 5]);
    translate([-1, 3, 2]) {
        cube([14.5, 9.13, 12]);
    }
    translate([14.5, 1, 5]) {
        cube([58, 2, 26]);
    }
    translate([14.5, 50, 5]) {
        cube([58, 2, 26]);
    }
    translate([-6.34, 32.4, 2]) {
        cube([16.4, 12.3, 12]);
    }
    
    translate([14.5, 5, 5]) {
        cube([58, 43, 10]);
    }
}

module potentiometer() {
    cylinder(6, 9, 9, $fn=20);
    cylinder(8, 5, 5, $fn=20);
    difference() {
        cylinder(35, 2.5, 2.5, $fn=20);
        translate([1,-3,20]) {
            cube([5, 6, 16]);
        }
    }
}

module potentiometer_holder() {
    difference() {
        translate([-10, -17, 0]) {
            cube([20, 30, 6]);
        }
        translate([0,0,0]) {
            cylinder(9, 9.5, 9.5, $fn=30);
        }
        translate([-9,-20,-1]) {
             cube([18, 15, 8]);
        }
    }
}

// potentiometer();

module mounting_holes(w,d,h,t,tt) {
    translate([-t*2,3*d/4,h+tt/2-t]) {
        rotate([0,90,0]) {
                cylinder(w+t*8, 2, 2, $fn=20);
        }
    }
    translate([-t*2,d/4,h+tt/2-t]) {
        rotate([0,90,0]) {
                cylinder(w+t*8, 2, 2, $fn=20);
        }
    }
}
module frame_join(w,d,h,t=1.5,tt=4) {
    difference() {
    hull() {
        cube([w,d,1]);
        translate([-t,-t,h-t]) {
            cube([w+t*2,d+t*2, tt]); 
        }
    }
    translate([0,0,-1]) {
        cube([w,d,h+2+tt]);
    }
    mounting_holes(w,d,h,t,tt);
    }
    
    
}

module board_base() {
    difference() {
        cube([79, 58, 25]);
        translate([1.8, 1.8, 1.5]) {
            cube([79-3.6, 58-3.6, 25.5]);
        }
        translate([-2, 4, 2]) {
            cube([14.5, 12.13, 16]);
        }
        translate([-2, 33, 2]) {
            cube([14.5, 16.13, 16]);
        }
    }
    
    translate([0,0,24]) {
        difference() {
        frame_join(79, 58, 4, 1.5, 6);
        }
    }
}

module board_input_holder() {
    translate([15,8+42/2,0]) {
        potentiometer();
        potentiometer_holder();
    };
    translate([45,8+42/2,0]) {
        potentiometer();
        potentiometer_holder();
    };
    difference() {
    translate([1,8,0]) {
        cube([77, 42, 2]);
        cube([1.5, 42, 7.5]);
        translate([75.5, 0, 0]) {
            cube([1.5, 42, 7.5]);
        }
    }
    mounting_holes(79, 58, 4, 1.5, 5);
    }
}

module board_top() {
    h = 13;
    translate([-2, -2, 0]) {
        difference() {
            cube([86, 65, h]);
            translate([1.5,1.5, -0.5]) {
                cube([86-3, 65-3, h-2]);
            }
            translate([18.5, 32.5, -1]) {
                cylinder(h*2, 3, 3, $fn=20);
            }
            translate([48.5, 32.5, -1]) {
                cylinder(h*2, 3, 3, $fn=20);
            }
            translate([0, 3.5, -0]) {
                mounting_holes(79, 58, 2, 1.5, 5);
            }
        };
        
     }
}

board_base();

translate([0, 0,25]) {
    board_input_holder();
}

translate([-1.5, -1.5, 36.5]) {
        board_top();
}

translate([2.5,2.5,2]) {
    //mimic_board(); // For debugging reasons
}