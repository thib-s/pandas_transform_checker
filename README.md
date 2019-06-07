# Pandas transform checker

## what is it ?

This library is focused on data quality checking on pandas transformations.
Transformations are functions that takes a pandas DataFrame as input ( plus
other params ) and output a DataFrame.

This library allow the user to specify a contract that the function must respect.
In this contract the user can specify:
 - the added columns
 - the deleted columns
 - the modified columns
 - if the function add/drop records
 - if the function modify the index ( ex: resampling )

Once the contract if specified, the function will raise a RuntimeError
if one of it's specifications is violated.

## how to use it ?

The package contains the decorator that performs the check it can be 
imported the following way:
```
from pandas_transform_checker.decorator_contract_checker import input_df_contract
```

### Args

df_param: name of the param of the function that is the input df
contract_params: dict defining the contract of the function in the following format:
```
contract_dict = {
    "col_additions": {
        "col_a": "int",
        "col_b": "float"
    },
    "col_deletions": {
        "col_c",
        "col_d"
    },
    "col_editions": {
        "col_e",
        "col_f"
    },
    "allow_index_edition": False,
    "allow_drop_record": True
}
```
which means that the function must create "col_a", "col_b", delete "col_c", "col_d", must
not modify any column data except "col_e", "col_f", and must not edit the index

here is the list of keys allowed in this dict:
- col_additions: dict where keys are column names and values are dtypes (string)
- col_deletions: set of str representing the deleted columns
- col_editions: set of str representing the modified columns
- allow_index_edition: bool indicating if the function modify the index
- allow_add_drop_record (bool): indicate if the function can drop some records (ex. when dropna is used)

### Usage
when you have a function that takes a df as input:
```
def super_func(df_input):
    ...
```
just add the annotation to automatically check properties
```
@input_df_contract(df_param="df_input", contract_dict={"col_editions": {"col_e","col_f"}})
def super_func(df_input):
    ...
```