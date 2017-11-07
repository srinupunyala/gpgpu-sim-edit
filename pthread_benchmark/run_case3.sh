#./simrun.sh -apps3 BLK SPMV 3DS
#./simrun.sh -apps3 3DS BP LPS
#sed -i 's/gpgpu_sms_app1 20/gpgpu_sms_app1 10/g' *gpgpusim.config*
#sed -i 's/gpgpu_sms_T2 20/gpgpu_sms_T2 30/g' *gpgpusim.config*
#./simrun.sh -apps3 LUD JPEG HS
#./simrun.sh -apps3 BLK SPMV RAY
./simrun.sh -apps3 SAD JPEG FFT
./simrun.sh -apps3 HS JPEG SAD
./simrun.sh -apps3 HS FFT SAD
./simrun.sh -apps3 SAD JPEG JPEG
#sed -i 's/gpgpu_sms_app1 10/gpgpu_sms_app1 10/g' *gpgpusim.config*
#sed -i 's/gpgpu_sms_T2 30/gpgpu_sms_T2 40/g' *gpgpusim.config*
#./simrun.sh -apps3 BLK BFS2 BP
#./simrun.sh -apps3 BFS2 BFS2 SPMV

