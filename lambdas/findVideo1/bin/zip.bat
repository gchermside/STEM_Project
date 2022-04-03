del .\deploy\findVideo1.zip
rmdir /s /q .\deploy\findVideo1
xcopy ..\..\venv\Lib\site-packages\* .\deploy\findVideo1 /s
copy ..\..\python-test-module\models\video1.pkl .\deploy\findVideo1
copy src\* \.deploy\findVideo1
7z a .\deploy\findVideo1.zip .\deploy\findVideo1\*