# Windows SDK 簽章查核

查核日期：**2026-11-17（台灣時間）**。範圍：**Fubon Neo Python SDK 2.5.0、Windows x64、`cp37-abi3-win_amd64` wheel**。這是指定發行檔的本機 Authenticode 查核，不是券商公布的 SAC 相容性保證。

**官網下載版與 PyPI 版雖然版本和 wheel 檔名相同，內部 PYD 與簽章狀態不同。SAC 尚未實測，`SACCompatibility: NOT_TESTED`。** 沒有執行 no-ISG audit 或 SAC enforcement 測試，也沒有執行 SDK import、登入或交易。

## 來源與實際檔案

- 官網：[SDK 下載頁](https://www.fbs.com.tw/TradeAPI/docs/download/download-sdk/) → [2.5.0 Windows ZIP](https://www.fbs.com.tw/TradeAPI_SDK/fubon_binary/fubon_neo-2.5.0-cp37-abi3-win_amd64.zip)，ZIP 內為 `fubon_neo-2.5.0-cp37-abi3-win_amd64.whl`。
- PyPI：[fubon-neo 2.5.0](https://pypi.org/project/fubon-neo/2.5.0/) → [Windows wheel](https://files.pythonhosted.org/packages/2f/59/2af284756bc107656074ce31d77d5ee2f518bbf902b6456eb71436b76161/fubon_neo-2.5.0-cp37-abi3-win_amd64.whl)。

以下雜湊均為 SHA-256：

| 發行管道 / Route | wheel | `fubon_neo/_fubon_neo.pyd` |
| --- | --- | --- |
| 官網 / Official website | `a7e55adac3adb0c8fc3d5fc94360d9e0d5fc0391f437c8eadde706374cb91c9f` | `2b7fe49c078e16188acab02059a8e8461af507f3d403876f5c4f4299c78bc9d4` |
| PyPI | `0b08ee203a6ac33be65a56c93ff7c58e1d1abebf437b2b8873aa6b94805095b1` | `ce4a8e68dce5bba5ba563322a55c24f008a75f83865388d3c554b859284ef2b5` |

官網 ZIP 本身的 SHA-256 為 `04eb4b11b1e3bb92c056a3b00f6ebe6fdc67642f4ca8eb0dc7c485f24139de58`。兩個 wheel 的 PYD、SBOM、WHEEL 與 RECORD 不同；不能假設這只是對同一份二進位檔附加簽章，也不能用版本號代替檔案身分。

## 本機簽章結果

| 項目 / Evidence | 官網 / Official website | PyPI |
| --- | --- | --- |
| Windows PE | 1 個 PYD | 1 個 PYD |
| Authenticode status | `Valid` | `NotSigned` |
| Signature type | `Authenticode` | `None` |
| Signer | 富邦綜合證券股份有限公司 | 無 |
| Issuer | GlobalSign GCC R45 CodeSigning CA 2020 | 無 |
| Timestamp certificate | Globalsign R45 TSA for CodeSign 202510 | 無 |

證據層級為 `LocalAuthenticodeOnly`。`Valid` 不等於目標 Windows 電腦已接受整個工作流程；`NotSigned` 也不能推導為一定被 SAC 阻擋。依 Microsoft 說明，SAC 的雲端判定與可信任簽章都可能影響結果，且二進位檔在載入時才被評估。[SAC FAQ](https://support.microsoft.com/en-us/windows/security/threat-malware-protection/smart-app-control-frequently-asked-questions)、[簽章說明](https://learn.microsoft.com/en-us/windows/apps/develop/smart-app-control/code-signing-for-smart-app-control)、[SAC 測試說明](https://learn.microsoft.com/en-us/windows/apps/develop/smart-app-control/test-your-app-with-smart-app-control)

## 使用與復核

Windows SAC 相容性會影響安裝選擇時，核對實際下載的 wheel、內部 PYD 與相依檔案。本次官網核心檔有有效簽章；不要把這個結果延伸為所有官網版本都已通過 SAC，也不要把 PyPI 這個檔案的結果延伸為所有 PyPI 版本皆未簽章。上游替換下載檔、SDK 升版或發行管道改變時，重新記錄日期、來源、雜湊與本機簽章，保留上游有效簽章。

可使用現有 Windows PowerShell 對解壓後的實際檔案查核；以下命令不執行 SDK：

```powershell
Get-FileHash -LiteralPath '.\fubon_neo-2.5.0-cp37-abi3-win_amd64.whl' -Algorithm SHA256
# Extract the wheel into a separate inspection directory first.
$nativeFile = '.\inspection\fubon_neo\_fubon_neo.pyd'
Get-FileHash -LiteralPath $nativeFile -Algorithm SHA256
Get-AuthenticodeSignature -LiteralPath $nativeFile |
    Select-Object Status, SignatureType,
        @{Name='Signer'; Expression={$_.SignerCertificate.Subject}},
        @{Name='Issuer'; Expression={$_.SignerCertificate.Issuer}},
        @{Name='TimestampSigner'; Expression={$_.TimeStamperCertificate.Subject}}
```

原生相依、延後載入的功能與應用程式封裝需各自查核；核心 PYD 有簽章，不能替整個 Python 環境背書。若要提出 SAC 相容性主張，還需另外取得特定 artifact、Windows build、政策模式、功能路徑與對應事件的實測證據。

## English summary

Checked **2026-11-17**, **SDK 2.5.0**, **Windows x64**. The official website ZIP contains a wheel whose `_fubon_neo.pyd` has a locally `Valid` Fubon signature issued by GlobalSign and a timestamp certificate. The same-version PyPI wheel contains a `NotSigned` PYD. The artifact hashes above identify the exact files; the two builds must not be treated as identical.

**SAC has not been tested (`NOT_TESTED`).** Local Authenticode validation is not SAC enforcement evidence. Recheck the actual artifacts after a version, distribution-route or upstream-file change, and inspect native dependencies separately.
