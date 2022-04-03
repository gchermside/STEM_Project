del .\deploy\findPicture.zip
rmdir /s /q .\deploy\findPicture
xcopy ..\..\venv\Lib\site-packages\* .\deploy\findPicture /s
copy ..\..\python-test-module\models\picture.pkl .\deploy\findPicture
copy src\* \.deploy\findPicture
7z a .\deploy\findPicture.zip .\deploy\findPicture\*