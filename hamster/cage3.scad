// Pinewood Derby "Heavy-Duty" Hamster Wheel
// Units: Inches
$fn = 60; 

// --- STRENGTH REFINEMENTS ---
wheel_diam = 3.0;
wheel_rad = wheel_diam / 2;
wheel_width = 1.0;

rim_thickness = 0.12;  // Thicker rims
rim_depth = 0.10; 

// Lattice Reinforcements
num_struts = 9;        // Half as many struts for a coarser, stronger mesh
lattice_wire_r = 0.05; // Doubled thickness (0.1" diameter wires)
twist_angle = 90;      // Reduced twist for straighter, stronger paths

// Vertical Support Reinforcements
num_pillars = num_struts * 2; 
pillar_r = 0.05;       // Doubled thickness (Matches lattice)

// Axle Hub Reinforcements
axle_diam = 0.07;      // Slightly larger for easier wire threading
hub_thickness = 0.12;  // Thicker support bars
hub_width = 0.35;      // Wider support bars

module lattice_mesh() {
    intersection() {
        cylinder(r=wheel_rad, h=wheel_width);
        union() {
            for (i = [0 : num_struts-1]) {
                // Clockwise
                rotate([0, 0, i * (360 / num_struts)])
                linear_extrude(height = wheel_width, twist = twist_angle)
                translate([wheel_rad - rim_thickness/1.5, 0, 0])
                circle(r = lattice_wire_r);
                
                // Counter-Clockwise
                rotate([0, 0, i * (360 / num_struts)])
                linear_extrude(height = wheel_width, twist = -twist_angle)
                translate([wheel_rad - rim_thickness/1.5, 0, 0])
                circle(r = lattice_wire_r);
            }
        }
    }
}

module vertical_supports() {
    for (i = [0 : num_pillars-1]) {
        rotate([0, 0, i * (360 / num_pillars)])
        translate([wheel_rad - rim_thickness/1.5, 0, 0])
        cylinder(h=wheel_width, r=pillar_r);
    }
}

module rims() {
    difference() {
        union() {
            cylinder(r=wheel_rad, h=rim_depth);
            translate([0, 0, wheel_width - rim_depth])
            cylinder(r=wheel_rad, h=rim_depth);
        }
        translate([0,0,-1])
        cylinder(r=wheel_rad - rim_thickness, h=wheel_width + 2);
    }
}

module axle_braces() {
    for (z_pos = [rim_depth/2, wheel_width - rim_depth/2]) {
        translate([0, 0, z_pos])
        difference() {
            union() {
                cube([wheel_diam - 0.1, hub_width, hub_thickness], center=true);
                cylinder(r=hub_width/1.6, h=hub_thickness, center=true);
            }
            cylinder(r=axle_diam/2, h=hub_thickness+0.1, center=true);
        }
    }
}

module wheel_assembly() {
    union() {
        rims();
        lattice_mesh();
        vertical_supports();
        axle_braces();
    }
}

// --- RENDER ---
color("orange")
wheel_assembly();

echo("Strut pairs:", num_struts);
echo("Wire Thickness (Diameter):", lattice_wire_r * 2);