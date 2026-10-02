# imyemail-cloud Homebrew 源

[English](README.md) · [简体中文](README.zh-CN.md) · [主项目仓库](https://github.com/logdns/imyemail-cloud)

[imyemail-cloud](https://github.com/logdns/imyemail-cloud) 是 MIT 开源的多端原生邮件客户端。这个 Homebrew tap 会安装 Apple Silicon macOS 应用，并提供同名的 `imyemail-cloud` 命令行入口。

## 安装

每台 Mac 首次使用时执行：

```bash
brew tap logdns/imyemail-cloud
brew trust --tap logdns/imyemail-cloud
brew install imyemail-cloud
```

`brew trust` 是 Homebrew 7 针对第三方 tap 的供应链确认，每台机器只需执行一次。完成后，日常安装命令就是：

```bash
brew install imyemail-cloud
```

也可以使用完整 cask 名称：

```bash
brew install --cask logdns/imyemail-cloud/imyemail-cloud
```

启动应用或使用命令行：

```bash
open -a imyemail-cloud
imyemail-cloud --help
```

## 更新与卸载

```bash
brew update
brew upgrade imyemail-cloud
brew uninstall imyemail-cloud
```

## 要求与发布边界

- Apple Silicon（`arm64`）
- macOS 14 Sonoma 或更高版本
- 当前开发包采用 ad-hoc 签名，未经过 Apple 公证。Homebrew 会在安装前核对固定 SHA-256，但 macOS 首次启动时仍可能要求在“系统设置 > 隐私与安全性”中确认允许打开。
- 正常卸载不会删除邮件数据或钥匙串凭据。

包哈希、签名状态和生产发布限制见[发布文档](https://github.com/logdns/imyemail-cloud/blob/main/docs/RELEASE.md)。

## Brewfile

```ruby
tap "logdns/imyemail-cloud"
cask "imyemail-cloud"
```

## 协议

[MIT](LICENSE)
