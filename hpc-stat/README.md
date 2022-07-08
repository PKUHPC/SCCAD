## 集群状态信息可视化系统

### 部署流程
1、更新语言文件
语言文件更新流程
- 更新html或py文件
- 更新messages.pot  ```pybabel extract -F babel.cfg -o messages.pot .```
- 生成更新后的语言翻译源文件  ```pybabel update -i messages.pot  -d translations```
- 更新对应语言翻译源文件
- 编译更新后的翻译源文件  ```pybabel compile -d translations```
- 部署
2、更新本地配置文件 local.py
- ```cp local.py.example local.py```
- 更新redis配置
3、构建容器
- ```bash delpoy.sh```
4、启动
- ```bash run.sh```
