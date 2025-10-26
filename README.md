# NekoChecker =-=

NekoChecker 是一款为 CTF 比赛中多题组 / 多题目设计的交互式答案检查工具。

## 运行

安装依赖：

```bash
pip install -r ./requirements.txt
```

带参数启动 Checker：

```bash
# 不带参数的情况下，默认为 ./problems.json
python3 ./run.py [题组配置文件名]
```

## 部署

在用于比赛环境时，你可能想要将其部署到某个目标容器。

从目前的情况来看，Clone 下整个仓库是比较方便的方法...
