
# Use cases

## Core Functions
- 創立使用者的功能(數值輸入錯誤的值)
- 更改使用者資料
- 任意更改machine id
- 手動搜尋食物功能(亂輸入會得到什麼)
- 用戶拿有條碼的東西掃描
- 用戶用食物、水果，測量東西的重量與熱量
- 無法辨識食物種類，跳出改手動輸入

## Test plan(QA test)

- UI是否有閃退的問題
  - Linux service自動開起環境,service
- 秤重值是否能正確抓取
- 螢幕觸控鍵盤是否能正常work
- Barcode掃描問題???????????????(影像有晃動)
  - 掃描失敗手動輸入
  - Hector輸入後端Barcode Table’s data


# Issues

- 統一容器，api直接扣容器重量
- 影像辨識API Input image:nparry, output name:String
- 資料庫名稱大小寫是一樣的嗎
- 外殼是否要有背蓋