#pragma once 

#include "searchable_bag.hpp"


class set
{
    private:
        searchable_bag &bag;
    public:
        set(searchable_bag& bag): bag(bag){}
        set(const set &o):bag(o.bag){}
        ~set(){}

        void insert(int val)
        {
            if (!bag.has(val))
                bag.insert(val);
        }

        void insert(int *data, int size)
        {
            for (int i = 0; i < size; i++)
            {
                if (!bag.has(data[i]))
                    bag.insert(data[i]);
            }
        }

        void print() const 
        {
            bag.print();
        }

        void clear()
        {
            bag.clear();
        }

        bool has(int val) const 
        {
            return (bag.has(val));
        }

        const searchable_bag& get_bag() const 
        {
            return (bag);
        }
};