#pragma once

#include <iostream>
#include <string>

class vect2
{
    private:
        int x;
        int y;
    public:
        vect2():x(0), y(0){}
        vect2(int a, int b):x(a), y(b){}
        vect2(const vect2 &o):x(o.x), y(o.y){}
        vect2 &operator=(const vect2 &o)
        {
            if (this != &o)
            {
                x = o.x;
                y = o.y;
            }
            return (*this);
        }
        
        friend std::ostream& operator<<(std::ostream &os, const vect2 &v)
        {
            os << "{" << v.x << ", " << v.y << "}";
            return (os);
        }

        friend vect2 operator*(const int a, const vect2& v)
        {
            return (vect2(a * v.x, a * v.y));
        }

        int operator[](int n) const
        {
            if (n == 0)
                return (x);
            return (y);
        }

        int& operator[](int n)
        {
            if (n == 0)
                return (x);
            return (y);
        }

        vect2 & operator++() //++a
        {
            x++;
            y++;
            return (*this);
        }
        
        vect2 operator++(int) //a++
        {
            vect2 tmp(*this);
            ++(*this);
            return (tmp);
        }

        vect2 & operator--() //--a
        {
            x--;
            y--;
            return (*this);
        }

        vect2 operator--(int) //a--
        {
            vect2 tmp(*this);
            --(*this);
            return (tmp);
        }

        vect2 operator+(const vect2 &o) const
        {
            return (vect2(x + o.x, y + o.y));
        }

        vect2& operator+=(const vect2 &o)
        {
            (*this) = (*this) + o;
            return (*this);
        }

        vect2 operator-(const vect2 &o) const
        {
            return (vect2(x - o.x, y - o.y));
        }

        vect2& operator-=(const vect2 &o)
        {
            (*this) = (*this) - o;
            return (*this);
        }

        vect2 operator*(const int a) const
        {
            return (vect2(x * a, y * a));
        }

        vect2& operator*=(const int a)
        {
            (*this) = (*this) * a;
            return (*this);
        }

        vect2 operator-() const
        {
            return (vect2(-x, -y));
        }

        bool operator==(const vect2 &o) const
        {
            return (x == o.x && y == o.y);
        }

        bool operator!=(const vect2 &o) const
        {
            return (x != o.x && y != o.y);
        }

};