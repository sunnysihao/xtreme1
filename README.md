# Xtreme1 python-sdk
***
## Install with PyPi(pip)
## API-tools
    client = Client(base_url: str, access_token: str)
- `base_url`:部署地址
- `access_token`:平台的 api token
#### 创建数据集
    client.create_dataset(name: str, annotation_type: str, description: str=None)
- `name`:数据集名称
- `annotation_type`:标注类型(LIDAR_FUSION(融合标注), LIDAR_BASIC(点云标注), IMAGE(图片标注))
- `description`:描述
#### 编辑数据集
    client.edit_dataset(dataset_id: int, name: str, description: str=None)
- `dataset_id`:数据集id
- `name`:要更改的新的数据集名字
- `description`:描述
#### 删除数据集
    client.delete_dataset(dataset_id: int)
- `dataset_id`:数据集id
#### 查询一个数据集
    client.queary_dataset(dataset_id: int)
- `dataset_id`:数据集id
#### 筛选查询多个数据集()
    client.query_datasets(page_no: int, page_size: str, **kwargs)
- `page_no`:页码 
- `page_size`:显示数量
- 可选参数:
    - `name`str:数据集名字(模糊查询)
    - `createStartTime`str:创建起始时间
    - `createEndTime`str:创建截至时间
    - `sortFiled`str:排序方式(NAME, CREATED_AT, UPDATED_AT)
    - `ascOrDesc`str:正序还是逆序(ASC,DESC)
    - `type`str:标注类型(LIDAR_FUSION(融合标注), LIDAR_BASIC(点云标注), IMAGE(图片标注))
#### 上传数据集(支持单个文件、压缩包、文件夹)
    upload_file(file_source: str, dataset_id: str)
- `file_source`:本地文件资源路径
- `dataset_id`:上传数据的目标数据集id
#### 筛选查询指定数据集下的data
    client.query_data_under_dataset(dataset_id: int, page_no: int, page_size: str, **kwargs)
- `dataset_id`:数据集id
- `page_no`:页码
- `page_size`:显示数量
- 可选参数:
    - `name`str:数据集名字(模糊查询)
    - `createStartTime`str:创建起始时间
    - `createEndTime`str:创建截至时间
    - `sortFiled`str:排序方式(NAME, CREATED_AT, UPDATED_AT)
    - `ascOrDesc`str:正序还是逆序(ASC,DESC)
    - `annotationStatus`str:状态(ANNOTATED(已标注),NOT_ANNOTATED(未标注),INVALID(无效))
#### 查询单个data
    query_data(data_id: int)
- `data_id`:data id
#### 根据data id查询多个data
  query_multiple_data(data_ids: list)
- `data_ids`:多个data id的列表
#### 根据data id删除多个data
  delete_multiple_data(data_ids: list)
- `data_ids`:多个data id的列表
#### 


## Annotation-tools

## Xtreme1-Exception
### ApiException
