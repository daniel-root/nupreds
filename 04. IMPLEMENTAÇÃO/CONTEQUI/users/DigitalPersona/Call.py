from ctypes import *
from dpfj import *
from dpfpdd import *
so_file = "win32/dpfpdd"
mydll = WinDLL(so_file)
#mydll = cdll.LoadLibrary(so_file)
#mydll = CDLL(so_file)
#mydll = OleDLL(so_file)
#mydll = PyDLL(so_file)
so_file = "win32/dpfj"
my_dll = WinDLL(so_file)
libc = cdll.msvcrt
printf = libc.printf

#inicializando a biblioteca
print(mydll.dpfpdd_init())

dev_cnt = c_uint(1)
dev_infos = DPFPDD_DEV_INFO()
mydll.dpfpdd_query_devices.argtypes = [POINTER(c_uint),POINTER(DPFPDD_DEV_INFO)]
mydll.dpfpdd_query_devices.restype = c_int
#pega iformações sobre o leitor
if DPFPDD_SUCCESS == mydll.dpfpdd_query_devices(dev_cnt,byref(dev_infos)):
    print("Varredura Completa")
printf(b"%i dispositivo(s) conectado(s)\n", dev_cnt)
dev_name = dev_infos.name
print(dev_name)
printf(b"Nome do dispositivo conectado: %s\n", dev_name)


pdev = DPFPDD_DEV()

#inicia o leitor
'''
mydll.dpfpdd_open.argtypes = [POINTER(c_char),POINTER(DPFPDD_DEV)]
mydll.dpfpdd_open.restype = c_int
print(mydll.dpfpdd_open(dev_name,pdev))
print("Dispositivo Selecionado")
print(pdev)
'''
#inicia o leitor com prioridade\

mydll.dpfpdd_open_ext.argtypes = [POINTER(c_char),DPFPDD_PRIORITY,POINTER(DPFPDD_DEV)]
mydll.dpfpdd_open_ext.restype = c_int
priority = DPFPDD_PRIORITY(DPFPDD_PRIORITY_COOPERATIVE)
if DPFPDD_SUCCESS == mydll.dpfpdd_open_ext(dev_name,priority,byref(pdev)):
    print("Leitor selecionado para uso")




#funcionalidades do leitor
dev_caps = DPFPDD_DEV_CAPS(52)
mydll.dpfpdd_get_device_capabilities.argtypes = [DPFPDD_DEV,POINTER(DPFPDD_DEV_CAPS)]
mydll.dpfpdd_get_device_capabilities.restype = c_int
if DPFPDD_SUCCESS == mydll.dpfpdd_get_device_capabilities(pdev,dev_caps):
    print("Funcionalidades adquiridas")
print("dpi do leitor: ",dev_caps.resolutions[0])


#status leitor
'''
dev = pdev
dev_status = DPFPDD_DEV_STATUS()
mydll.dpfpdd_get_device_status.argtypes = [DPFPDD_DEV,POINTER(DPFPDD_DEV_STATUS)]
mydll.dpfpdd_get_device_status.restypes  = c_int
print(mydll.dpfpdd_get_device_status(dev,byref(dev_status)))
print(dev_status.status)
'''
#Não obrigatório
'''
my_dll.dpfj_select_engine.argtypes = [DPFJ_DEV, DPFJ_ENGINE_TYPE]
my_dll.dpfj_select_engine.restype = c_int
engine = DPFJ_ENGINE_TYPE(0)
print(my_dll.dpfj_select_engine(pdev,engine))
'''

#iniciar o processo de inscrição e aloque recursos
'''
fmd_type = DPFJ_FMD_FORMAT(DPFJ_FMD_ANSI_378_2004)
if DPFPDD_SUCCESS == my_dll.dpfj_start_enrollment(fmd_type):
    print("Enrollment iniciado!")
'''

