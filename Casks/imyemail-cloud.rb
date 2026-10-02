cask "imyemail-cloud" do
  version "0.2.1"
  sha256 "91f6ac78b0d0571e2595982f3058764c59463f68628f1e1170a3267d35cf2ed2"

  url "https://github.com/logdns/imyemail-cloud/releases/download/v#{version}/imyemail-cloud-macos-arm64-20261002-unsigned.zip"
  name "imyemail-cloud"
  desc "Open-source native email client"
  homepage "https://imy.email/"

  livecheck do
    url :url
    strategy :github_latest
  end

  depends_on arch: :arm64
  depends_on macos: :sonoma

  app "imyemail-cloud.app"
  binary "#{appdir}/imyemail-cloud.app/Contents/MacOS/imyemail-cloud"

  uninstall quit: "email.imy.cloud"

  caveats <<~EOS
    This open-source development build is ad-hoc signed and is not Apple-notarized.
    macOS may require approval in System Settings > Privacy & Security before
    the first launch. Release and signing details:
      https://github.com/logdns/imyemail-cloud/blob/v#{version}/docs/RELEASE.md
  EOS
end
