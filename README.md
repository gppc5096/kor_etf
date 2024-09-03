## 한국 주식 ETF 정보 현황
### URL : https://finance.naver.com/item/main.naver?code=360750 에서 틱커명으로 검색

* Tiger S&P500 : 360750
* Tiger 나스닥100 : 133690
* Ace 미국테크TOP7Plus : 465580
---------------------------------
* Kodex CD금리액티브(합성) : 459580
* Tiger CD금리액티브(합성) : 357870

### 맥용 아이콘 만들기
* 이미지를 1024x1024 픽셀 크기의 PNG 파일로 저장합니다.
  - PNG 파일을 .icns 파일로 변환합니다. Mac에서는 다음과 같은 방법을 사용할 수 있습니다:
  - 터미널을 열고 다음 명령어를 실행합니다:

   mkdir MyIcon.iconset
   sips -z 16 16 icon.png --out MyIcon.iconset/icon_16x16.png
   sips -z 32 32 icon.png --out MyIcon.iconset/icon_16x16@2x.png
   sips -z 32 32 icon.png --out MyIcon.iconset/icon_32x32.png
   sips -z 64 64 icon.png --out MyIcon.iconset/icon_32x32@2x.png
   sips -z 128 128 icon.png --out MyIcon.iconset/icon_128x128.png
   sips -z 256 256 icon.png --out MyIcon.iconset/icon_128x128@2x.png
   sips -z 256 256 icon.png --out MyIcon.iconset/icon_256x256.png
   sips -z 512 512 icon.png --out MyIcon.iconset/icon_256x256@2x.png
   sips -z 512 512 icon.png --out MyIcon.iconset/icon_512x512.png
   cp icon.png MyIcon.iconset/icon_512x512@2x.png
   iconutil -c icns MyIcon.iconset

### 실행파일 명령어
* pyinstaller --name="KOR ETF Viewer" --windowed --icon=MyIcon.icns main.py
