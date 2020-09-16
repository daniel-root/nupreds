from ctypes import *
DPFPDD_API_VERSION_MAJOR = 1
DPFPDD_API_VERSION_MINOR = 10
DPFPDD_SUCCESS = 0
DPFPDD_E_NOT_IMPLEMENTED = 0x0a
DPFPDD_E_FAILURE = 0x0b
DPFPDD_E_NO_DATA = 0x0c
DPFPDD_E_MORE_DATA = 0x0d
DPFPDD_E_INVALID_PARAMETER = 0x14
DPFPDD_E_INVALID_DEVICE = 0x15
DPFPDD_E_DEVICE_BUSY = 0x1e
DPFPDD_E_DEVICE_FAILURE = 0x1f
DPFPDD_E_PAD_LIBRARY = 0x21
DPFPDD_E_PAD_DATA = 0x22
DPFPDD_E_PAD_LICENSE = 0x23
DPFPDD_E_PAD_FAILURE = 0x24
DPFPDD_DEV = c_void_p
class DPFPDD_VER_INFO(Structure):
    _fields_ = [("major",c_int),("minor",c_int),("maintenance",c_int)]
class DPFPDD_VERSION(Structure):
    _fields_ = [("size",c_uint),("lib_ver",DPFPDD_VER_INFO),("api_ver",DPFPDD_VER_INFO)]
DPFPDD_HW_MODALITY = c_uint
DPFPDD_HW_MODALITY_UNKNOWN = 0
DPFPDD_HW_MODALITY_SWIPE = 1
DPFPDD_HW_MODALITY_AREA = 2
DPFPDD_HW_TECHNOLOGY = c_uint
DP_HW_TECHNOLOGY_UNKNOWN = 0
DP_HW_TECHNOLOGY_OPTICAL = 1
DP_HW_TECHNOLOGY_CAPACITIVE = 2
DP_HW_TECHNOLOGY_THERMAL = 3
DP_HW_TECHNOLOGY_PRESSURE = 4
MAX_STR_LENGTH = 128
MAX_DEVICE_NAME_LENGTH = 1024
class DPFPDD_HW_DESCR(Structure):
    _fields_ = [("vendor_name",c_char*MAX_STR_LENGTH),("product_name",c_char*MAX_STR_LENGTH),("serial_num",c_char*MAX_STR_LENGTH)]
class DPFPDD_HW_ID(Structure):
    _fields_ = [("vendor_id",c_ushort),("product_id",c_ushort)]
class DPFPDD_HW_VERSION(Structure):
    _fields_ = [("hw_ver",DPFPDD_VER_INFO),("fw_ver",DPFPDD_VER_INFO),("bcd_rev",c_ushort)]
class DPFPDD_DEV_INFO(Structure):
    _fields_ = [
        ("size",c_uint),
        ("name",c_char*MAX_DEVICE_NAME_LENGTH),
        ("descr",DPFPDD_HW_DESCR),
        ("id",DPFPDD_HW_ID),
        ("ver",DPFPDD_HW_VERSION),
        ("modality",DPFPDD_HW_MODALITY),
        ("technology",DPFPDD_HW_TECHNOLOGY)]
DPFPDD_PRIORITY = c_uint
DPFPDD_PRIORITY_COOPERATIVE = 2
DPFPDD_PRIORITY_EXCLUSIVE = 4
class DPFPDD_DEV_CAPS(Structure):
    _fields_ = [
        ("size",c_uint),
        ("can_capture_image",c_int),
        ("can_stream_image",c_int),
        ("can_extract_features",c_int),
        ("can_match",c_int),
        ("can_identify",c_int),
        ("has_fp_storage",c_int),
        ("indicator_type",c_uint),
        ("has_pwr_mgmt",c_int),
        ("has_calibration",c_int),
        ("piv_compliant",c_int),
        ("resolution_cnt",c_uint),
        ("resolutions",c_uint*1)]
DPFPDD_STATUS = c_uint
DPFPDD_STATUS_READY = 0
DPFPDD_STATUS_BUSY = 1
DPFPDD_STATUS_NEED_CALIBRATION = 2
DPFPDD_STATUS_FAILURE = 3
class DPFPDD_DEV_STATUS(Structure):
    _fields_ = [("size",c_uint),("status",c_uint),("finger_detected",c_int),("data",c_ubyte)]