#inicia a captura async
'''
capture_parm = DPFPDD_CAPTURE_PARAM(0)

capture_parm.size = sizeof(capture_parm)
capture_parm.image_fmt = DPFPDD_IMG_FMT_ISOIEC19794
capture_parm.image_proc = DPFPDD_IMG_PROC_NONE
capture_parm.image_res = dev_caps.resolutions[0]

image_size = c_uint(0)
context = c_void_p(1)
#callback = DPFPDD_CAPTURE_RESULT()
#callback = DPFPDD_CAPTURE_CALLBACK_DATA_0(0)
#callback = DPFPDD_CAPTURE_CALLBACK()
#callback.reserved = 0
#print(callback.reserved)

@CFUNCTYPE(None,POINTER(c_void_p), c_uint,c_uint,POINTER(c_void_p))
def CaptureCallback(callback_context,reserved,callback_data_size,callback_data):
    print("Ola")
    if None == callback_context: return
    if None == callback_data: return
    pCaptureData = cast(callback_data,DPFPDD_CAPTURE_CALLBACK_DATA_0)
    pBuffer = c_ubyte(sizeof(DPFPDD_CAPTURE_CALLBACK_DATA_0+pCaptureData.image_size))
    
    if None != pBuffer:
        pcd = cast(pBuffer,DPFPDD_CAPTURE_CALLBACK_DATA_0)
        memmove(pcd,pCaptureData,sizeof(DPFPDD_CAPTURE_CALLBACK_DATA_0))
        
        pcd.image_data = pBuffer + sizeof(DPFPDD_CAPTURE_CALLBACK_DATA_0)
        memmove(pcd.image_data,pCaptureData.image_data,pCaptureData.image_data)


CB_T = CFUNCTYPE(None)
cb_ptr = CB_T(CaptureCallback)
#cmp_func = CMPFUNC(CaptureCallback)


#mydll.dpfpdd_capture_async.argtypes = [DPFPDD_DEV,POINTER(DPFPDD_CAPTURE_PARAM),POINTER(c_void_p),DPFPDD_CAPTURE_CALLBACK_DATA_0]
#mydll.dpfpdd_capture_async.argtypes = [POINTER(None),]
#mydll.dpfpdd_capture_async.argtypes = [DPFPDD_DEV,POINTER(DPFPDD_CAPTURE_PARAM),c_void_p,CaptureCallback(None,None,None,None)]
#mydll.dpfpdd_capture_async.restypes = c_int
mydll.dpfpdd_capture_async(pdev,byref(capture_parm),None,cb_ptr)
print(image_size)

#inicia o leitor
mydll.dpfpdd_open.argtypes = [POINTER(c_char),POINTER(DPFPDD_DEV)]
mydll.dpfpdd_open.restype = c_int
print(mydll.dpfpdd_open(dev_name,pdev))
print("Dispositivo Selecionado")
print(pdev)

'''
#compare duas digitais

