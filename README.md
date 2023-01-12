# Xtreme1 Python SDK

## Installation

~~~python
pip install xtrame1
~~~

---

## Usage

```python
from xtreme1.client import Client

BASE_URL = 'https://x1-community.alidev.beisai.com'
ACCESS_TOKEN = '...jDC9Pfk9Xstt9vaanXkh8...'

client = Client(base_url=BASE_URL, access_token=ACCESS_TOKEN)
```
---

### Datasets

暂空

#### Create a dataset

You can use this method to create a dataset.

For now, supported annotation types are: **['LIDAR_FUSION', 'LIDAR_BASIC', 'IMAGE']**.

```python
car_dataset = client.create_dataset(name='test', annotation_type='IMAGE', description='A test dataset.')
```
#### Edit a dataset

You can use this method to change the information of your dataset.

```python
info = client.edit_dataset(dataset_id='999999', new_name='cars')
print(info) # Success

# Or use 'dataset.edit()'
car_dataset.edit(new_name='cars')
```
#### Delete a dataset

You can use this method to delete your dataset.

Notice that if you are really sure to do this, change the 'is_sure' parameter to **True**.

```python
info = client.delete_dataset(dataset_id='999999', is_sure=True)
print(info) # Success

# or use 'dataset.delete()'
car_dataset.delete(is_sure=True)
```
#### Query dataset

You can use this method to query a dataset or a list of datasets.

Notice that this method always returns a list even if there is only one dataset.

There are two important parameters: 'page_no' and 'page_size'. The querying result is splitted into pages like an iterator. You can change 'page_size' to get more or fewer datasets at a time and change 'page_no' to load the next page of all querying results.

```python 
# Query one single dataset by passing a dataset id
dataset_list = client.query_dataset(dataset_id='888888')
print(dataset_list) # [BFDataset(id=888888, name=driver_dataset)]

# Query a list of datasets with some filters
dataset_list = client.query_dataset(
    page_no = 1, # default 1
    page_size = 3, # default 1
    dataset_name = 'car', # fuzzy query
    create_start_time = (2022, 1, 1),
    create_end_time = (2023, 1, 1),
    sort_by = 'CREATED_AT', # ['NAME', 'CREATED_AT', 'UPDATED_AT']
    ascending = True,
    dataset_type = 'LIDAR_FUSION'
)
print(dataset_list)
"""
[BFDataset(id=888000, name=car_dataset1),
 BFDataset(id=888001, name=car_dataset2),
 BFDataset(id=888002, name=car_dataset3)]
"""
```
#### Query data under the dataset

This method is similar to the above one.

It returns a long dict. If you want to simplify this dict, use 'get_values()' to select specific keys in the dict. After that, you can use 'as_table()' to show the data in tabular form and use 'rich.print()' to print this table.

```python
from xtreme1.array_funcs import get_values, as_table
from rich import print as rprint

data_dict = client.query_data_under_dataset(
	dataset_id = '888888',
    page_no = 1, # default 1
    page_size = 10, # default 10
    name = None,
    create_start_time = None,
    create_end_time = None,
    sort_by = 'CREATED_AT',
    ascending = True,
    annotation_status = 'ANNOTATED' # ['ANNOTATED', 'NOT_ANNOTATED', 'INVALID']
)

# Or use 'dataset.query_data(...)'
data_dict = car_dataset.query_data(page_size=10)

# Simplify the dict
simple_data = get_values(
    data_dict['list'], 
    # Tuple ('content', 'name:1') means the 'name' key is under the 'content' key
    # If you don't use the '1' in 'name:1', it returns all the names in one list
    needed_keys=['id', ('content', 'name:1'), 'url:1'] 
)
print(simple_data)
"""
[[111111, '001.png', 'https://xxx'],
 [111112, '002.png', 'https://xxx'],
 [111113, '003.png', 'https://xxx'],
 ...],
"""

# Turn the list to a table
# Ignore the 'headers' parameter if your data is a dict
result_table = as_table(simple_data, headers=['data_id', 'file_name', 'url'])
rprint(result_table)
```
---

### Data

Data ≠ File! Data is the unit of your annotation work. For example:

- For an 'IMAGE' dataset, a copy of data means an independent image.
- For a 'LIDAR_BASIC' dataset, a copy of data means a pcd file.
- However, for a 'LIDAR_FUSION' dataset, a copy of data means **a pcd file + a camera config file + several images** because all these files together make an annotation work.

#### Query specific data

You can use this method to query specific data by passing a 'data_id' parameter.

Unlike the 'query_data_under_dataset()' method, this method returns all querying data at a time.

```python
data_list = client.query_data(data_id=['111110', '111111'])
```
#### Delete data

You can use this method to delete data. It's similar to the 'delete_dataset()' method.

~~~python
client.delete_data(dataset_id='888888', data_id=['111110', '111111'], is_sure=True)
~~~

#### Upload data

You can use this method to push data to a dataset by using a local path or URL.

This method always returns a serial number, which is used to query the upload status.

~~~python
serial_number = client.upload_data('test.zip', '888888')
print(serial_number) # 16134xxxxx836416

status = client.query_upload_status('16134xxxxx836416')
print(status)
"""
[{'id': 888,
  'serialNumber': '16134xxxxx836416',
  'errorMessage': '',
  'totalFileSize': 11111,
  'downloadedFileSize': 11111,
  'totalDataNum': 1,
  'parsedDataNum': 1,
  'status': 'PARSE_COMPLETED'}]
"""
~~~



#### 根据data id删除多个data
  delete_multiple_data(data_ids: list)
- `data_ids`:多个data id的列表
#### 


## Annotation-tools

## Xtreme1-Exception
### ApiException
