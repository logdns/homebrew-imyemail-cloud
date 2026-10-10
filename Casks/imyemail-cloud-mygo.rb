cask "imyemail-cloud-mygo" do
  arch arm: "arm64", intel: "amd64"

  version "0.3.4"
  on_arm do
    sha256 "f902b0ff07cfa8dda98d846d652701eb5aa0694aa9f541634f52b0d95307f6ae"
  end
  on_intel do
    sha256 "e4e40f0b08ddaa81a8a18509f7cb028a61c2c00828d37d6e80dd7d2796f78601"
  end

  url "https://github.com/logdns/imyemail-cloud/releases/download/mygo-v#{version}/imyemail-cloud-mygo-#{version}-darwin-#{arch}-selfsigned.zip"
  name "imyemail-cloud-mygo"
  desc "Go-native email desktop preview with a bundled Rust core"
  homepage "https://imy.email/"

  livecheck do
    skip "Preview releases are independently verified by the tap sync workflow"
  end

  depends_on macos: :sonoma

  app "imyemail-cloud-mygo.app"
  binary "#{appdir}/imyemail-cloud-mygo.app/Contents/MacOS/imyemail-cloud-mygo"

  uninstall quit: "email.imy.cloud.mygo"

  caveats <<~EOS
    Desktop preview, not feature-equivalent to imyemail-cloud-native.
    Self-signed, not Apple-notarized or publicly trusted. Verify the publisher
    fingerprint before approving the app in System Settings > Privacy & Security.
    Native and MyGo accounts/data remain independent; there is no auto-migration.
    https://github.com/logdns/imyemail-cloud/blob/main/docs/INSTALL.md
  EOS
end
