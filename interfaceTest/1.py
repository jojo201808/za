import  os

class Ideamonkey():
    def __int__(self):
        self.devicelist = []
        self.devicemodels = []
        self.name = 'dddd'

    def get_devices(self):
        devicetmp = []
        rtd = os.popen('adb devices').readlines()
        # 获取手机设备号
        for d in rtd:
            devicetmp.append(d.split('\t')[0])
        self.devicelist = devicetmp[1:-1]
        print(self.devicelist)
        print(self.name)
        print(self.devicemodels)
       
        # 获取手机型号
        for m in range(len(self.devicelist)):
            # tmpmodel = os.popen('adb -s '+devicelist[m]+' shell getprop ro.product.model').readlines()[0].split('\n')[0]
            tmpmodel = os.popen('adb -s ' + self.devicelist[m] + ' shell getprop ro.product.model') \
                .readlines()[0].strip('\n')
            #self.devicemodels.append(tmpmodel)

if __name__ == '__main__':
    t = Ideamonkey()
    t.get_devices()