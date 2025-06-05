#include <iostream>
using std::cin, std::cout, std::endl;

struct Point { 
    int x;
    int y;
};

class Polygon {
    private:
        Point* vertices;   // data member for an ordered list of points
        int numVertices;   // data member for the number of points

    public:
        // constructor
        Polygon() : vertices(nullptr), numVertices(0) { }

        // destructor
        ~Polygon() { delete[] vertices; }

        // copy constructor
        Polygon(const Polygon& poly)
        {
            numVertices = poly.getNumVertices();
            Point* polyVertices = poly.getVertices();
            vertices = new Point[numVertices];

            // copy the list of points
            for (int i = 0; i < numVertices; i++)
            {
                vertices[i].x = polyVertices[i].x;
                vertices[i].y = polyVertices[i].y;
            }
        }

        // copy assignment operator
        Polygon& operator=(const Polygon& poly)
        {
            // self-assignment check
            if (this != &poly)
            {
                // deallocate memory for the existing object
                delete[] vertices;

                // update the number of vertices and reallocate
                numVertices = poly.getNumVertices();
                vertices = new Point[numVertices];

                // copy the list of points
                Point* polyVertices = poly.getVertices();
                for (int i = 0; i < numVertices; i++)
                {
                    vertices[i].x = polyVertices[i].x;
                    vertices[i].y = polyVertices[i].y;
                }
            }
            return *this;
        }

        void addVertex(int x, int y)
        {
            // resize the array
            // allocate memory to the tempory pointer
            Point* temp = new Point[numVertices + 1];

            // copy the values from the original array to new array
            for (int i = 0; i < numVertices; i++)
            {
                temp[i].x = vertices[i].x;
                temp[i].y = vertices[i].y;
            }
            // add the new vertice to the end
            temp[numVertices].x = x;
            temp[numVertices].y = y;

            // delete the old array
            delete[] vertices;

            // have vertices point to the new array and update numVertices
            vertices = temp;
            numVertices++;
        }

        Point* getVertices() const   { return vertices; }
        int getNumVertices() const   { return numVertices; }

        // outputs the list of vertices (x1,y1), (x2, y2), ...
        void print()
        {
            if (vertices != nullptr)
            {
                for (int i = 0; i < numVertices; i++)
                {
                    cout << "(" << vertices[i].x << "," << vertices[i].y << ")"; 
                    // if this is not the last vertice in the list, output ","
                    if (i < numVertices - 1)
                        cout << ", ";
                }
                cout << endl;
            }
        }  
};

int main()
{
    // define an instance of the Polygon class
    Polygon p1;
    p1.addVertex(1,2);
    p1.addVertex(2,5);
    p1.addVertex(3,4);
    p1.addVertex(3,3);

    // should output (1,2), (2,5), (3, 4), (3,3)
    cout << "Output p1: " << endl;
    p1.print();

    cout << endl << "Creating p2 from p1: " << endl;
    Polygon p2(p1);
    
    // should output (1,2), (2,5), (3, 4), (3,3)
    p2.print();

    cout << endl << "Assigning p1 to p3: " << endl;
    Polygon p3;
    p3 = p1;
    p3.addVertex(2, 2);


    // should output (1,2), (2,5), (3, 4), (3,3), (2,2)
    p3.print();

    return 0;
}
