from ctypes import *
from users.DigitalPersona.dpfj import *
from users.DigitalPersona.dpfpdd import *
from users.DigitalPersona.main import CaptureFinger

so_file = "users/DigitalPersona/win32/dpfpdd.dll"
mydll = CDLL(so_file)
so_file = "users/DigitalPersona/win32/dpfj.dll"
my_dll = CDLL(so_file)

#printf c++
libc = cdll.msvcrt
printf = libc.printf

def Enrollment(hReader):
    bStop = True
    while(bStop):
        capture_cnt = 0
        pFmd = c_ubyte()
        nFmdSize = c_uint(0)
        print("Enrollment started")
        print("--------------------")

        #start the enrollment
        result = my_dll.dpfj_start_enrollment(DPFJ_FMD_ANSI_378_2004)
        if(DPFJ_SUCCESS == result):
            bDone = 0
            bFirst = 1
            while(bDone == 0):
                capture_cnt = capture_cnt + 1
                print(capture_cnt)


                if(bFirst):
                    bFirst = 0
                    result, pFmd, nFmdSize = CaptureFinger("any finger", hReader, DPFJ_FMD_ANSI_378_2004, byref(pFmd), byref(nFmdSize))
                    if(0 != result):
                        bShop = False
                        break
                
                else:
                    result, pFmd, nFmdSize = CaptureFinger("the same finger", hReader, DPFJ_FMD_ANSI_378_2004, byref(pFmd), byref(nFmdSize))
                    if(0 != result):
                        bShop = False
                        break
                
                result = my_dll.dpfj_add_to_enrollment(DPFJ_FMD_ANSI_378_2004, pFmd, nFmdSize, 0)
                pFmd = c_ubyte()
                if result == DPFJ_SUCCESS:
                    bDone = 1
                    break
                else:
                    print("dpfj_add_to_enrollment()")
            pEnrollmentFmd = c_ubyte()
            nEnrollmentFmdSize = c_uint(0)
            if(bDone):
                result = my_dll.dpfj_create_enrollment_fmd(None, byref(nEnrollmentFmdSize))
                print(nEnrollmentFmdSize)
                pEnrollmentFmd = (c_ubyte*nEnrollmentFmdSize.value)(*b'')
                result = my_dll.dpfj_create_enrollment_fmd(pEnrollmentFmd, byref(nEnrollmentFmdSize))
                if result == DPFJ_SUCCESS and 0 != nEnrollmentFmdSize:
                    print("Enrollment template created, size: ", nEnrollmentFmdSize.value)
                                        
            result = my_dll.dpfj_finish_enrollment()
            mydll.dpfpdd_exit()
            if(DPFJ_SUCCESS != result):
                print("dpfj_finish_enrollment()")
            string = ''.join(chr(i) for i in pEnrollmentFmd)
            print(string)
            return string
        else:
            print("dpfj_start_enrollment()")



# Defining main function 
def main():
    #Inicializar
    result = mydll.dpfpdd_init()
    if(DPFPDD_SUCCESS == result): 
        print("calling dpfpdd_init()")
        print("----------------------")


        #Informações sobre o leitor
        dev_cnt = c_uint(2)
        dev_infos = DPFPDD_DEV_INFO()
        mydll.dpfpdd_query_devices.argtypes = [POINTER(c_uint),POINTER(DPFPDD_DEV_INFO)]
        mydll.dpfpdd_query_devices.restype = c_int
        result = mydll.dpfpdd_query_devices(dev_cnt,byref(dev_infos))
        if(DPFPDD_SUCCESS == result):
            print("Varredura Completa")
            print("----------------------")
            printf(b"Nome do dispositivo conectado: %s\n", dev_infos.name)
            print("----------------------")


            #Inicia o leitor
            pdev = DPFPDD_DEV()
            dev_name = dev_infos.name
            mydll.dpfpdd_open.argtypes = [POINTER(c_char),POINTER(DPFPDD_DEV)]
            mydll.dpfpdd_open.restype = c_int
            #result = mydll.dpfpdd_open(dev_name,byref(pdev))
            result = mydll.dpfpdd_open_ext(dev_name, DPFPDD_PRIORITY_EXCLUSIVE, byref(pdev))
            if(DPFPDD_SUCCESS == result):
                print("Dispositivo Selecionado")
                print("----------------------")

                #funcionalidades do leitor
                dev_caps = DPFPDD_DEV_CAPS(60)
                mydll.dpfpdd_get_device_capabilities.argtypes = [DPFPDD_DEV,POINTER(DPFPDD_DEV_CAPS)]
                mydll.dpfpdd_get_device_capabilities.restype = c_int
                if DPFPDD_SUCCESS == mydll.dpfpdd_get_device_capabilities(pdev,dev_caps):
                    print("Funcionalidades adquiridas")
                    print("dpi do leitor: ",dev_caps.resolutions[0])
                    print("----------------------")
                    
                    
                    return Enrollment(pdev)
                    

                else:
                    print("Funcionalidades não adiquiridas")   
            
            else:
                print("Erro ao selecionar dispositivo.")
            
            #Fecha o despositivo
            mydll.dpfpdd_close.argtypes = [DPFPDD_DEV]
            mydll.dpfpdd_close.restype = c_int
            if DPFPDD_SUCCESS == mydll.dpfpdd_close(pdev):
                print("Dispositivo encerrado")
                print("----------------------")

        else:
            print("Erro ao fazer varredura")
            print("----------------------")
        
        #Finalizar
        mydll.dpfpdd_exit()

    else: print("error when calling dpfpdd_init()") 

# Using the special variable  
# __name__ 
if __name__=="__main__": 
    main() 


