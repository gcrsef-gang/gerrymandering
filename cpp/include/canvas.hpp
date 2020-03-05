#include "shape.hpp"
#include <SDL2/SDL.h>

namespace GeoDraw {
    
    class Color {
        int r, g, b;

        public:

        void set_color(int rx, int gx, int bx) {
            r = rx;
            g = gx;
            b = bx;
        }

        Color();
        Color(std::string hex);
        Color(int rx, int gx, int bx) : r(rx), g(gx), b(bx) {};
    };

    class Pixel {
        Color color;
        int x, y;

        public:
        Pixel(int ax, int ay, Color c) : x(ax), y(ay), color(c) {}
        void draw();
    };

    class Outline {
        public:
            GeoGerry::LinearRing border;
            Color color;
            int line_thickness;
            bool filled;

            Outline(GeoGerry::LinearRing lr, Color c, int th, bool f) :
                border(lr), color(c), line_thickness(th), filled(f) {}
    };

    class Canvas {
        /*
            A class for storing information about a screen
            of pixels and shapes to be written to an SDL display
        */

        private:
        // contents of the canvas
        std::vector<Outline> outlines;               // shapes to be drawn individually
        std::vector<Outline> holes;                  // shapes to be drawn individually
        GeoGerry::bounding_box get_bounding_box();   // calculate bounding box of coordinates

        // modify canvas attributes
        void translate(long int x, long int y);      // move the outlines by x and y
        void scale(double scale_factor);             // scale the shapes by scale factor
        void rasterize_shapes();                     // determine pixel positions and values for coordiantes
        void rasterize_edges();                      // generate edges

        // meta information
        int x, y;                         // dimensions of the screen
        std::vector<Pixel> pixels;        // the pixel array to write to screen
        GeoGerry::bounding_box box;       // the outer bounding box

        public:
        Canvas(int dx, int dy) : x(dx), y(dy) {};

        // add shape to the canvas
        void add_shape(GeoGerry::Shape s, bool = true, Color = Color(0,0,0), int = 1);
        void add_shape(GeoGerry::LinearRing s, bool = true, Color = Color(0,0,0), int = 1);
        void add_shape(GeoGerry::Multi_Shape s, bool = true, Color = Color(0,0,0), int = 1);
        void add_shape(GeoGerry::Precinct_Group s, bool = true, Color = Color(0,0,0), int = 1);
        
        void resize_window(int x, int y);
        void draw();
    };

    class Anim {
        std::vector<Canvas> frames;
        int delay;

        void playback();
    };
}