如果你希望不通过修改代码，而是全局设置项目路径，这样后面所有的文件都可以正常使用`config`模块，你可以通过设置`PYTHONPATH`环境变量来实现。这可以确保Python解释器在运行任何文件时都能找到你的项目根目录。

### 通过命令行直接设置`PYTHONPATH`：

#### Windows 下的解决方案：
1. **在当前终端会话中设置`PYTHONPATH`**：
   你可以在运行脚本之前，直接在命令行设置`PYTHONPATH`。

   ```bash
   set PYTHONPATH=H:\my_project\quant_trading_bot;%PYTHONPATH%
   ```

   然后再运行你的脚本：

   ```bash
   python data\data_fetcher.py
   ```

2. **在 PowerShell 中设置`PYTHONPATH`**：
   如果你使用 PowerShell 运行命令，可以使用如下方式：

   ```bash
   $env:PYTHONPATH = "H:\my_project\quant_trading_bot;$env:PYTHONPATH"
   ```

   然后再运行脚本：

   ```bash
   python data\data_fetcher.py
   ```

### 全局永久设置（环境变量）
如果你想每次打开终端时都自动设置好`PYTHONPATH`，可以通过修改系统的环境变量来完成。

1. **在 Windows 系统中永久设置 `PYTHONPATH`**：
   - 打开 **控制面板** -> **系统和安全** -> **系统** -> **高级系统设置** -> **环境变量**。
   - 在 **用户变量** 或 **系统变量** 中，找到 `PYTHONPATH`，如果没有此变量，则创建一个新的变量。
   - 将项目路径 `H:\my_project\quant_trading_bot` 添加到 `PYTHONPATH` 的变量值中（使用分号`;`分隔多个路径）。

这样，无论你在哪个终端中运行你的 Python 文件，Python 都能找到 `config.settings`。

### 验证设置：
1. 设置完 `PYTHONPATH` 后，你可以通过以下命令检查是否设置成功：

   ```bash
   python -c "import sys; print(sys.path)"
   ```

   你应该会看到 `H:\my_project\quant_trading_bot` 已经出现在输出的路径列表中。

2. 之后你就可以直接运行你的 Python 文件了：

   ```bash
   python data\data_fetcher.py
   ```

通过这种方式设置 `PYTHONPATH`，无需修改任何文件，所有脚本都可以正确找到 `config` 模块。

如果有任何问题或进一步的需求，请告诉我！