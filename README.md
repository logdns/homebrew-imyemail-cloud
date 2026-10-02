# Homebrew tap for imyemail-cloud

[English](README.md) · [简体中文](README.zh-CN.md) · [Main repository](https://github.com/logdns/imyemail-cloud)

[imyemail-cloud](https://github.com/logdns/imyemail-cloud) is an MIT-licensed,
multi-platform native email client. This tap installs the macOS Apple Silicon
application and its `imyemail-cloud` command-line interface.

## Install

Tap this repository once, then install with the requested short name:

```bash
brew tap logdns/imyemail-cloud
brew trust --tap logdns/imyemail-cloud
brew install imyemail-cloud
```

`brew trust` is a Homebrew 7 supply-chain confirmation for third-party taps.
It is required once per machine. After that, the short install command is:

```bash
brew install imyemail-cloud
```

The standard explicit cask form also works without a separate tap command:

```bash
brew tap logdns/imyemail-cloud
brew trust --tap logdns/imyemail-cloud
brew install --cask logdns/imyemail-cloud/imyemail-cloud
```

Launch the application from Applications, or run the CLI:

```bash
open -a imyemail-cloud
imyemail-cloud --help
```

## Upgrade and uninstall

```bash
brew update
brew upgrade imyemail-cloud
brew uninstall imyemail-cloud
```

## Requirements and release boundary

- Apple Silicon (`arm64`)
- macOS 14 Sonoma or newer
- The current package is ad-hoc signed and not Apple-notarized. Homebrew checks
  its pinned SHA-256 before installation, but macOS may still require approval
  in System Settings > Privacy & Security before the first launch.
- This tap does not delete mailbox data or Keychain credentials during a normal
  uninstall.

For package hashes, signing status, and production-release limitations, see the
[release documentation](https://github.com/logdns/imyemail-cloud/blob/main/docs/RELEASE.md).

## Brewfile

```ruby
tap "logdns/imyemail-cloud"
cask "imyemail-cloud"
```

## License

[MIT](LICENSE)