DPFPDD_QUALITY = c_uint
DPFPDD_QUALITY_GOOD = 0
DPFPDD_QUALITY_TIMED_OUT = 1
DPFPDD_QUALITY_CANCELED = 1<<1
DPFPDD_QUALITY_NO_FINGER = 1<<2
DPFPDD_QUALITY_FAKE_FINGER = 1<<3
DPFPDD_QUALITY_FINGER_TOO_LEFT = 1<<4
DPFPDD_QUALITY_FINGER_TOO_RIGHT = 1<<5
DPFPDD_QUALITY_FINGER_TOO_HIGH = 1<<6
DPFPDD_QUALITY_FINGER_TOO_LOW = 1<<7
DPFPDD_QUALITY_FINGER_OFF_CENTER = 1<<8
DPFPDD_QUALITY_SCAN_SKEWED = 1<<9
DPFPDD_QUALITY_SCAN_TOO_SHORT = 1<<10
DPFPDD_QUALITY_SCAN_TOO_LONG = 1<<11
DPFPDD_QUALITY_SCAN_TOO_SLOW = 1<<12
DPFPDD_QUALITY_SCAN_TOO_FAST = 1<<13
DPFPDD_QUALITY_SCAN_WRONG_DIRECTION = 1<<14
DPFPDD_QUALITY_READER_DIRTY = 1<<15
DPFPDD_IMAGE_FMT = c_uint
DPFPDD_IMG_FMT_PIXEL_BUFFER = 0
DPFPDD_IMG_FMT_ANSI381 = 0x001B0401
DPFPDD_IMG_FMT_ISOIEC19794 = 0x01010007
DPFPDD_IMAGE_PROC = c_uint
DPFPDD_IMG_PROC_DEFAULT = 0
DPFPDD_IMG_PROC_PIV = 1
DPFPDD_IMG_PROC_ENHANCED = 2
DPFPDD_IMG_PROC_ENHANCED_2 = 3
DPFPDD_IMG_PROC_UNPROCESSED = 0x52617749
DPFPDD_IMG_PROC_NONE = DPFPDD_IMG_PROC_DEFAULT
class DPFPDD_CAPTURE_PARAM(Structure):
    _fields_ = [
        ("size",c_uint),
        ("image_fmt",DPFPDD_IMAGE_FMT),
        ("image_proc",DPFPDD_IMAGE_PROC),
        ("image_res",c_uint)]
class DPFPDD_IMAGE_INFO(Structure):
    _fields_ = [
        ("size",c_uint),
        ("width",c_uint),
        ("height",c_uint),
        ("res",c_uint),
        ("bpp",c_uint)]
class DPFPDD_CAPTURE_RESULT(Structure):
    _fields_ = [
        ("size",c_uint),
        ("success",c_int),
        ("quality",DPFPDD_QUALITY),
        ("score",c_uint),
        ("info",DPFPDD_IMAGE_INFO)]
class DPFPDD_CAPTURE_CALLBACK_DATA_0(Structure):
    _fields_ = [("size",c_uint),("error",c_int),("capture_parm",DPFPDD_CAPTURE_PARAM),("capture_result",DPFPDD_CAPTURE_RESULT),("image_size",c_uint),("image_data",c_ubyte)]
class DPFPDD_CAPTURE_CALLBACK(c_void_p):
    _fields_ =[("callback_context",c_void_p),("reserved",c_uint),("callback_data_size",c_uint),("callback_data",c_void_p)] 
DPFPDD_LED_ID = c_uint
DPFPDD_LED_MAIN = 0x01
DPFPDD_LED_REJECT = 0x04
DPFPDD_LED_ACCEPT = 0x08
DPFPDD_LED_FINGER_DETECT = 0x10
DPFPDD_LED_AUX_1 = 0x14
DPFPDD_LED_AUX_2 = 0x18
DPFPDD_LED_PWM = 0x80
DPFPDD_LED_ALL = 0xffffffff
DPFPDD_LED_MODE_TYPE = c_uint
DPFPDD_LED_AUTO = 1
DPFPDD_LED_CLIENT = 2
DPFPDD_LED_CLIENT_PWM = 3
DPFPDD_LED_CLIENT_BLINK = 4
DPFPDD_LED_CMD_TYPE = c_uint
DPFPDD_LED_CMD_OFF = 0
DPFPDD_LED_CMD_ON = 1
DPFPDD_LED_CMD_PWM_MIN = 0
DPFPDD_LED_CMD_PWM_MAX = 255
DPFPDD_CLIENT_PWM_SUPPORTED = 0x80000000
DPFPDD_CLIENT_BLINK_SUPPORTED = 0x40000000
DPFPDD_PARMID = c_uint()
DPFPDD_PARMID_ROTATE = 0x100
DPFPDD_PARMID_FINGERDETECT_ENABLE = 0x104
DPFPDD_PARMID_IOMAP = 0x105
DPFPDD_PARMID_MOTIONDETECT_ENABLE = 0x107
DPFPDD_PARMID_FRAME_INTERVAL = 0x110
DPFPDD_PARMID_PTAPI_GET_GUID = 0x302
DPFPDD_PARMID_PAD_ENABLE = 0x200
DPFPDD_PARMID_PAD_DP_ENABLE = 0x201
DPFPDD_PARMID_PAD_CONFIDENCE = 0x202
DPFPDD_PARMID_SPOOFDETECT_ENABLE = DPFPDD_PARMID_PAD_DP_ENABLE
class DPFPDD_IOMAP(Structure):
    _fields_ = [("addr",c_ushort),("len",c_ushort),("buff",c_ubyte)]