fmd1_type = DPFJ_FMD_FORMAT(DPFJ_FMD_ISO_19794_2_2005)
fmd1_size = c_uint(424)
#a = 'AOg5Acgp43NcwEE381mKa_NcZ2bpje3SGCTsMWQgUHtHwyoQ8NkwZ_gMCMTg1PooQW0e1AcLGaYUYB6S7HqLtnkIWdrDQw1krrMkHxBIP6kV9Sx4LiHa9ViaHFwK5jE25e5P21ugTtL0N0DXpaFbgYrO2I5AhMT7q3l-9qJ45WXRBvwyM_JyBtn2Qan2qElzm7_v44D05W9_E1ql1KG6EZH6B8IQH7obmOzP6NAsSN5yEHkK-wWJCFvpzPoAKkgZDdQ1hsuUVUsyhyZ60Cv8-opSN7ydOUDJzChwV7reVsCqa4J9X-KadJSgY0mqaWyBbEyw1NMe8FL8-yDXwldtD301MXtFyZl_uJWqEaAypw7nJAB7X8ur1fKt6h6ODEDxIy7HZMXhBm7ljpDlvE6Xd1-WDrC2NN9tcYzl-91v'
#fmd1 = []
#for i in range(0,len(a)):
#    fmd1.append(ord(a[i]))
#print(fmd1)
fmd1 = (c_ubyte * 424)(*b'AOg5Acgp43NcwEE381mKa_NcZ2bpje3SGCTsMWQgUHtHwyoQ8NkwZ_gMCMTg1PooQW0e1AcLGaYUYB6S7HqLtnkIWdrDQw1krrMkHxBIP6kV9Sx4LiHa9ViaHFwK5jE25e5P21ugTtL0N0DXpaFbgYrO2I5AhMT7q3l-9qJ45WXRBvwyM_JyBtn2Qan2qElzm7_v44D05W9_E1ql1KG6EZH6B8IQH7obmOzP6NAsSN5yEHkK-wWJCFvpzPoAKkgZDdQ1hsuUVUsyhyZ60Cv8-opSN7ydOUDJzChwV7reVsCqa4J9X-KadJSgY0mqaWyBbEyw1NMe8FL8-yDXwldtD301MXtFyZl_uJWqEaAypw7nJAB7X8ur1fKt6h6ODEDxIy7HZMXhBm7ljpDlvE6Xd1-WDrC2NN9tcYzl-91v')
fmd1_view_idx = c_uint(0)
fmd2_type = DPFJ_FMD_FORMAT(DPFJ_FMD_ISO_19794_2_2005)
fmd2_size = c_uint(424)
#fmd2 = c_char*424
#fmd2 = (c_ubyte * 450)(*b'AOg5Acgp43NcwEE381mKK9xcZ2ZZQFVtN_RBol3P004_FaL4Onq0Mnu45xbdOzd1LWsySMsUliAHRbnQHeLjA0odlcC1Tk7K-KNI_yeFzn7MysAtDF8JbL-hFIAIrpva8y7VXZQRjehYkpZ3gu-oolJSynSSEPCYINr44cyFLS2OY933njI6fLgplfQGJVFGRvqGS9VRhtZany1OxmohlNzrSJ0o8XXCu-qRpLeL8buOWOUlbl5oXP7KRaj9qiw8IqbozYpaYDomniQthpcoOz_QDPQqe_hya0zaxZ_yuSMAkLNraBf-tXDdji3YMJrtQgHn9OKy_vOazsAEXlaFQzazydQ5Faq15I2y_rZz1T06pgrNkFuFmxDPjKQIBfQbETSZmtdcQeVPSYKP_yJ066rKWfhjRof5LKJXSOhv')
#b = 'AOg2Acgp43NcwEE381mKa8lcZ2aGzrRnNS1hfLNMYOeXVp3VBRFkG01k_sWyv_vkU2WQeQKaZF2Ud5cISxHd3XsAR7AGCTDmrkGsu64_95G1NoN2SwRel3m6VXCg3GwudTpvEXTMOB_ndiuo8zkNGFQQKkFp2vZNe15jwXgmMh-GpYVzsTwYgdUDphXT3lCFMf5gLPD_ioNeZK2JsbJFKYu_0AOygUgnkqq3SdmZkL4kAbqHakTGM1S1sVNYuIT-wIRnbwxNodISJWelLe3rfjubobW9OvffRLVQNX4R5NSCPXSa-HncJwrKuOnvqKxYnAkqz2RuDPZ15EzqvCqJkPpjz6xMhwAG9BYAWBp8VrUP2wOIyddam0sqN0lUkzktxu71FbNiMRudu4RCzCblg4o1F3s5WHNQNRRvAAAA'
#fmd2 = []
#print(len(b))
#for i in range(0,len(b)):
#    fmd2.append(ord(b[i]))
#print(fmd2)
fmd2 = (c_ubyte * 424)(*b'AOg5Acgp43NcwEE381mKK9xcZ2ZZQFVtN_RBol3P004_FaL4Onq0Mnu45xbdOzd1LWsySMsUliAHRbnQHeLjA0odlcC1Tk7K-KNI_yeFzn7MysAtDF8JbL-hFIAIrpva8y7VXZQRjehYkpZ3gu-oolJSynSSEPCYINr44cyFLS2OY933njI6fLgplfQGJVFGRvqGS9VRhtZany1OxmohlNzrSJ0o8XXCu-qRpLeL8buOWOUlbl5oXP7KRaj9qiw8IqbozYpaYDomniQthpcoOz_QDPQqe_hya0zaxZ_yuSMAkLNraBf-tXDdji3YMJrtQgHn9OKy_vOazsAEXlaFQzazydQ5Faq15I2y_rZz1T06pgrNkFuFmxDPjKQIBfQbETSZmtdcQeVPSYKP_yJ066rKWfhjRof5LKJXSOhv')
fmd2_view_idx = c_uint(0)
score = c_uint(0)
my_dll.dpfj_compare.argtypes = [DPFJ_FMD_FORMAT,POINTER(c_ubyte),c_uint,c_uint,DPFJ_FMD_FORMAT,POINTER(c_ubyte),c_uint,c_uint,POINTER(c_uint)]
my_dll.dpfj_compare.restype = c_int
print(my_dll.dpfj_compare(DPFJ_FMD_ANSI_378_2004,fmd1,fmd1_size,0,DPFJ_FMD_ANSI_378_2004,fmd2,fmd2_size,0,byref(score)))
print(score)



#configuração led
'''
mydll.dpfpdd_led_config.argtypes = [DPFPDD_DEV,DPFPDD_LED_ID,DPFPDD_LED_MODE_TYPE,c_void_p]
mydll.dpfpdd_led_config.restypes = c_int

print(mydll.dpfpdd_led_config(pdev, DPFPDD_LED_ACCEPT or DPFPDD_LED_REJECT ,DPFPDD_LED_CLIENT,None))

print("finish")
import time
mydll.dpfpdd_led_ctrl.argtypes = [DPFPDD_DEV,DPFPDD_LED_ID,DPFPDD_LED_CMD_TYPE]
#mydll.dpfpdd_led_ctrl,
print(mydll.dpfpdd_led_ctrl(pdev, 0x08, 1))
time.sleep(5)
print(mydll.dpfpdd_led_ctrl(pdev, 0x08, 0))
'''


