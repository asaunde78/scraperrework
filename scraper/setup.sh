
if [ -d "chrome/" ] ; then
    echo "chrome installed already!"
    exit
fi
echo "missing chrome; installing"
wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/118.0.5982.0/linux64/chrome-linux64.zip -P chrome
cd chrome
echo "unzipping"
unzip chrome-linux64.zip
rm -f chrome-linux64.zip
echo "done!"