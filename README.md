## PASSBOX

### 初始化程序（第一次运行时）
- 配置 *settings.json*
    - *pass*: 加密后密文存储地址，默认为git ，需配置 *remote(仓库地址)* , *branch(分支)*
    - *rsa* : 密钥存储地址,默认为git ,同上
    - 注意 :仓库最好为Private 仓库
  
  
- 安装python(>3) 库, pip intsall -r requirements.txt
-  设置快捷脚本(因为我用的是windows,这里以passbox.bat做示范) 并 添加本目录到 环境变量
-  命令行 运行 *passbox init*  生成密钥和相关文件夹
  
### 使用 & 迁移
   - 程序都基于命令行方便操作
     - 重设私钥密码 passbox reset oldKey(原密码 ) newKey(新密码)
     - 加密 passbox enc *name*(网站域名或其他) *pass*(网站用户名密码信息 或者其他) *aeskey*(私钥密码)
     - 解密 passbox dec *name* *aeskey*
     - 考虑安全，强烈推荐 设置私钥密码 : passbox reset - *${aesKey}*(私钥密码) 将对私钥进行aes加密 ，因为初始时无密码 所以*oldKey*为 -
     - 注意: 私钥密码无时 请写 -