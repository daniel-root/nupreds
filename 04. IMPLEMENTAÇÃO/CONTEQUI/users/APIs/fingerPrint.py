from ctypes import *
from users.APIs.dpfj import *
from users.APIs.dpfpdd import *

so_file = "users/APIs/lib/windows/x64/dpfpdd"
mydll = CDLL(so_file)
so_file = "users/APIs/lib/windows/x64/dpfj"
my_dll = CDLL(so_file)

#printf c++
libc = cdll.msvcrt
printf = libc.printf

def CaptureFinger(szFingerName, hReader, nFtType, ppFt, pFtSize):
    result = c_int(0)
    ppFt = c_void_p
    pFtSize = 0

    cparam = DPFPDD_CAPTURE_PARAM(0)
    cparam.size = sizeof(cparam)
    cparam.image_fmt = DPFPDD_IMG_FMT_ISOIEC19794
    cparam.image_proc = DPFPDD_IMG_PROC_NONE
    cparam.image_res = 500
    
    cresult = DPFPDD_CAPTURE_RESULT(0)
    cresult.size = sizeof(cresult)
    cresult.info.size = sizeof(cresult.info)
    
    nImageSize = c_uint(0)
    
    mydll.dpfpdd_capture.arftypes = [DPFPDD_DEV,POINTER(DPFPDD_CAPTURE_PARAM),c_uint,POINTER(DPFPDD_CAPTURE_RESULT),POINTER(c_uint),POINTER(c_ubyte)]
    mydll.dpfpdd_capture.restypes = c_int
    mydll.dpfpdd_capture(hReader,byref(cparam),0,byref(cresult),byref(nImageSize),None)
    
    pImage = (c_ubyte*139990)(*b'')
    

    while(1):
        is_ready = 0
        while(1):
            ds = DPFPDD_DEV_STATUS()
            ds.size = sizeof(DPFPDD_DEV_STATUS)
            result = mydll.dpfpdd_get_device_status(hReader, byref(ds))
            if(DPFPDD_SUCCESS != result):
                return "dpfpdd_get_device_status()"
                break
            if(DPFPDD_STATUS_READY == ds.status or DPFPDD_STATUS_NEED_CALIBRATION == ds.status):
                is_ready = 1
                break
        
        if (is_ready == 0):
            break

        #print("Put", szFingerName," on the reader, or press Ctrl-C to cancel...")
        result = mydll.dpfpdd_capture(hReader, byref(cparam), -1, byref(cresult), byref(nImageSize), pImage)
        
        if(DPFPDD_SUCCESS != result):
            return "Erro dpfpdd_capture()"
        else:
            if cresult.success:
                #print("fingerprint captured")
                nFeaturesSize = c_uint(MAX_FMD_SIZE)
                
                pFeatures = (c_ubyte*1562)(*b'')

                my_dll.dpfj_create_fmd_from_fid.argtypes = [DPFJ_FID_FORMAT,POINTER(c_ubyte),c_uint,DPFJ_FMD_FORMAT,POINTER(c_ubyte),POINTER(c_uint)]
                my_dll.dpfj_create_fmd_from_fid.restypes = c_int
                result = my_dll.dpfj_create_fmd_from_fid(DPFJ_FID_ISO_19794_4_2005, pImage, nImageSize, nFtType, pFeatures, byref(nFeaturesSize))
                if(DPFJ_SUCCESS == result):
                    ppFt = pFeatures
                    pFtSize = nFeaturesSize
                    
                    #print("features extracted.")
        break
    return result, ppFt, pFtSize
                
                



