del .\deploy\findVideo2.zip
rmdir /s /q .\deploy\findVideo2
xcopy ..\..\venv\Lib\site-packages\* .\deploy\findVideo2 /s
copy ..\..\python-test-module\models\video2.pkl .\deploy\findVideo2
copy src\* \.deploy\findVideo2
7z a .\deploy\findVideo2.zip .\deploy\findVideo2\*