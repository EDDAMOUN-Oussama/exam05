// #pragma once

// #include <iostream>
// #include <string>
// #include <algorithm>

// class bigint
// {
//     private:
//         std::string val;
//     public:
//         bigint():val("0"){}
//         bigint(size_t n):val(std::to_string(n)){}
//         bigint (const bigint& other): val(other.val){}
//         bigint &operator=(const bigint& other)
//         {
//             if (this != &other)
//                 val = other.val;
//             return (*this);
//         }
//         ~bigint(){}



//         friend std::ostream& operator<<(std::ostream &os, const bigint &bg)
//         {
//             return ((os << bg.val));
//         }

//         bigint operator+(const bigint& other) const
//         {
//             int s1, s2, sum;
//             int  a, b, carr;
//             bigint res;
//             char digit;

//             s1 = val.size() - 1;
//             s2 = other.val.size() - 1;
//             res.val.clear();
//             carr = 0;
//             while (s1 >= 0 || s2 >= 0 || carr)
//             {
//                 if (s1 >= 0)
//                     a = val[s1] - '0';
//                 else
//                     a = 0;
//                 if (s2 >= 0)
//                     b = other.val[s2] - '0';
//                 else
//                     b = 0;
//                 sum = a + b + carr;
//                 digit = sum % 10 + '0';
//                 carr = sum / 10;
//                 res.val += digit;
//                 s1--;
//                 s2--;
//             }
//             std::reverse(res.val.begin(), res.val.end());
//             return (res);
//         }

//         bigint& operator+=(const bigint& other)
//         {
//             *this = (*this) + other;
//             return (*this);
//         }

//         bigint& operator++() //++a
//         {
//             *this += (bigint) 1;
//             return (*this);
//         }

//         bigint operator++(int) //a++
//         {
//             bigint tmp(*this);
//             ++(*this);
//             return tmp;
//         }



//         bool operator==(const bigint& other) const
//         {
//             return (val == other.val);
//         }

//         bool operator!=(const bigint& other) const 
//         {
//             return (!((*this) == other));
//         }

//         bool operator>(const bigint& other) const
//         {
//             if (val.size() != other.val.size())
//                 return (val.size() > other.val.size());
//             return (val > other.val);
//         }

//         bool operator<(const bigint& other) const 
//         {
//             return (other > (*this));
//         }

//         bool operator>=(const bigint &other) const
//         {
//             return (!((*this) < other));
//         }

//         bool operator<=(const bigint& other) const
//         {
//             return (!((*this) > other));
//         }







//         bigint &operator<<=(size_t n)
//         {
//             if ((*this) != bigint(0))
//                 val.append(n, '0');
//             return (*this);
//         }

//         bigint operator<<(size_t n) const
//         {
//             bigint tmp(*this);
//             tmp <<= n;
//             return (tmp);
//         }

//         bigint &operator>>=(const bigint &n)
//         {
//             if (bigint(val.size()) <= n)
//                 val = "0";
//             else
//             {
//                 bigint i;
//                 while (i < n)
//                 {
//                     val.erase(val.size() - 1);
//                     i++;
//                 }
//             }
//             return (*this);
//         }
// };


































#pragma once

#include <iostream>
#include <string>
#include <algorithm>

class bigint
{
    private:
        std::string val;
    public:
    bigint():val("0"){}
    bigint(size_t n): val(std::to_string(n)){}
    bigint (const bigint & o): val(o.val){}
    bigint &operator=(const bigint& o)
    {
        if (this != &o)
            val = o.val;
        return (*this);
    }
    ~bigint(){}


    friend std::ostream &operator<<(std::ostream &os, const bigint &bg)
    {
        os << bg.val;
        return (os);
    }


    bigint operator+(const bigint &o) const 
    {
        int s1 = val.size() -1;
        int s2 = o.val.size() -1;
        int sum, carr = 0;
        int a, b;
        char digit;
        bigint res;

        res.val.clear();

        while (s1 >= 0 || s2 >= 0 || carr)
        {
            a = b = 0;
            if (s1 >= 0)
                a = val[s1] - '0';
            if (s2 >= 0)
                b = o.val[s2] - '0';
            sum = a + b + carr;
            digit = sum % 10 + '0';
            carr = sum / 10;
            res.val += digit;
            s1--;
            s2--;
        }
        std::reverse(res.val.begin(), res.val.end());
        return (res);
    }

    bigint &operator+=(const bigint & o)
    {
        (*this) = (*this) + o;
        return (*this);
    }

    bigint &operator++() // ++a
    {
        (*this) += (bigint)1;
        return (*this);
    }

    bigint operator++(int) //a++
    {
        bigint tmp(*this);
        ++(*this);
        return (tmp);
    }


    bool operator==(const bigint &o) const
    {
        return (val == o.val);
    }

    bool operator!=(const bigint &o) const 
    {
        return (!((*this) == o));
    }

    bool operator>(const bigint &o) const
    {
        if (val.size() != o.val.size())
            return (val.size() > o.val.size());
        return (val > o.val);
    }

    bool operator<(const bigint & o) const
    {
        return (o > (*this));
    }

    bool operator>=(const bigint &o) const
    {
        return (!((*this) < o));
    }

    bool operator<=(const bigint &o) const
    {
        return (!((*this) > o));
    }



    bigint& operator<<=(size_t n)
    {
        if ((*this) != bigint(0))
            val.append(n, '0');
        return (*this);
    }

    bigint operator<<(size_t n) const
    {
        bigint tmp(*this);
        tmp <<= n;
        return (tmp);
    }

    bigint& operator>>=(const bigint n)
    {
        if (bigint(val.size()) <= n)
            val = "0";
        else
        {
            bigint i;
            while (i < n)
            {
                val.erase(val.size() -1);
                i++;
            }
        }
        return (*this);
    }

};