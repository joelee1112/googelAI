# Vercel 500 錯誤除錯指南

## 問題分析

您的 LINE Bot 在 Vercel 上發生 500 內部伺服器錯誤。根據代碼分析，主要問題包括：

1. **環境變數未設定**
2. **模組匯入錯誤**
3. **缺乏錯誤處理**
4. **檔案路徑問題**

## 修復步驟

### 1. 設定環境變數

在 Vercel 專案設定中添加以下環境變數：

```
LINE_CHANNEL_ACCESS_TOKEN=你的_LINE_Channel_Access_Token
LINE_CHANNEL_SECRET=你的_LINE_Channel_Secret
MANT0U_BOT_MODEL=default
IMGBB_KEY=你的_IMGBB_Key (如果需要)
```

### 2. 使用修復版本

我已經創建了以下修復檔案：

- `index_minimal.py` - 最小可行版本（建議先使用）
- `index_safe.py` - 完整安全版本
- `diagnostic.py` - 診斷工具

### 3. 部署步驟

1. **測試最小版本**：
   ```bash
   # 更新 vercel.json 指向 index_minimal.py（已完成）
   vercel --prod
   ```

2. **檢查環境變數**：
   - 訪問 `https://你的域名.vercel.app/status` 
   - 檢查返回的狀態資訊

3. **測試 webhook**：
   - 在 LINE Developers Console 設定 webhook URL
   - 測試發送訊息

### 4. 除錯工具

如果仍有問題，可以暫時部署診斷版本：

1. 修改 `vercel.json` 中的 `src: "diagnostic.py"`
2. 重新部署
3. 訪問 `/debug` 端點查看詳細錯誤資訊

### 5. 常見錯誤解決方案

#### 錯誤：模組匯入失敗
- 檢查 `requirements.txt` 是否包含所有必要套件
- 確認套件版本相容性

#### 錯誤：環境變數未設定
- 在 Vercel Dashboard 的 Settings > Environment Variables 中設定
- 確認變數名稱完全正確

#### 錯誤：檔案路徑問題
- 避免使用 `/tmp/` 路徑（在 serverless 環境中不穩定）
- 使用相對路徑或 Vercel 提供的暫存目錄

### 6. 監控和日誌

- 在 Vercel Dashboard 的 Functions 標籤中查看執行日誌
- 添加更多 `print()` 語句來追蹤執行流程

### 7. 逐步恢復功能

一旦基本功能正常：

1. 逐步恢復原始功能模組
2. 每次添加一個功能後進行測試
3. 如果出現錯誤，立即回滾到上一個穩定版本

## 測試清單

- [ ] 基本 HTTP 請求回應正常
- [ ] 環境變數正確設定
- [ ] LINE webhook 接收正常
- [ ] 基本訊息回覆功能
- [ ] 錯誤處理機制運作
- [ ] 日誌記錄正常

## 緊急回滾

如果需要緊急回滾到基本功能：

1. 將 `vercel.json` 中的 `src` 改為 `index_minimal.py`
2. 執行 `vercel --prod`
3. 這將提供最基本但穩定的服務

## 支援

如果問題持續存在，請檢查：

1. Vercel 函數日誌
2. LINE Developers Console 的 webhook 日誌
3. 瀏覽器開發者工具的網路請求
