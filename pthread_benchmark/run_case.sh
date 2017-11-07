sed -i 's/gpgpu_sms_app1 30/gpgpusim_app1 15/g' *gpgpusim.config*
./simrun.sh -apps BLK SPMV
sed -i 's/gpgpusim_app_1 15/gpgpusim_app1 50/g' *gpgpusim.config*
./simrun.sh -apps SAD BFS2
sed -i 's/gpgpusim_app_1 50/gpgpusim_app1 10/g' *gpgpusim.config*
./simrun.sh -apps GUPS BFS2
sed -i 's/gpgpusim_app_1 10/gpgpusim_app1 50/g' *gpgpusim.config*
./simrun.sh -apps NN BFS2
sed -i 's/gpgpusim_app_1 50/gpgpusim_app1 35/g' *gpgpusim.config*
./simrun.sh -apps RAY BLK
sed -i 's/gpgpusim_app_1 35/gpgpusim_app1 50/g' *gpgpusim.config*
./simrun.sh -apps HS BLK
#sed -i 's/gpgpusim_app_1 15/gpgpusim_app1 15/g' *gpgpusim.config*
./simrun.sh -apps HS BFS2
sed -i 's/gpgpusim_app_1 50/gpgpusim_app1 30/g' *gpgpusim.config*
./simrun.sh -apps BLK LUD
sed -i 's/gpgpusim_app_1 30/gpgpusim_app1 45/g' *gpgpusim.config*
./simrun.sh -apps BP FFT
sed -i 's/gpgpusim_app_1 45/gpgpusim_app1 20/g' *gpgpusim.config*
./simrun.sh -apps 3DS LPS