#Inicia captura 1
'''
capture_parm = DPFPDD_CAPTURE_PARAM(0)
capture_parm.size = sizeof(capture_parm)
#capture_parm.image_fmt = DPFPDD_IMG_FMT_ANSI381
capture_parm.image_fmt = DPFPDD_IMG_FMT_ISOIEC19794
capture_parm.image_proc = DPFPDD_IMG_PROC_NONE
capture_parm.image_res = dev_caps.resolutions[0]
#capture_parm.image_res = c_uint(500)
capture_result = DPFPDD_CAPTURE_RESULT(0)
capture_result.size = sizeof(capture_result)
capture_result.info.size = sizeof(capture_result.info)
image_size = c_uint(0)
mydll.dpfpdd_capture.arftypes = [DPFPDD_DEV,POINTER(DPFPDD_CAPTURE_PARAM),c_uint,POINTER(DPFPDD_CAPTURE_RESULT),POINTER(c_uint),POINTER(c_ubyte)]
mydll.dpfpdd_capture.restypes = c_int
print(mydll.dpfpdd_capture(pdev,byref(capture_parm),0,byref(capture_result),byref(image_size),None))

dev_status = DPFPDD_DEV_STATUS()
mydll.dpfpdd_get_device_status.argtypes = [DPFPDD_DEV,POINTER(DPFPDD_DEV_STATUS)]
mydll.dpfpdd_get_device_status.restypes  = c_int
if DPFPDD_SUCCESS == mydll.dpfpdd_get_device_status(pdev,byref(dev_status)):
    print("Status okay",dev_status.status)
print(image_size)
teste = (c_ubyte * 139990)(*b'')
#teste = sizeof(image_size)
print(teste)
print(mydll.dpfpdd_capture(pdev,POINTER(capture_parm),-1,POINTER(capture_result),image_size,teste))
print(image_size)
print(teste)
printf(b"%s\n", teste)
print("tamanho",capture_result.size)
print("okay",capture_result.success)
print("qualidade",capture_result.quality)
print("score",capture_result.score)
print("imagem pixel",capture_result.info.bpp)




#Inicia captura 2

capture_parm = DPFPDD_CAPTURE_PARAM(0)
capture_parm.size = sizeof(capture_parm)
capture_parm.image_fmt = DPFPDD_IMG_FMT_ISOIEC19794
capture_parm.image_proc = DPFPDD_IMG_PROC_NONE
capture_parm.image_res = dev_caps.resolutions[0]
#capture_parm.image_res = c_uint(500)
capture_result = DPFPDD_CAPTURE_RESULT(0)
capture_result.size = sizeof(capture_result)
capture_result.info.size = sizeof(capture_result.info)
image_size = c_uint(0)
mydll.dpfpdd_capture.arftypes = [DPFPDD_DEV,POINTER(DPFPDD_CAPTURE_PARAM),c_uint,POINTER(DPFPDD_CAPTURE_RESULT),POINTER(c_uint),POINTER(c_ubyte)]
mydll.dpfpdd_capture.restypes = c_int
print(mydll.dpfpdd_capture(pdev,byref(capture_parm),0,byref(capture_result),byref(image_size),None))

dev_status = DPFPDD_DEV_STATUS()
mydll.dpfpdd_get_device_status.argtypes = [DPFPDD_DEV,POINTER(DPFPDD_DEV_STATUS)]
mydll.dpfpdd_get_device_status.restypes  = c_int
if DPFPDD_SUCCESS == mydll.dpfpdd_get_device_status(pdev,byref(dev_status)):
    print("Status okay",dev_status.status)
print(image_size)
teste1 = (c_ubyte * 139990)(*b'')
#teste = sizeof(image_size)
print(teste1)

print(mydll.dpfpdd_capture(pdev,byref(capture_parm),-1,byref(capture_result),byref(image_size),teste1))
#print(image_size)
#print(teste1.value)
print(sizeof(teste1))
#printf(b"%s\n", teste1)
print(capture_result.success)



#compara duas digitais
my_dll.dpfj_compare.argtypes = [DPFJ_FMD_FORMAT,POINTER(c_ubyte),c_uint,c_uint,DPFJ_FMD_FORMAT,POINTER(c_ubyte),c_uint,c_uint,POINTER(c_uint)]
my_dll.dpfj_compare.restype = c_int
rate = c_uint(0)
print(my_dll.dpfj_compare(DPFPDD_IMG_FMT_ISOIEC19794, pFeatures, nFeaturesSize, 0, DPFPDD_IMG_FMT_ISOIEC19794, pFeatures2, nFeaturesSize, 0, rate))
'''

#fecha o despositivo
mydll.dpfpdd_close.argtypes = [DPFPDD_DEV]
mydll.dpfpdd_close.restype = c_int
if DPFPDD_SUCCESS == mydll.dpfpdd_close(pdev):
    print("dispositivo encerado")

#liberando a biblioteca
print(mydll.dpfpdd_exit())