def Verification(hReader):
    pFeatures1 = c_ubyte()
    nFeatures1Size = c_uint(0)
    pFeatures2= c_ubyte()
    nFeatures2Size = c_uint(0)

    bStop = False
    while(bStop != True):
        #print("Verification started")
        result, pFeatures1, nFeatures1Size = CaptureFinger("any finger", hReader, DPFJ_FMD_ISO_19794_2_2005, byref(pFeatures1), byref(nFeatures1Size))
        
        if result == 0:
            user= Client.objects.all().values_list('fingerprint',flat=True)
            #print(user)
            result = 0
            if result == 0:
                falsematch_rate = c_uint(0)
                for i in user:
                    #print(i)
                    if i == None:
                        continue
                    
                    a = Client.objects.filter(fingerprint=i).values_list('usuario',flat=True)
                    #print(a[0])
                    res = [] 
                    for ele in i:
                        res.extend(ord(num) for num in ele)
                    pFeatures2 = (c_ubyte * len(res))(*res)
                    nFeatures2Size = sizeof(pFeatures2)                    
                    my_dll.dpfj_compare.argtypes = [DPFJ_FMD_FORMAT,POINTER(c_ubyte),c_uint,c_uint,DPFJ_FMD_FORMAT,POINTER(c_ubyte),c_uint,c_uint,POINTER(c_uint)]
                    my_dll.dpfj_compare.restype = c_int
                    result = my_dll.dpfj_compare(DPFJ_FMD_ISO_19794_2_2005, pFeatures1, nFeatures1Size, 0, DPFJ_FMD_ISO_19794_2_2005, pFeatures2, nFeatures2Size, 0, byref(falsematch_rate))
                    if(DPFJ_SUCCESS == result):
                        #target_falsematch_rate = c_long(21474.83647)
                        #print(falsematch_rate)
                        if(falsematch_rate.value == 0):
                            #print("Fingerprints matched.")
                            return a[0]

                        else:
                            continue
                            #print("Fingerprints did not match.")
                    else:
                        return "Erro dpfj_compare()"
            else: 
               return "Error"
        bStop = True




# Defining main function 
def main(tipo):
    #Inicializar
    result = mydll.dpfpdd_init()
    if(DPFPDD_SUCCESS == result): 
        #print("calling dpfpdd_init()")
        #print("----------------------")


        #Informações sobre o leitor
        dev_cnt = c_uint(2)
        dev_infos = DPFPDD_DEV_INFO()
        mydll.dpfpdd_query_devices.argtypes = [POINTER(c_uint),POINTER(DPFPDD_DEV_INFO)]
        mydll.dpfpdd_query_devices.restype = c_int
        result = mydll.dpfpdd_query_devices(dev_cnt,byref(dev_infos))
        #print(dev_cnt)
        #print(result)
        if(DPFPDD_SUCCESS == result):
            #print("Varredura Completa")
            #print("----------------------")
            #printf(b"Nome do dispositivo conectado: %s\n", dev_infos.name)
            #print("----------------------")


            #Inicia o leitor
            pdev = DPFPDD_DEV()
            dev_name = dev_infos.name
            mydll.dpfpdd_open.argtypes = [POINTER(c_char),POINTER(DPFPDD_DEV)]
            mydll.dpfpdd_open.restype = c_int
            result = mydll.dpfpdd_open(dev_name,byref(pdev))
            #result = mydll.dpfpdd_open_ext(dev_name, DPFPDD_PRIORITY_EXCLUSIVE, byref(pdev))
            #print(dev_name)
            #print(result)
            if(DPFPDD_SUCCESS == result):
                #print("Dispositivo Selecionado")
                #print("----------------------")

                #funcionalidades do leitor
                dev_caps = DPFPDD_DEV_CAPS(60)
                mydll.dpfpdd_get_device_capabilities.argtypes = [DPFPDD_DEV,POINTER(DPFPDD_DEV_CAPS)]
                mydll.dpfpdd_get_device_capabilities.restype = c_int
                if DPFPDD_SUCCESS == mydll.dpfpdd_get_device_capabilities(pdev,dev_caps):
                    #print("Funcionalidades adquiridas")
                    #print("dpi do leitor: ",dev_caps.resolutions[0])
                    #print("----------------------")
                    
                    if tipo == "Verification":
                        result = Verification(pdev)
                    else:
                        pFeatures1 = c_ubyte()
                        nFeatures1Size = c_uint(0) 
                        result, pFeatures1, nFeatures1Size = CaptureFinger("any finger", pdev, DPFJ_FMD_ISO_19794_2_2005, byref(pFeatures1), byref(nFeatures1Size))
                        if(DPFPDD_SUCCESS == result):
                            result = ''.join(chr(i) for i in pFeatures1)
                        else:
                            result = "Erro ao adquirir impresão"
                        
                    

                else:
                    return "Erro ao adiquirir Funcionalidades"
            
            else:
                return "Erro ao selecionar dispositivo."
            
            #Fecha o despositivo
            mydll.dpfpdd_close.argtypes = [DPFPDD_DEV]
            #print("fechou")
            mydll.dpfpdd_close.restype = c_int
            if DPFPDD_SUCCESS != mydll.dpfpdd_close(pdev):
               return "Erro ao encerrar"
                #print("----------------------")


        else:
            return "Erro ao fazer varredura"
            #print("----------------------")
        
        #Finalizar
        mydll.dpfpdd_exit()
        return result

    else: return "Erro when calling dpfpdd_init()" 