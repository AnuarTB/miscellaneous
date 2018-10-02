# B+ tree 

## Table of contents
1. [Project overview](#project-overview)
2. [Data properties](#data-properties)
3. [B+ tree properties](#b-tree-properties)
4. [Running the program](#running-the-program)
5. [Running the tests](#running-the-tests)

---

### <a name="project-overview"></a> Project overview 
The implementation of simple database built on top of [B+ tree](https://en.wikipedia.org/wiki/B%2B_tree). 

`main.py` - the main program for interacting with database.

`classes.py` - the module for implementing classes `Node`, `BPlusTree` and `Interface` which are used in the `main.py`.

`orders.csv` - sample data file, consisting of products' data in CSV format.

`test_bplustree.py` - module for testing the B+ tree functions.

### <a name="data-properties"></a> Data properties

The data in the csv file is represented in simple CSV format, where the first row, is the attribute vector: 
```
ProductID,ProductName,SupplierID,CategoryID,Unit,Price
```
In this table there are 77 distinct tuples. 

### <a name="b-tree-properties"></a> B+ tree properties

The B+ tree is implemented in the `classes.py` as `BPlusTree` class. 

The order of the tree is d = 4.

You can specify the attributes that will serve as key, during the runtime, by choosing two attributes. 

**Note**: The keys will be compared lexicographically. For example, it means that among keys '9' and '10', '10' will have smaller value. 

### <a name="running-the-program"></a> Running the program

To run the program execute the following command in the directory of the program, in shell. 
```shell
python main.py
```

### <a name="running-the-tests"></a> Running the tests

To test the program, the python library `unittest` was used. To see the tests you can examine `test_bplustree.py` module. To run tests, execute the following command:

```shell
python -m unittest -v test_bplustree.py
```

**NOTE**: As you might observe, only B+ tree methods are tested, as all B+ tree methods underly the program structure and serve as core component of the database. B+ tree is implemented with the forethought, that it might be used for different interfaces and purposes, so extensive test coverage of B+ tree methods is provided.   
