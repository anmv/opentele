from __future__ import annotations
from typing import List, Dict, Tuple, TypeVar, Type
from .utils import *
import hashlib, os

_T = TypeVar("_T")


class DeviceInfo(object):
    def __init__(self, model, version) -> None:
        self.model = model
        self.version = version

    def __str__(self) -> str:
        return f"{self.model} {self.version}"


class SystemInfo(BaseObject):
    deviceList: List[DeviceInfo] = []
    device_modesl: List[str] = []
    system_versions: List[str] = []

    def __init__(self) -> None:
        pass

    @classmethod
    def RandomDevice(cls: Type[SystemInfo], unique_id: str = None) -> DeviceInfo:
        hash_id = cls._strtohashid(unique_id)
        return cls._RandomDevice(hash_id)

    @classmethod
    def _RandomDevice(cls, hash_id: int):
        cls.__gen__()
        return cls._hashtovalue(hash_id, cls.deviceList)

    @classmethod
    def __gen__(cls):
        raise NotImplementedError(
            f"{cls.__name__} device not supported for randomize yet"
        )

    @classmethod
    def _strtohashid(cls, unique_id: str = None):
        if unique_id != None and not isinstance(unique_id, str):
            unique_id = str(unique_id)

        byteid = os.urandom(32) if unique_id == None else unique_id.encode("utf-8")

        return int(hashlib.sha1(byteid).hexdigest(), 16) % (10 ** 12)

    @classmethod
    def _hashtorange(cls, hash_id: int, max, min=0):
        return hash_id % (max - min) + min

    @classmethod
    def _hashtovalue(cls, hash_id: int, values: List[_T]) -> _T:
        return values[hash_id % len(values)]

    @classmethod
    def _CleanAndSimplify(cls, text: str) -> str:
        return " ".join(word for word in text.split(" ") if word)


class GeneralDesktopDevice(SystemInfo):
    # Total: 794 devices, update Jan 10th 2022
    # Real device models that I crawled myself from the internet
    #
    # This is the values in HKEY_LOCAL_MACHINE\HARDWARE\DESCRIPTION\System\BIOS
    # including SystemFamily, SystemProductName, BaseBoardProduct
    #
    # Filtered any models that exceed 15 characters
    # just like tdesktop does in lib_base https://github.com/desktop-app/lib_base/blob/master/base/platform/win/base_info_win.cpp#L173
    #
    # Feel free to use
    #
    # Sources: https://answers.microsoft.com/, https://www.techsupportforum.com/ and https://www.bleepingcomputer.com/

    # device_models = [
    #     "0000000000",
    #     "0133D9",
    #     "03X0MN",
    #     "04GJJT",
    #     "04VWF2",
    #     "04WT2G",
    #     "05DN3X",
    #     "05FFDN",
    #     "0679",
    #     "0692FT",
    #     "06CDVY",
    #     "07JNH0",
    #     "0841B1A",
    #     "0874P6",
    #     "08VFX1",
    #     "095TWY",
    #     "09DKKT",
    #     "0C1D71",
    #     "0GDG8Y",
    #     "0H0CC0",
    #     "0H869M",
    #     "0J797R",
    #     "0JC474",
    #     "0KM92T",
    #     "0KP0FT",
    #     "0KV3RP",
    #     "0KWVT8",
    #     "0M277C",
    #     "0M332H",
    #     "0M9XW4",
    #     "0MYG77",
    #     "0N7TVV",
    #     "0NWWY0",
    #     "0P270J",
    #     "0PD9KD",
    #     "0PPYW4",
    #     "0R1203",
    #     "0R849J",
    #     "0T105W",
    #     "0TP406",
    #     "0U785D",
    #     "0UU795",
    #     "0WCNK6",
    #     "0Y2MRG",
    #     "0YF8P5",
    #     "1005P",
    #     "1005PE",
    #     "10125",
    #     "103C_53307F",
    #     "103C_53307F G=D",
    #     "103C_53311M HP",
    #     "103C_53316J",
    #     "103C_53316J G=D",
    #     "103C_5335KV",
    #     "103C_5336AN",
    #     "1066AWU",
    #     "110-050eam",
    #     "122-YW-E173",
    #     "131-GT-E767",
    #     "1425",
    #     "1494",
    #     "1496",
    #     "1633",
    #     "181D",
    #     "1849",
    #     "18F9",
    #     "198C",
    #     "1998",
    #     "20060",
    #     "20216",
    #     "20245",
    #     "20250",
    #     "20266",
    #     "20351",
    #     "20384",
    #     "20ATCTO1WW",
    #     "20AWA161TH",
    #     "20BECTO1WW",
    #     "20HD005EUS",
    #     "20HES2SF00",
    #     "20V9",
    #     "2166",
    #     "216C",
    #     "2248",
    #     "22CD",
    #     "2349G5P",
    #     "2378DHU",
    #     "2A9A",
    #     "2AB1",
    #     "2AC8",
    #     "2AE0",
    #     "304Bh",
    #     "3060",
    #     "30B9",
    #     "30DC",
    #     "30F7",
    #     "3600",
    #     "3624",
    #     "3627",
    #     "3642",
    #     "3646h",
    #     "3679CTO",
    #     "3717",
    #     "4157RC2",
    #     "4313CTO",
    #     "500-056",
    #     "600-1305t",
    #     "600-1370",
    #     "60073",
    #     "740U5L",
    #     "765802U",
    #     "80B8",
    #     "80C4",
    #     "80D0",
    #     "80E3",
    #     "80E5",
    #     "80E9",
    #     "80FC",
    #     "80RU",
    #     "80S7",
    #     "80Y7",
    #     "8114",
    #     "81DE",
    #     "81EF",
    #     "81H9",
    #     "81MU",
    #     "81VV",
    #     "8216",
    #     "8217",
    #     "82KU",
    #     "838F",
    #     "843B",
    #     "844C",
    #     "84A6",
    #     "84DA",
    #     "8582",
    #     "86F9",
    #     "8786",
    #     "8I945PL-G",
    #     "90NC001MUS",
    #     "90NC00JBUS",
    #     "945GT-GN",
    #     "965P-S3",
    #     "970A-G/3.1",
    #     "980DE3/U3S3",
    #     "990FXA-UD3",
    #     "A320M-S2H",
    #     "A320M-S2H-CF",
    #     "A55M-DGS",
    #     "A58MD",
    #     "A78XA-A2T",
    #     "A7DA 3 series",
    #     "A88X-PLUS",
    #     "AB350 Gaming K4",
    #     "AO533",
    #     "ASUS MB",
    #     "AX3400",
    #     "Acer Desktop",
    #     "Acer Nitro 5",
    #     "Alienware",
    #     "Alienware 17",
    #     "Alienware 17 R2",
    #     "Alienware 18",
    #     "Alienware X51",
    #     "Alienware m15",
    #     "All Series",
    #     "Aspire 4520",
    #     "Aspire 4736Z",
    #     "Aspire 5",
    #     "Aspire 5250",
    #     "Aspire 5252",
    #     "Aspire 5536",
    #     "Aspire 5538G",
    #     "Aspire 5732Z",
    #     "Aspire 5735",
    #     "Aspire 5738",
    #     "Aspire 5740",
    #     "Aspire 6930G",
    #     "Aspire 8950G",
    #     "Aspire A515-51G",
    #     "Aspire E5-575G",
    #     "Aspire M3641",
    #     "Aspire M5-581T",
    #     "Aspire M5-581TG",
    #     "Aspire M5201",
    #     "Aspire M5802",
    #     "Aspire M5811",
    #     "Aspire M7300",
    #     "Aspire R5-571TG",
    #     "Aspire T180",
    #     "Aspire V3-574G",
    #     "Aspire V5-473G",
    #     "Aspire V5-552P",
    #     "Aspire VN7-792G",
    #     "Aspire X1301",
    #     "Aspire X1700",
    #     "Aspire X3400G",
    #     "Aspire one",
    #     "Asterope",
    #     "Aurora",
    #     "Aurora R5",
    #     "Aurora-R4",
    #     "B360M D3H-CF",
    #     "B360M-D3H",
    #     "B450M DS3H",
    #     "B450M DS3H-CF",
    #     "B550 MB",
    #     "B550M DS3H",
    #     "B560 MB",
    #     "B560M DS3H",
    #     "B85M-D2V",
    #     "B85M-G",
    #     "BDW",
    #     "Boston",
    #     "Burbank",
    #     "C40",
    #     "CELSIUS R640",
    #     "CG1330",
    #     "CG5290",
    #     "CG8270",
    #     "CM1630",
    #     "CathedralPeak",
    #     "Charmander_KL",
    #     "CloverTrail",
    #     "Cuba MS-7301",
    #     "D102GGC2",
    #     "D900T",
    #     "D945GCL",
    #     "DG41WV",
    #     "DH61WW",
    #     "DH67CL",
    #     "DH77EB",
    #     "DP55WB",
    #     "DT1412",
    #     "DX4300",
    #     "DX4831",
    #     "DX4860",
    #     "DX58SO",
    #     "Dazzle_RL",
    #     "Default string",
    #     "Dell DM061",
    #     "Dell DV051",
    #     "Dell DXC061",
    #     "Dell XPS420",
    #     "Dell XPS720",
    #     "Desktop",
    #     "Dimension 3000",
    #     "Dimension 4700",
    #     "Dimension E521",
    #     "Durian 7A1",
    #     "EP35-DS3",
    #     "EP35-DS3R",
    #     "EP35-DS4",
    #     "EP35C-DS3R",
    #     "EP43-DS3L",
    #     "EP45-DS3L",
    #     "EP45-UD3L",
    #     "EP45-UD3LR",
    #     "EP45-UD3P",
    #     "EP45-UD3R",
    #     "EP45T-UD3LR",
    #     "ET1831",
    #     "EX58-UD3R",
    #     "Eee PC",
    #     "Eureka3",
    #     "Extensa 5620",
    #     "Extensa 7620",
    #     "F2A88X-D3HP",
    #     "F5SL",
    #     "F71IX1",
    #     "FJNB215",
    #     "FM2A88X Pro3+",
    #     "FMCP7AM&#160;",
    #     "Freed_CFS",
    #     "G1.Assassin2",
    #     "G31M-ES2L",
    #     "G31MVP",
    #     "G31T-M2",
    #     "G33M-DS2R",
    #     "G41M-Combo",
    #     "G41M-ES2L",
    #     "G41MT-S2P",
    #     "G53JW",
    #     "G53SW",
    #     "G55VW",
    #     "G60JX",
    #     "G73Sw",
    #     "GA-73PVM-S2H",
    #     "GA-770T-USB3",
    #     "GA-78LMT-S2P",
    #     "GA-78LMT-USB3",
    #     "GA-790FXTA-UD5",
    #     "GA-870A-UD3",
    #     "GA-880GM-D2H",
    #     "GA-880GM-UD2H",
    #     "GA-880GM-USB3",
    #     "GA-880GMA-USB3",
    #     "GA-890GPA-UD3H",
    #     "GA-890XA-UD3",
    #     "GA-970A-D3",
    #     "GA-EA790X-DS4",
    #     "GA-MA74GM-S2H",
    #     "GA-MA770-UD3",
    #     "GA-MA770T-UD3",
    #     "GA-MA770T-UD3P",
    #     "GA-MA785GM-US2H",
    #     "GA-MA785GT-UD3H",
    #     "GA-MA78G-DS3H",
    #     "GA-MA78LM-S2H",
    #     "GA-MA790FX-DQ6",
    #     "GA-MA790X-DS4",
    #     "GA-MA790X-UD4",
    #     "GA401IV",
    #     "GA502IU",
    #     "GE60 2OC\\2OE",
    #     "GF8200E",
    #     "GL502VMK",
    #     "GL502VML",
    #     "GL552VW",
    #     "GL553VD",
    #     "GT5636E",
    #     "GT5654",
    #     "GT5674",
    #     "GT70 2OC/2OD",
    #     "Gateway Desktop",
    #     "Gateway M280",
    #     "Godzilla-N10",
    #     "H110M-A/M.2",
    #     "H110M-DVS R3.0",
    #     "H55-USB3",
    #     "H55M-S2V",
    #     "H61M-C",
    #     "H61M-HVS",
    #     "H61MXL/H61MXL-K",
    #     "H67M-D2-B3",
    #     "H81H3-AM",
    #     "H81M-D PLUS",
    #     "H87-D3H",
    #     "H87-D3H-CF",
    #     "H87-HD3",
    #     "H97-D3H",
    #     "H97M Pro4",
    #     "HP 15",
    #     "HP 620",
    #     "HP All-in-One 22-c1xx",
    #     "HP Compaq 6720s",
    #     "HP Compaq 8000 Elite SFF",
    #     "HP Compaq 8100 Elite CMT",
    #     "HP Compaq 8200 Elite CMT",
    #     "HP Compaq 8200 Elite USDT",
    #     "HP Compaq dc7800p Convertible",
    #     "HP ENVY",
    #     "HP ENVY 14",
    #     "HP ENVY 14 Sleekbook",
    #     "HP ENVY TS m6 Sleekbook",
    #     "HP ENVY x360 Convertible",
    #     "HP ENVY x360 m6 Convertible",
    #     "HP Elite x2 1012 G1",
    #     "HP EliteBook 6930p",
    #     "HP EliteBook 8540w",
    #     "HP EliteDesk 800 G1 SFF",
    #     "HP G62",
    #     "HP G70",
    #     "HP G7000",
    #     "HP HDX18",
    #     "HP Laptop 15-da0xxx",
    #     "HP Pavilion",
    #     "HP Pavilion 15",
    #     "HP Pavilion Gaming 690-0xxx",
    #     "HP Pavilion Gaming 790-0xxx",
    #     "HP Pavilion P6000 Series",
    #     "HP Pavilion Sleekbook 14",
    #     "HP Pavilion dm4",
    #     "HP Pavilion dv2700",
    #     "HP Pavilion dv3",
    #     "HP Pavilion dv4",
    #     "HP Pavilion dv5",
    #     "HP Pavilion dv6",
    #     "HP Pavilion dv7",
    #     "HP Pavilion g6",
    #     "HP ProBook 4320s",
    #     "HP ProBook 450 G2",
    #     "HP ProBook 4520s",
    #     "HP ProBook 4530s",
    #     "HP Spectre x360 Convertible",
    #     "HPE-498d",
    #     "HPE-560Z",
    #     "IDEAPAD",
    #     "IMEDIA MC 2569",
    #     "INVALID",
    #     "ISKAA",
    #     "IdeaCentre K330",
    #     "Infoway",
    #     "Inspiron",
    #     "Inspiron 1525",
    #     "Inspiron 1526",
    #     "Inspiron 1545",
    #     "Inspiron 1564",
    #     "Inspiron 1750",
    #     "Inspiron 3891",
    #     "Inspiron 518",
    #     "Inspiron 5570",
    #     "Inspiron 560",
    #     "Inspiron 570",
    #     "Inspiron 6000",
    #     "Inspiron 620",
    #     "Inspiron 660",
    #     "Inspiron 7559",
    #     "Inspiron 7720",
    #     "Inspiron N5010",
    #     "Inspiron N7010",
    #     "Intel_Mobile",
    #     "Ironman_SK",
    #     "K40ID",
    #     "K43SA",
    #     "K46CM",
    #     "K50AB",
    #     "K52JB",
    #     "K53SV",
    #     "K55VD",
    #     "K56CM",
    #     "KL3",
    #     "KM400A-8237",
    #     "Kabini CRB",
    #     "LENOVO",
    #     "LEONITE",
    #     "LH700",
    #     "LIFEBOOK SH561",
    #     "LNVNB161216",
    #     "LX6810-01",
    #     "LY325",
    #     "Lancer 5A2",
    #     "Lancer 5B2",
    #     "Latitude",
    #     "Latitude 3410",
    #     "Latitude 5400",
    #     "Latitude 6430U",
    #     "Latitude 7420",
    #     "Latitude 7490",
    #     "Latitude D630",
    #     "Latitude E4300",
    #     "Latitude E5450",
    #     "Latitude E6330",
    #     "Latitude E6430",
    #     "Latitude E6510",
    #     "Latitude E6520",
    #     "Lenovo B50-70",
    #     "Lenovo G50-80",
    #     "Livermore8",
    #     "M11x R2",
    #     "M14xR2",
    #     "M15x",
    #     "M17x",
    #     "M2N-E",
    #     "M2N-SLI",
    #     "M2N-X",
    #     "M3A-H/HDMI",
    #     "M3A770DE",
    #     "M3N78-AM",
    #     "M4A785TD-M EVO",
    #     "M4A785TD-V EVO",
    #     "M4A78LT-M",
    #     "M4A78T-E",
    #     "M4A79 Deluxe",
    #     "M4A79XTD EVO",
    #     "M4A87TD/USB3",
    #     "M4A89GTD-PRO",
    #     "M4N68T",
    #     "M4N98TD EVO",
    #     "M5640/M3640",
    #     "M570U",
    #     "M5A78L LE",
    #     "M5A78L-M LE",
    #     "M5A78L-M/USB3",
    #     "M5A87",
    #     "M5A88-V EVO",
    #     "M5A97",
    #     "M5A97 LE R2.0",
    #     "M5A97 R2.0",
    #     "M68MT-S2",
    #     "M750SLI-DS4",
    #     "M771CUH Lynx",
    #     "MA51_HX",
    #     "MAXIMUS V GENE",
    #     "MCP61PM-AM",
    #     "MCP73PV",
    #     "MJ-7592",
    #     "MS-16GC",
    #     "MS-1727",
    #     "MS-17K3",
    #     "MS-6714",
    #     "MS-7094",
    #     "MS-7325",
    #     "MS-7327",
    #     "MS-7350",
    #     "MS-7360",
    #     "MS-7366",
    #     "MS-7502",
    #     "MS-7514",
    #     "MS-7519",
    #     "MS-7522",
    #     "MS-7529",
    #     "MS-7549",
    #     "MS-7577",
    #     "MS-7583",
    #     "MS-7586",
    #     "MS-7592",
    #     "MS-7599",
    #     "MS-7637",
    #     "MS-7640",
    #     "MS-7641",
    #     "MS-7673",
    #     "MS-7678",
    #     "MS-7680",
    #     "MS-7681",
    #     "MS-7751",
    #     "MS-7752",
    #     "MS-7793",
    #     "MS-7816",
    #     "MS-7817",
    #     "MS-7821",
    #     "MS-7850",
    #     "MS-7917",
    #     "MS-7972",
    #     "MS-7977",
    #     "MS-7A34",
    #     "MS-7A62",
    #     "MS-7B00",
    #     "MS-7B46",
    #     "MS-7C02",
    #     "MS-7C75",
    #     "MX8734",
    #     "Makalu",
    #     "Mi Laptop",
    #     "N53SV",
    #     "N552VX",
    #     "N55SF",
    #     "N61Jq",
    #     "N68-GS3 UCC",
    #     "N68C-S UCC",
    #     "N76VZ",
    #     "N81Vp",
    #     "NFORCE 680i SLI",
    #     "NL8K_NL9K",
    #     "NL9K",
    #     "NP740U5L-Y03US",
    #     "NT500R5H-X51M",
    #     "NUC7i7DNB",
    #     "NUC7i7DNHE",
    #     "NV52 Series",
    #     "NV54 Series",
    #     "NWQAE",
    #     "Narra6",
    #     "Nettle2",
    #     "Nitro AN515-52",
    #     "Not Applicable",
    #     "Notebook PC",
    #     "OEM",
    #     "OptiPlex 330",
    #     "OptiPlex 745",
    #     "OptiPlex 755",
    #     "OptiPlex 9010",
    #     "OptiPlex GX520",
    #     "P170EM",
    #     "P170HMx",
    #     "P35-DS3L",
    #     "P43-A7",
    #     "P4M90-M7A",
    #     "P4P800",
    #     "P4S-LA",
    #     "P55-UD4",
    #     "P55-US3L",
    #     "P55-USB3",
    #     "P55A-UD3",
    #     "P55A-UD3R",
    #     "P55A-UD4",
    #     "P55A-UD4P",
    #     "P55M-UD2",
    #     "P5E-VM HDMI",
    #     "P5K PRO",
    #     "P5N32-E SLI",
    #     "P5Q SE2",
    #     "P5Q-PRO",
    #     "P5QL PRO",
    #     "P5QL-E",
    #     "P5QPL-AM",
    #     "P67A-UD3-B3",
    #     "P67A-UD4-B3",
    #     "P67A-UD5-B3",
    #     "P6T",
    #     "P6T DELUXE V2",
    #     "P6T SE",
    #     "P6X58D PREMIUM",
    #     "P6X58D-E",
    #     "P7477A-ABA 751n",
    #     "P7P55D",
    #     "P7P55D-E",
    #     "P7P55D-E LX",
    #     "P8610",
    #     "P8H61-M LE/USB3",
    #     "P8H67-M PRO",
    #     "P8P67",
    #     "P8P67 PRO",
    #     "P8P67-M PRO",
    #     "P8Z68-V LE",
    #     "P8Z68-V LX",
    #     "P8Z68-V PRO",
    #     "P8Z77-V",
    #     "P8Z77-V LX",
    #     "P9X79 LE",
    #     "PM800-8237",
    #     "PORTEGE R705",
    #     "PRIME A320M-K",
    #     "PRIME B450M-A",
    #     "PRIME X470-PRO",
    #     "PRIME Z270-A",
    #     "PRIME Z390-A",
    #     "PRIME Z490-V",
    #     "PWWAA",
    #     "Polaris_HW",
    #     "Portable PC",
    #     "PowerEdge 2950",
    #     "PowerEdge R515",
    #     "PowerEdge T420",
    #     "Precision",
    #     "Precision 7530",
    #     "Precision M6500",
    #     "Proteus IV",
    #     "QL5",
    #     "Qosmio X505",
    #     "R560-LAR39E",
    #     "ROG",
    #     "RS690M2MA",
    #     "RS780HVF",
    #     "RV415/RV515",
    #     "S500CA",
    #     "S550CM",
    #     "SABERTOOTH P67",
    #     "SABERTOOTH X58",
    #     "SAMSUNG ATIV",
    #     "SG41",
    #     "SJV50PU",
    #     "SKL",
    #     "SM80_HR",
    #     "SQ9204",
    #     "STRIKER II NSE",
    #     "SVE14125CLB",
    #     "SVE14A25CVW",
    #     "SX2801",
    #     "SX2802",
    #     "Satellite A200",
    #     "Satellite A215",
    #     "Satellite A300D",
    #     "Satellite A500",
    #     "Satellite A505",
    #     "Satellite A665",
    #     "Satellite A665D",
    #     "Satellite C660",
    #     "Satellite C855D",
    #     "Satellite L635",
    #     "Satellite L650",
    #     "Satellite P205D",
    #     "Satellite R630",
    #     "Shark 2.0",
    #     "Studio 1458",
    #     "Studio 1555",
    #     "Studio 1558",
    #     "Studio 1747",
    #     "Studio XPS 1640",
    #     "Studio XPS 7100",
    #     "Studio XPS 9100",
    #     "Suntory_KL",
    #     "Swift 3",
    #     "Swift SF314-52",
    #     "T5212",
    #     "T5226",
    #     "T9408UK",
    #     "TA790GX 128M",
    #     "TA790GX A3+",
    #     "TA790GXB3",
    #     "TA790GXE",
    #     "TA790GXE 128M",
    #     "TA990FXE",
    #     "TM1963",
    #     "TPower I55",
    #     "TZ77XE3",
    #     "ThinkPad L440",
    #     "ThinkPad T430",
    #     "ThinkPad T440p",
    #     "ThinkPad T470",
    #     "ThinkPad T510",
    #     "ThinkPad T540p",
    #     "Type1Family",
    #     "U50F",
    #     "UD3R-SLI",
    #     "UL30VT",
    #     "USOPP_BH",
    #     "UX303UB",
    #     "UX32VD",
    #     "VAIO",
    #     "VGN-NR498E",
    #     "VGN-NW265F",
    #     "VGN-SR45H_B",
    #     "VIOLET6",
    #     "VPCEB27FD",
    #     "VPCEE31FX",
    #     "VPCF11QFX",
    #     "VPCF1290X",
    #     "VPCF22C5E",
    #     "VPCF22J1E",
    #     "VPCS111FM",
    #     "Veriton E430",
    #     "VivoBook",
    #     "Vostro",
    #     "Vostro 1520",
    #     "Vostro 1720",
    #     "Vostro1510",
    #     "W35xSS_370SS",
    #     "W55xEU",
    #     "X421JQ",
    #     "X510UNR",
    #     "X550CA",
    #     "X550JX",
    #     "X555LAB",
    #     "X556UB",
    #     "X556UF",
    #     "X570 GAMING X",
    #     "X570 MB",
    #     "X58-USB3",
    #     "X58A-UD3R",
    #     "X58A-UD5",
    #     "X58A-UD7",
    #     "XPS",
    #     "XPS 13 9305",
    #     "XPS 13 9370",
    #     "XPS 15 9550",
    #     "XPS 15 9560",
    #     "XPS 630i",
    #     "XPS 730",
    #     "XPS 730X",
    #     "XPS 8300",
    #     "XPS 8700",
    #     "XPS 8940",
    #     "XPS A2420",
    #     "XPS L501X",
    #     "XPS L701X",
    #     "XPS M1530",
    #     "YOGA 530-14ARR",
    #     "YOGA 920-13IKB",
    #     "YOGATablet2",
    #     "Yoga2",
    #     "Z10PE-D8 WS",
    #     "Z170 PRO GAMING",
    #     "Z170-E",
    #     "Z170X-Gaming 5",
    #     "Z170X-UD3",
    #     "Z170X-UD3-CF",
    #     "Z370P D3",
    #     "Z370P D3-CF",
    #     "Z68 Pro3",
    #     "Z68A-D3-B3",
    #     "Z68A-D3H-B3",
    #     "Z68AP-D3",
    #     "Z68MA-D2H-B3",
    #     "Z68X-UD3H-B3",
    #     "Z68XP-UD3",
    #     "Z68XP-UD4",
    #     "Z77 Pro4",
    #     "Z77X-D3H",
    #     "Z87 Extreme6",
    #     "Z87-D3HP",
    #     "Z87-D3HP-CF",
    #     "Z87M Extreme4",
    #     "Z87N-WIFI",
    #     "Z87X-OC",
    #     "Z87X-OC-CF",
    #     "Z87X-UD4H",
    #     "Z97-A",
    #     "Z97-A-USB31",
    #     "Z97-AR",
    #     "Z97-C",
    #     "Z97-PRO GAMER",
    #     "Z97X-Gaming 7",
    #     "eMachines E725",
    #     "h8-1070t",
    #     "h8-1534",
    #     "imedia S3720",
    #     "ixtreme M5800",
    #     "p6654y",
    #     "p6710f",
    # ]

    device_models = {
        # Dell Latitude Business Laptops (2019-2025)
        "L9430": {"manufacturer": "Dell", "model": "Latitude 9430", "year": 2022, "type": "laptop"},
        "L7330": {"manufacturer": "Dell", "model": "Latitude 7330", "year": 2022, "type": "laptop"},
        "L7430": {"manufacturer": "Dell", "model": "Latitude 7430", "year": 2022, "type": "laptop"},
        "L7530": {"manufacturer": "Dell", "model": "Latitude 7530", "year": 2022, "type": "laptop"},
        "L5430": {"manufacturer": "Dell", "model": "Latitude 5430", "year": 2022, "type": "laptop"},
        "L5530": {"manufacturer": "Dell", "model": "Latitude 5530", "year": 2022, "type": "laptop"},

        # Dell XPS Premium Series
        "XPS9320": {"manufacturer": "Dell", "model": "XPS 13 Plus 9320", "year": 2022, "type": "laptop"},
        "XPS1340": {"manufacturer": "Dell", "model": "XPS 13 9340", "year": 2024, "type": "laptop"},
        "XPS1440": {"manufacturer": "Dell", "model": "XPS 14 9440", "year": 2024, "type": "laptop"},
        "XPS1640": {"manufacturer": "Dell", "model": "XPS 16 9640", "year": 2024, "type": "laptop"},

        # Dell OptiPlex Business Desktops
        "O7020": {"manufacturer": "Dell", "model": "OptiPlex 7020", "year": 2024, "type": "desktop"},
        "O5090": {"manufacturer": "Dell", "model": "OptiPlex 5090", "year": 2021, "type": "desktop"},
        "O3000": {"manufacturer": "Dell", "model": "OptiPlex 3000", "year": 2022, "type": "desktop"},

        # Dell Precision Workstations
        "P5470": {"manufacturer": "Dell", "model": "Precision 5470", "year": 2022, "type": "laptop"},
        "P5570": {"manufacturer": "Dell", "model": "Precision 5570", "year": 2022, "type": "laptop"},
        "P5770": {"manufacturer": "Dell", "model": "Precision 5770", "year": 2022, "type": "laptop"},

        # HP EliteBook Business Series (G9-G11)
        "EB630G9": {"manufacturer": "HP", "model": "EliteBook 630 G9", "year": 2022, "type": "laptop"},
        "EB640G9": {"manufacturer": "HP", "model": "EliteBook 640 G9", "year": 2022, "type": "laptop"},
        "EB650G9": {"manufacturer": "HP", "model": "EliteBook 650 G9", "year": 2022, "type": "laptop"},
        "EB640G10": {"manufacturer": "HP", "model": "EliteBook 640 G10", "year": 2023, "type": "laptop"},
        "EB840G11": {"manufacturer": "HP", "model": "EliteBook 840 G11", "year": 2024, "type": "laptop"},

        # HP ProBook Mid-Range Business
        "PB440G9": {"manufacturer": "HP", "model": "ProBook 440 G9", "year": 2022, "type": "laptop"},
        "PB450G9": {"manufacturer": "HP", "model": "ProBook 450 G9", "year": 2022, "type": "laptop"},
        "PB440G10": {"manufacturer": "HP", "model": "ProBook 440 G10", "year": 2023, "type": "laptop"},

        # HP Envy Consumer Premium
        "ENVYx360": {"manufacturer": "HP", "model": "Envy x360 13", "year": 2022, "type": "laptop"},
        "ENVYx36014": {"manufacturer": "HP", "model": "Envy x360 14", "year": 2024, "type": "laptop"},
        "ENVYx36016": {"manufacturer": "HP", "model": "Envy x360 16", "year": 2024, "type": "laptop"},
        "ENVY17": {"manufacturer": "HP", "model": "Envy 17", "year": 2024, "type": "laptop"},

        # HP Pavilion Consumer
        "PAero13": {"manufacturer": "HP", "model": "Pavilion Aero 13", "year": 2024, "type": "laptop"},
        "PPLus16": {"manufacturer": "HP", "model": "Pavilion Plus 16", "year": 2024, "type": "laptop"},

        # Lenovo ThinkPad T/X/P Series (2019-2025)
        "20T0CTO1WW": {"manufacturer": "Lenovo", "model": "ThinkPad T14 Gen 1", "year": 2020, "type": "laptop"},
        "20T1CTO1WW": {"manufacturer": "Lenovo", "model": "ThinkPad T14s Gen 1", "year": 2020, "type": "laptop"},
        "TPT14sG4": {"manufacturer": "Lenovo", "model": "ThinkPad T14s Gen 4", "year": 2023, "type": "laptop"},
        "TPX13s": {"manufacturer": "Lenovo", "model": "ThinkPad X13s", "year": 2022, "type": "laptop"},
        "TPP1G7": {"manufacturer": "Lenovo", "model": "ThinkPad P1 Gen 7", "year": 2024, "type": "laptop"},
        "TPX915A": {"manufacturer": "Lenovo", "model": "ThinkPad X9 15 Aura Edition", "year": 2025, "type": "laptop"},

        # Lenovo Legion Gaming
        "LGN5": {"manufacturer": "Lenovo", "model": "Legion 5", "year": 2020, "type": "laptop"},
        "LGN7": {"manufacturer": "Lenovo", "model": "Legion 7", "year": 2020, "type": "laptop"},
        "LGNP5G8": {"manufacturer": "Lenovo", "model": "Legion Pro 5 Gen 8", "year": 2023, "type": "laptop"},
        "LGN9i": {"manufacturer": "Lenovo", "model": "Legion 9i", "year": 2023, "type": "laptop"},

        # Lenovo IdeaPad Consumer
        "IPPro": {"manufacturer": "Lenovo", "model": "IdeaPad Pro", "year": 2023, "type": "laptop"},
        "IPSlim": {"manufacturer": "Lenovo", "model": "IdeaPad Slim", "year": 2023, "type": "laptop"},
        "IP2in1": {"manufacturer": "Lenovo", "model": "IdeaPad 2-in-1", "year": 2023, "type": "laptop"},

        # ASUS TUF Gaming
        "TUFF15": {"manufacturer": "ASUS", "model": "TUF Gaming F15", "year": 2022, "type": "laptop"},
        "TUFF17": {"manufacturer": "ASUS", "model": "TUF Gaming F17", "year": 2022, "type": "laptop"},
        "TUFA15": {"manufacturer": "ASUS", "model": "TUF Gaming A15", "year": 2022, "type": "laptop"},
        "TUFA17": {"manufacturer": "ASUS", "model": "TUF Gaming A17", "year": 2022, "type": "laptop"},
        "TUFA15G2": {"manufacturer": "ASUS", "model": "TUF Gaming A15 Gen 2", "year": 2023, "type": "laptop"},
        "TUFD15": {"manufacturer": "ASUS", "model": "TUF Dash F15", "year": 2022, "type": "laptop"},

        # ASUS ROG Gaming
        "G401x": {"manufacturer": "ASUS", "model": "ROG Zephyrus G14", "year": 2024, "type": "laptop"},
        "GU605": {"manufacturer": "ASUS", "model": "ROG Zephyrus G16", "year": 2024, "type": "laptop"},
        "G614x": {"manufacturer": "ASUS", "model": "ROG Strix G16", "year": 2024, "type": "laptop"},
        "GZ302": {"manufacturer": "ASUS", "model": "ROG Flow Z13", "year": 2025, "type": "laptop"},

        # ASUS ZenBook/VivoBook
        "UX3402": {"manufacturer": "ASUS", "model": "ZenBook 14 OLED", "year": 2024, "type": "laptop"},
        "M1605": {"manufacturer": "ASUS", "model": "VivoBook 16 M1605", "year": 2023, "type": "laptop"},

        # Acer Nitro Gaming
        "AN515": {"manufacturer": "Acer", "model": "Nitro 5", "year": 2022, "type": "laptop"},
        "ANV15AI": {"manufacturer": "Acer", "model": "Nitro V 15 AI", "year": 2025, "type": "laptop"},
        "ANV17AI": {"manufacturer": "Acer", "model": "Nitro V 17 AI", "year": 2025, "type": "laptop"},
        "ANV14AI": {"manufacturer": "Acer", "model": "Nitro V 14 AI", "year": 2025, "type": "laptop"},
        "ANV16AI": {"manufacturer": "Acer", "model": "Nitro V 16 AI", "year": 2025, "type": "laptop"},

        # Acer Swift Ultrabooks
        "SF314": {"manufacturer": "Acer", "model": "Swift 3", "year": 2022, "type": "laptop"},
        "SFG14": {"manufacturer": "Acer", "model": "Swift Go 14", "year": 2024, "type": "laptop"},
        "SFG16": {"manufacturer": "Acer", "model": "Swift Go 16", "year": 2024, "type": "laptop"},
        "SFE16": {"manufacturer": "Acer", "model": "Swift Edge 16", "year": 2024, "type": "laptop"},

        # Acer Predator Gaming
        "PH315": {"manufacturer": "Acer", "model": "Predator Helios 300", "year": 2022, "type": "laptop"},
        "PH16AI": {"manufacturer": "Acer", "model": "Predator Helios 16 AI", "year": 2025, "type": "laptop"},
        "PH18AI": {"manufacturer": "Acer", "model": "Predator Helios 18 AI", "year": 2025, "type": "laptop"},

        # Acer Aspire Budget
        "A515": {"manufacturer": "Acer", "model": "Aspire 5", "year": 2022, "type": "laptop"},
        "AV16": {"manufacturer": "Acer", "model": "Aspire Vero 16", "year": 2025, "type": "laptop"},

        # MSI Gaming Series
        "GS77": {"manufacturer": "MSI", "model": "Stealth GS77", "year": 2022, "type": "laptop"},
        "GS66": {"manufacturer": "MSI", "model": "Stealth GS66", "year": 2022, "type": "laptop"},
        "GE76": {"manufacturer": "MSI", "model": "Raider GE76", "year": 2022, "type": "laptop"},
        "GP76": {"manufacturer": "MSI", "model": "Vector GP76", "year": 2022, "type": "laptop"},
        "GP66": {"manufacturer": "MSI", "model": "Vector GP66", "year": 2022, "type": "laptop"},

        # MSI Creator/Business Series
        "CZ16": {"manufacturer": "MSI", "model": "Creator Z16", "year": 2022, "type": "laptop"},
        "CA16AI": {"manufacturer": "MSI", "model": "Creator A16 AI+", "year": 2024, "type": "laptop"},
        "PS13E": {"manufacturer": "MSI", "model": "Prestige 13 Evo", "year": 2023, "type": "laptop"},
        "PA16AI": {"manufacturer": "MSI", "model": "Prestige A16 AI+", "year": 2024, "type": "laptop"},
        "SE14FA13M": {"manufacturer": "MSI", "model": "Summit E14 Flip Evo A13M", "year": 2023, "type": "laptop"},
        "SA16AI": {"manufacturer": "MSI", "model": "Summit A16 AI+", "year": 2024, "type": "laptop"},

        # Gigabyte/AORUS Motherboards and Systems
        "Z790AOR": {"manufacturer": "Gigabyte", "model": "Z790 AORUS", "year": 2022, "type": "motherboard"},
        "Z790AORX": {"manufacturer": "Gigabyte", "model": "Z790 AORUS X Gen", "year": 2023, "type": "motherboard"},
        "X870EAXT": {"manufacturer": "Gigabyte", "model": "X870E AORUS XTREME AI TOP", "year": 2024,
                     "type": "motherboard"},
        "X870EAE7": {"manufacturer": "Gigabyte", "model": "X870E AORUS ELITE WIFI7", "year": 2024,
                     "type": "motherboard"},
        "B650EAM": {"manufacturer": "Gigabyte", "model": "B650E AORUS Master", "year": 2023, "type": "motherboard"},
        "AOR500S": {"manufacturer": "Gigabyte", "model": "AORUS STEALTH 500", "year": 2022, "type": "desktop"},

        # Microsoft Surface Devices (2022-2025)
        "Surface_Pro_9": {"manufacturer": "Microsoft", "model": "Surface Pro 9", "year": 2022, "type": "laptop"},
        "Surface_Pro_10": {"manufacturer": "Microsoft", "model": "Surface Pro 10", "year": 2024, "type": "laptop"},
        "Surface_Pro_11": {"manufacturer": "Microsoft", "model": "Surface Pro 11", "year": 2024, "type": "laptop"},
        "Surface_Laptop_5": {"manufacturer": "Microsoft", "model": "Surface Laptop 5", "year": 2022, "type": "laptop"},
        "Surface_Laptop_6": {"manufacturer": "Microsoft", "model": "Surface Laptop 6", "year": 2024, "type": "laptop"},
        "Surface_Go_4": {"manufacturer": "Microsoft", "model": "Surface Go 4", "year": 2023, "type": "laptop"}
    }


class WindowsDevice(GeneralDesktopDevice):
    system_versions = ["Windows 11", "Windows 10", "Windows 8", "Windows 8.1", "Windows 7"]

    deviceList: List[DeviceInfo] = []

    @classmethod
    def __gen__(cls: Type[WindowsDevice]) -> None:

        if len(cls.deviceList) == 0:

            results: List[DeviceInfo] = []

            for model in cls.device_models:
                model = cls._CleanAndSimplify(model.replace("_", ""))
                for version in cls.system_versions:
                    results.append(DeviceInfo(model, version))

            cls.deviceList = results


class LinuxDevice(GeneralDesktopDevice):
    system_versions: List[str] = []
    deviceList: List[DeviceInfo] = []

    @classmethod
    def __gen__(cls: Type[LinuxDevice]) -> None:

        if len(cls.system_versions) == 0:
            # https://github.com/desktop-app/lib_base/blob/master/base/platform/linux/base_info_linux.cpp#L129

            # ? Purposely reduce the amount of devices parameter to generate deviceList more quickly
            enviroments = [
                "GNOME",
                "MATE",
                "XFCE",
                "Cinnamon",
                "Unity",
                "ubuntu",
                "LXDE",
                "KDE",
                "Plasma",
                "Hyprland",  # популярный Wayland compositor
                "Sway",  # i3-совместимый для Wayland
            ]

            wayland = ["Wayland", "XWayland", "X11"]

            libcNames = ["glibc"]
            libcVers = ["2.36", "2.37", "2.38", "2.39", "2.40",
                        "2.41", "2.42"]

            # enviroments = [
            #     "GNOME", "MATE", "XFCE", "Cinnamon", "X-Cinnamon",
            #     "Unity", "ubuntu", "GNOME-Classic", "LXDE"
            # ]

            # wayland = ["Wayland", "XWayland", "X11"]

            # libcNames = ["glibc", "libc"]
            # libcVers = [
            #     "2.20", "2.21", "2.22", "2.23", "2.24", "2.25", "2.26", "2.27",
            #     "2.28", "2.29", "2.30", "2.31", "2.32", "2.33", "2.34"
            # ]

            def getitem(group: List[List[str]], prefix: str = "") -> List[str]:

                prefix = "" if prefix == "" else prefix + " "
                results = []
                if len(group) == 1:
                    for item in group[0]:
                        results.append(prefix + item)
                    return results

                for item in group[0]:
                    results.extend(getitem(group[1:], prefix + item))

                return results

            libcFullNames = getitem([libcNames, libcVers], "")

            cls.system_versions = getitem(
                [enviroments, wayland, libcFullNames], "Linux"
            )

            results: List[DeviceInfo] = []

            for version in cls.system_versions:
                for model in cls.device_models:
                    results.append(DeviceInfo(model, version))

            cls.deviceList = results


class macOSDevice(GeneralDesktopDevice):
    deviceList: List[DeviceInfo] = []

    # Total: 54 device models, update Jan 10th 2022
    # Only list device models since 2013
    #
    # Sources:
    # Thanks to: https://mrmacintosh.com/list-of-mac-boardid-deviceid-model-identifiers-machine-models/
    #       and: https://github.com/brunerd/jamfTools/blob/main/EAs/macOSCompatibility.sh
    #
    # Remark: https://www.innerfence.com/howto/apple-ios-devices-dates-versions-instruction-sets
    # Added 12+ MacOS versions: https://apple.fandom.com/wiki/List_of_Mac_OS_versions

    device_models = [
        "iMac20,1",  # iMac (Retina 5K, 27-inch, 2020)	4 августа 2020 г.
        "iMac20,2",  # iMac (Retina 5K, 27-inch, 2020)	4 августа 2020 г.
        "iMac21,1",  # iMac (24-inch, M1, 2021)	20 апреля 2021 г.
        "iMac21,2",  # iMac (24-inch, M1, 2021)	20 апреля 2021 г.
        "MacBookAir9,1",  # MacBook Air (Retina, 13-inch, 2020)	18 марта 2020 г.
        "MacBookAir10,1",  # MacBook Air (M1, 2020)	10 ноября 2020 г.
        "MacBookPro16,2",  # MacBook Pro (13-inch, 2020, 4 TBT3)	4 мая 2020 г.
        "MacBookPro16,3",  # MacBook Pro (13-inch, 2020, 2 TBT3)	4 мая 2020 г.
        "MacBookPro17,1",  # MacBook Pro (13-inch, M1, 2020)	10 ноября 2020 г.
        "MacBookPro18,1",  # MacBook Pro (16-inch, 2021)	18 октября 2021 г.
        "MacBookPro18,2",  # MacBook Pro (16-inch, 2021)	18 октября 2021 г.
        "MacBookPro18,3",  # MacBook Pro (14-inch, 2021)	18 октября 2021 г.
        "MacBookPro18,4",  # MacBook Pro (14-inch, 2021)	18 октября 2021 г.
        "Macmini9,1",  # Mac mini (M1, 2020)	10 ноября 2020 г.
        "Mac13,1",  # Mac Studio (2022)	8 марта 2022 г.
        "Mac13,2",  # Mac Studio (2022)	8 марта 2022 г.
        "Mac14,2",  # MacBook Air (M2, 2022)	6 июня 2022 г.
        "Mac14,3",  # Mac mini (2023)	17 января 2023 г.
        "Mac14,5",  # MacBook Pro (14-inch, 2023)	17 января 2023 г.
        "Mac14,6",  # MacBook Pro (16-inch, 2023)	17 января 2023 г.
        "Mac14,7",  # MacBook Pro (13-inch, M2, 2022)	6 июня 2022 г.
        "Mac14,8",  # Mac Pro (2023)	5 июня 2023 г.
        "Mac14,9",  # MacBook Pro (14-inch, 2023)	17 января 2023 г.
        "Mac14,10",  # MacBook Pro (16-inch, 2023)	17 января 2023 г.
        "Mac14,12",  # Mac mini (2023)	17 января 2023 г.
        "Mac14,13",  # Mac Studio (2023)	5 июня 2023 г.
        "Mac14,14",  # Mac Studio (2023)	5 июня 2023 г.
        "Mac14,15",  # MacBook Air (15-inch, M2, 2023)	5 июня 2023 г.
        "Mac15,3",  # MacBook Pro (14-inch, Nov 2023)	30 октября 2023 г.
        "Mac15,4",  # iMac (24-inch, 2023)	30 октября 2023 г.
        "Mac15,5",  # iMac (24-inch, 2023)	30 октября 2023 г.
        "Mac15,6",  # MacBook Pro (14-inch, Nov 2023)	30 октября 2023 г.
        "Mac15,7",  # MacBook Pro (16-inch, Nov 2023)	30 октября 2023 г.
        "Mac15,8",  # MacBook Pro (14-inch, Nov 2023)	30 октября 2023 г.
        "Mac15,9",  # MacBook Pro (16-inch, Nov 2023)	30 октября 2023 г.
        "Mac15,10",  # MacBook Pro (14-inch, Nov 2023)	30 октября 2023 г.
        "Mac15,11",  # MacBook Pro (16-inch, Nov 2023)	30 октября 2023 г.
        "Mac15,12",  # MacBook Air (13-inch, M3, 2024)	4 марта 2024 г.
        "Mac15,13",  # MacBook Air (15-inch, M3, 2024)	4 марта 2024 г.
        "Mac16,1",  # MacBook Pro (14-inch, 2024)	30 октября 2024 г.
        "Mac16,2",  # iMac (24-inch, 2024)	28 октября 2024 г.
        "Mac16,3",  # iMac (24-inch, 2024)	28 октября 2024 г.
        "Mac16,5",  # MacBook Pro (16-inch, 2024)	30 октября 2024 г.
        "Mac16,6",  # MacBook Pro (14-inch, 2024)	30 октября 2024 г.
        "Mac16,7",  # MacBook Pro (16-inch, 2024)	30 октября 2024 г.
        "Mac16,8",  # MacBook Pro (14-inch, 2024)	30 октября 2024 г.
    ]

    # Source: https://support.apple.com/en-us/HT201222
    system_versions = [
        "macOS 11.0",
        "macOS 11.0.1",
        "macOS 11.1",
        "macOS 11.2",
        "macOS 11.2.1",
        "macOS 11.2.2",
        "macOS 11.2.3",
        "macOS 11.3",
        "macOS 11.3.1",
        "macOS 11.4",
        "macOS 11.5",
        "macOS 11.5.1",
        "macOS 11.5.2",
        "macOS 11.6",
        "macOS 11.6.1",
        "macOS 11.6.2",
        "macOS 12.0",
        "macOS 12.0.1",
        "macOS 12.1",
        "macOS 12.2",
        "macOS 12.2.1",
        "macOS 12.3",
        "macOS 12.3.1",
        "macOS 12.4",
        "macOS 12.5",
        "macOS 12.5.1",
        "macOS 12.6",
        "macOS 12.6.1",
        "macOS 12.6.2",
        "macOS 12.6.3",
        "macOS 12.6.4",
        "macOS 12.6.5",
        "macOS 12.6.6",
        "macOS 12.6.7",
        "macOS 12.6.8",
        "macOS 12.6.9",
        "macOS 12.7",
        "macOS 12.7.1",
        "macOS 12.7.2",
        "macOS 12.7.3",
        "macOS 12.7.4",
        "macOS 12.7.5",
        "macOS 12.7.6",
        "macOS 13.0",
        "macOS 13.0.1",
        "macOS 13.1",
        "macOS 13.2",
        "macOS 13.2.1",
        "macOS 13.3",
        "macOS 13.3.1",
        "macOS 13.4",
        "macOS 13.4.1",
        "macOS 13.5",
        "macOS 13.5.1",
        "macOS 13.5.2",
        "macOS 13.6",
        "macOS 13.6.1",
        "macOS 13.6.2",
        "macOS 13.6.3",
        "macOS 13.6.4",
        "macOS 13.6.5",
        "macOS 13.6.6",
        "macOS 13.6.7",
        "macOS 13.6.8",
        "macOS 13.6.9",
        "macOS 13.7",
        "macOS 13.7.1",
        "macOS 13.7.2",
        "macOS 13.7.3",
        "macOS 13.7.4",
        "macOS 14.0",
        "macOS 14.1",
        "macOS 14.1.1",
        "macOS 14.1.2",
        "macOS 14.2",
        "macOS 14.2.1",
        "macOS 14.3",
        "macOS 14.3.1",
        "macOS 14.4",
        "macOS 14.4.1",
        "macOS 14.5",
        "macOS 14.6",
        "macOS 14.6.1",
        "macOS 14.7",
        "macOS 14.7.1",
        "macOS 14.7.2",
        "macOS 14.7.3",
        "macOS 14.7.4",
        "macOS 15.0",
        "macOS 15.0.1",
        "macOS 15.1",
        "macOS 15.1.1",
        "macOS 15.2",
        "macOS 15.3",
        "macOS 15.3.1",
        "macOS 15.4",
        "macOS 15.5",
    ]

    deviceList: List[DeviceInfo] = []

    @classmethod
    def __gen__(cls: Type[macOSDevice]) -> None:

        if len(cls.deviceList) == 0:

            # https://github.com/desktop-app/lib_base/blob/master/base/platform/mac/base_info_mac.mm#L42

            def FromIdentifier(model: str):
                words = []
                word = ""

                for ch in model:
                    if not ch.isalpha():
                        continue
                    if ch.isupper():
                        if word != "":
                            words.append(word)
                            word = ""
                    word += ch

                if word != "":
                    words.append(word)
                result = ""
                for word in words:
                    if result != "" and word != "Mac" and word != "Book":
                        result += " "
                    result += word

                return result

            new_devices_models = []
            for model in cls.device_models:
                model = cls._CleanAndSimplify(FromIdentifier(model))
                if not model in new_devices_models:
                    new_devices_models.append(model)

            cls.device_models = new_devices_models

            results: List[DeviceInfo] = []

            for model in cls.device_models:
                for version in cls.system_versions:
                    results.append(DeviceInfo(model, version))

            cls.deviceList = results


class AndroidDevice(SystemInfo):
    device_models = [
        "Samsung SM-A515F",
        "Samsung SM-A515U",
        "Samsung SM-A515U1",
        "Samsung SM-A515W",
        "Samsung SM-S515DL",
        "Samsung SM-A715F",
        "Samsung SM-A715W",
        "Samsung SM-G980F",
        "Samsung SM-G9810",
        "Samsung SM-G981N",
        "Samsung SM-G981U",
        "Samsung SM-G981U1",
        "Samsung SM-G981V",
        "Samsung SM-G981W",
        "Samsung SM-G981B",
        "Samsung SM-G985F",
        "Samsung SM-G9860",
        "Samsung SM-G986N",
        "Samsung SM-G986U",
        "Samsung SM-G986U1",
        "Samsung SM-G986W",
        "Samsung SM-G986B",
        "Samsung SM-G9880",
        "Samsung SM-G988N",
        "Samsung SM-G988Q",
        "Samsung SM-G988U",
        "Samsung SM-G988U1",
        "Samsung SM-G988W",
        "Samsung SM-G988B",
        "Samsung SM-N980F",
        "Samsung SM-N9810",
        "Samsung SM-N981N",
        "Samsung SM-N981U",
        "Samsung SM-N981U1",
        "Samsung SM-N981W",
        "Samsung SM-N981B",
        "Samsung SM-N985F",
        "Samsung SM-N9860",
        "Samsung SM-N986N",
        "Samsung SM-N986U",
        "Samsung SM-N986U1",
        "Samsung SM-N986W",
        "Samsung SM-N986B",
        "Samsung SC-51B",
        "Samsung SCG09",
        "Samsung SM-G9910",
        "Samsung SM-G991U1",
        "Samsung SM-G991W",
        "Samsung SM-G991B",
        "Samsung SM-G991N",
        "Samsung SCG10",
        "Samsung SM-G9960",
        "Samsung SM-G996U1",
        "Samsung SM-G996W",
        "Samsung SM-G996B",
        "Samsung SM-G996N",
        "Samsung SC-52B",
        "Samsung SM-G9980",
        "Samsung SM-G998U",
        "Samsung SM-G998U1",
        "Samsung SM-G998W",
        "Samsung SM-G998B",
        "Samsung SM-G998N",
        "Samsung SM-A325F",
        "Samsung SM-A325M",
        "Samsung SCG08",
        "Samsung SM-A326B",
        "Samsung SM-A326BR",
        "Samsung SM-A326U",
        "Samsung SM-A326U1",
        "Samsung SM-A326W",
        "Samsung SM-S326DL",
        "Samsung SM-A326K",
        "Samsung SM-A4260",
        "Samsung SM-A426B",
        "Samsung SM-A426N",
        "Samsung SM-A426U",
        "Samsung SM-A426U1",
        "Samsung SM-A525F",
        "Samsung SM-A5260",
        "Samsung SM-A526B",
        "Samsung SM-A526N",
        "Samsung SM-A526U",
        "Samsung SM-A526U1",
        "Samsung SM-A526W",
        "Samsung SM-A725F",
        "Samsung SM-A725M",
        "Samsung SM-M127F",
        "Samsung SM-M127G",
        "Samsung SM-M127N",
        "Samsung SM-F127G",
        "Samsung SM-M426B",
        "Samsung SM-M515F",
        "Samsung SM-M625F",
        "Samsung SM-F415F",
        "Samsung SM-T870",
        "Samsung SM-T875",
        "Samsung SM-T875N",
        "Samsung SM-T878U",
        "Samsung SM-T970",
        "Samsung SM-T975",
        "Samsung SM-T975N",
        "Samsung SM-T976B",
        "Samsung SM-T976N",
        "Samsung SM-T978U",
        "Samsung SM-T730",
        "Samsung SM-T735",
        "Samsung SM-T735C",
        "Samsung SM-T735N",
        "Samsung SM-T736B",
        "Samsung SM-T736N",
        "Samsung SM-T737",
        "Samsung SM-T220",
        "Samsung SM-T225",
        "Samsung SM-T225C",
        "Samsung SM-T225N",
        "Samsung SM-T500",
        "Samsung SM-T505",
        "Samsung SM-T505C",
        "Samsung SM-T505N",
        "Samsung SM-T507",
        "Samsung SC-03L",
        "Samsung SCV41",
        "Samsung SM-G970F",
        "Samsung SM-G970N",
        "Samsung SM-G9700",
        "Samsung SM-G9708",
        "Samsung SM-G970U",
        "Samsung SM-G970U1",
        "Samsung SM-G970W",
        "Samsung SM-G973F",
        "Samsung SM-G973N",
        "Samsung SM-G9730",
        "Samsung SM-G9738",
        "Samsung SM-G973C",
        "Samsung SM-G973U",
        "Samsung SM-G973U1",
        "Samsung SM-G973W",
        "Samsung SC-04L",
        "Samsung SCV42",
        "Samsung SM-G975F",
        "Samsung SM-G975N",
        "Samsung SM-G9750",
        "Samsung SM-G9758",
        "Samsung SM-G975U",
        "Samsung SM-G975U1",
        "Samsung SM-G975W",
        "Samsung SM-G977B",
        "Samsung SM-G977N",
        "Samsung SM-G977P",
        "Samsung SM-G977T",
        "Samsung SM-G977U",
        "Samsung SM-N970F",
        "Samsung SM-N9700",
        "Samsung SM-N970U",
        "Samsung SM-N970U1",
        "Samsung SM-N970W",
        "Samsung SM-N971N",
        "Samsung SC-01M",
        "Samsung SCV45",
        "Samsung SM-N9750",
        "Samsung SM-N975C",
        "Samsung SM-N975U",
        "Samsung SM-N975U1",
        "Samsung SM-N975W",
        "Samsung SM-N975F",
        "Samsung SM-N976B",
        "Samsung SM-N976N",
        "Samsung SM-N9760",
        "Samsung SM-N976Q",
        "Samsung SM-N976V",
        "Samsung SM-N976U",
        "Samsung SM-A015A",
        "Samsung SM-A015AZ",
        "Samsung SM-A015F",
        "Samsung SM-A015G",
        "Samsung SM-A015M",
        "Samsung SM-A015T1",
        "Samsung SM-A015U",
        "Samsung SM-A015U1",
        "Samsung SM-A015V",
        "Samsung SM-S111DL",
        "Samsung SM-A025A",
        "Samsung SM-A025AZ",
        "Samsung SM-A025F",
        "Samsung SM-A025G",
        "Samsung SM-A025M",
        "Samsung SM-A025U",
        "Samsung SM-A025U1",
        "Samsung SM-A025V",
        "Samsung SM-A115A",
        "Samsung SM-A115AP",
        "Samsung SM-A115AZ",
        "Samsung SM-A115F",
        "Samsung SM-A115M",
        "Samsung SM-A115U",
        "Samsung SM-A115U1",
        "Samsung SM-A115W",
        "Samsung SM-A125F",
        "Samsung SM-A125M",
        "Samsung SM-A125N",
        "Samsung SM-A125U",
        "Samsung SM-A125U1",
        "Samsung SM-S127DL",
        "Samsung SM-A217F",
        "Samsung SM-A217M",
        "Samsung SM-A217N",
        "Samsung SM-A315F",
        "Samsung SM-A315G",
        "Samsung SM-A315N",
        "Samsung SC-41A",
        "Samsung SCV48",
        "Samsung SM-A415F",
        "Samsung SCV44",
        "Samsung SM-F9000",
        "Samsung SM-F900F",
        "Samsung SM-F900U",
        "Samsung SM-F900U1",
        "Samsung SM-F900W",
        "Samsung SCV47",
        "Samsung SM-F7000",
        "Samsung SM-F700F",
        "Samsung SM-F700N",
        "Samsung SM-F700U",
        "Samsung SM-F700U1",
        "Samsung SM-F700W",
        "Samsung SCG04",
        "Samsung SM-F9160",
        "Samsung SM-F916B",
        "Samsung SM-F916N",
        "Samsung SM-F916Q",
        "Samsung SM-F916U",
        "Samsung SM-F916U1",
        "Samsung SM-F916W",
        "Samsung SM-T860",
        "Samsung SM-T865",
        "Samsung SM-T865N",
        "Samsung SM-T866N",
        "Samsung SM-T867",
        "Samsung SM-T867R4",
        "Samsung SM-T867U",
        "Samsung SM-T867V",
        "Samsung SM-P610",
        "Samsung SM-P615",
        "Samsung SM-P615C",
        "Samsung SM-P615N",
        "Samsung SM-P617",
        "Samsung SM-T510",
        "Samsung SM-T515",
        "Samsung SM-T515N",
        "Samsung SM-T517",
        "Samsung SM-T517P",
        "Samsung SM-T307U",
        "Samsung SM-T570",
        "Samsung SM-T575",
        "Samsung SM-T575N",
        "Samsung SM-T577",
        "Samsung SM-T577U",
        # Android 14 & 15
        "Google Pixel 6",
        "Google Pixel 6 Pro",
        "Google Pixel 6a",
        "Google Pixel 7",
        "Google Pixel 7 Pro",
        "Google Pixel 7a",
        "Google Pixel 8",
        "Google Pixel 8 Pro",
        "Google Pixel 8a",
        "Google Pixel 9",
        "Google Pixel 9 Pro",
        "Google Pixel 9 Pro XL",
        "Google Pixel 9 Pro Fold",
        "Google Pixel Fold",
        "Google Pixel Tablet",
        "Samsung Galaxy S24",
        "Samsung Galaxy S24+",
        "Samsung Galaxy S24 Ultra",
        "Samsung Galaxy S24 FE",
        "Samsung Galaxy S23",
        "Samsung Galaxy S23+",
        "Samsung Galaxy S23 Ultra",
        "Samsung Galaxy S23 FE",
        "Samsung Galaxy S22",
        "Samsung Galaxy S22+",
        "Samsung Galaxy S22 Ultra",
        "Samsung Galaxy S21",
        "Samsung Galaxy S21+",
        "Samsung Galaxy S21 Ultra",
        "Samsung Galaxy S21 FE",
        "Samsung Galaxy Z Fold6",
        "Samsung Galaxy Z Flip6",
        "Samsung Galaxy Z Fold5",
        "Samsung Galaxy Z Flip5",
        "Samsung Galaxy Z Fold4",
        "Samsung Galaxy Z Flip4",
        "Samsung Galaxy Z Fold3",
        "Samsung Galaxy Z Flip3",
        "Samsung Galaxy A15",
        "Samsung Galaxy A16",
        "Samsung Galaxy A25",
        "Samsung Galaxy A34",
        "Samsung Galaxy A35",
        "Samsung Galaxy A54",
        "Samsung Galaxy A55",
        "Samsung Galaxy A73",
        "Samsung Galaxy F15",
        "Samsung Galaxy F34",
        "Samsung Galaxy F54",
        "Samsung Galaxy F55",
        "Samsung Galaxy M15",
        "Samsung Galaxy M34",
        "Samsung Galaxy M54",
        "Samsung Galaxy M55",
        "Samsung Galaxy Tab S9",
        "Samsung Galaxy Tab S9+",
        "Samsung Galaxy Tab S9 Ultra",
        "Samsung Galaxy Tab S9 FE",
        "Samsung Galaxy Tab S9 FE+",
        "Samsung Galaxy Tab S8",
        "Samsung Galaxy Tab S8+",
        "Samsung Galaxy Tab S8 Ultra",
        "Xiaomi 15",
        "Xiaomi 14",
        "Xiaomi 14T Pro",
        "Xiaomi 13",
        "Xiaomi 13T",
        "Xiaomi 12",
        "Xiaomi 12T",
        "Xiaomi Civi 1S",
        "Xiaomi Civi 2",
        "Xiaomi Civi 3",
        "Xiaomi Civi 4 Pro",
        "Xiaomi Pad 6",
        "Xiaomi Pad 6 Pro",
        "Xiaomi Pad 6 Max 14",
        "Xiaomi Pad 6S Pro 12.4",
        "Xiaomi Pad 5 Pro 12.4",
        "Redmi Note 13",
        "Redmi Note 13 5G",
        "Redmi Note 13 Pro",
        "Redmi Note 13 Pro 5G",
        "Redmi Note 13 Pro Plus 5G",
        "Redmi Note 13R",
        "Redmi Note 13R Pro",
        "Redmi Note 12",
        "Redmi Note 12 4G",
        "Redmi Note 12 Turbo",
        "Redmi Note 12 Pro 4G",
        "Redmi Note 12 Pro Speed",
        "Redmi Note 12R",
        "Redmi Note 12R Pro",
        "Redmi Note 12T Pro",
        "Redmi Note 12S",
        "Redmi K70",
        "Redmi K70E",
        "Redmi K70 Pro",
        "Redmi K70 Ultra",
        "Redmi K60",
        "Redmi K60 Pro",
        "Redmi K60 Ultra",
        "Redmi 14C",
        "Redmi 13",
        "Redmi 13R",
        "Redmi 13 5G",
        "Redmi 13C 5G",
        "Redmi Pad Pro",
        "OnePlus 13",
        "OnePlus 13R",
        "OnePlus 12",
        "OnePlus 12R",
        "OnePlus 11",
        "OnePlus 11R",
        "OnePlus 10 Pro",
        "OnePlus 10T",
        "OnePlus 10R",
        "OnePlus Open",
        "OnePlus Nord 3",
        "OnePlus Nord 4",
        "OnePlus Nord CE3",
        "OnePlus Nord CE3 Lite",
        "OnePlus Nord CE4",
        "OnePlus Nord CE4 Lite",
        "OnePlus Pad",
        "OnePlus Pad 2",
        "Sony Xperia 1 VI",
        "Sony Xperia 1 V",
        "Sony Xperia 5 V",
        "Sony Xperia 10 VI",
        "Sony Xperia 10 V",
        "Asus ROG Phone 8",
        "Asus ROG Phone 8 Pro",
        "Asus ROG Phone 7",
        "Motorola Razr+ (2024)",
        "Motorola Razr 50 Ultra",
        "Motorola Razr (2024)",
        "Motorola Razr 50",
        "Motorola Razr 50s",
        "Motorola Razr+ (2023)",
        "Motorola Razr 40 Ultra",
        "Motorola Razr (2023)",
        "Motorola Razr 40",
        "Motorola Razr 40s",
        "Motorola Edge (2024)",
        "Motorola Edge (2023)",
        "Motorola Edge+ (2023)",
        "Motorola Edge 50 Ultra",
        "Motorola Edge 50 Pro",
        "Motorola Edge 50 Neo",
        "Motorola Edge 50 Fusion",
        "Motorola Edge 50",
        "Motorola Edge 40",
        "Motorola Edge 40 Neo",
        "Motorola Edge 40 Pro",
        "Motorola Edge 30 Ultra",
        "Motorola Moto G Power 5G (2024)",
        "Motorola Moto G Stylus 5G (2024)",
        "Motorola Moto G 5G (2024)",
        "Motorola Moto G85",
        "Motorola Moto G75",
        "Motorola Moto G55",
        "Motorola Moto G45",
        "Motorola Moto G35",
        "Motorola Moto G34 5G",
        "Motorola ThinkPhone",
        "Realme C55",
        "Realme GT series",
    ]

    system_versions = [
        "SDK 31",  # Android 12 (2021)
        "SDK 32",  # Android 12L (2021)
        "SDK 33",  # Android 13 Tiramisu (2022)
        "SDK 34",  # Android 14 Upside Down Cake (2023)
        "SDK 35",  # Android 15 Vanilla Ice Cream (2024)
        # "SDK 36",  # Android 16 Baklava (2025)
    ]

    deviceList: List[DeviceInfo] = []

    @classmethod
    def __gen__(cls: Type[AndroidDevice]) -> None:

        if len(cls.deviceList) == 0:

            results: List[DeviceInfo] = []

            for model in cls.device_models:
                for version in cls.system_versions:
                    results.append(DeviceInfo(model, version))

            cls.deviceList = results


class iOSDeivce(SystemInfo):
    device_models = {
        11: ["", " Pro", " Pro Max"],
        12: [" mini", "", " Pro", " Pro Max"],
        13: [" Pro", " Pro Max", " Mini", ""],
        14: [" Pro", " Pro Max", " Plus", ""],
        15: [" Pro", " Pro Max", " Plus", ""],
        16: [" Pro", " Pro Max", " Plus", "e", ""],
    }

    system_versions: Dict[int, Dict[int, List[int]]] = {
        # Версии обновлены 05.08.2025

        # iOS 26 (сентябрь 2025 - планируемый релиз) пока исключаем
        # Новая система нумерации на основе года
        # 26: {
        #     0: [],  # iOS 26.0 (планируется к релизу в сентябре 2025)
        # },

        # iOS 18 (сентябрь 2024 - текущая актуальная версия)
        18: {
            6: [],  # iOS 18.6 (июль 2025) - текущая версия
            5: [],  # iOS 18.5 (май 2025)
            4: [1],  # iOS 18.4.1 (апрель 2025)
            3: [2, 1],  # iOS 18.3.1, 18.3.2 (февраль-март 2025)
            2: [1],  # iOS 18.2.1 (январь 2025)
            1: [1],  # iOS 18.1.1 (ноябрь 2024)
            0: [1],  # iOS 18.0.1 (октябрь 2024)
        },

        # iOS 17 (сентябрь 2023)
        17: {
            7: [2],  # iOS 17.7.2 (ноябрь 2024)
            6: [1],  # iOS 17.6.1 (август 2024)
            5: [],  # iOS 17.5 (май 2024)
            4: [1],  # iOS 17.4.1 (март 2024)
            3: [1],  # iOS 17.3.1 (февраль 2024)
            2: [1],  # iOS 17.2.1 (декабрь 2023)
            1: [2, 1],  # iOS 17.1.1, 17.1.2 (октябрь-ноябрь 2023)
            0: [3, 2, 1],  # iOS 17.0.1, 17.0.2, 17.0.3 (сентябрь-октябрь 2023)
        },

        # iOS 16 (сентябрь 2022)
        16: {
            7: [11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1],  # iOS 16.7.1 - 16.7.11 (сентябрь 2023 - март 2025)
            6: [1],  # iOS 16.6.1 (сентябрь 2023)
            5: [1],  # iOS 16.5.1 (май 2023)
            4: [1],  # iOS 16.4.1 (апрель 2023) + RSR патч
            3: [1],  # iOS 16.3.1 (февраль 2023)
            2: [],  # iOS 16.2 (декабрь 2022)
            1: [2, 1],  # iOS 16.1.1, 16.1.2 (октябрь-ноябрь 2022)
            0: [3, 2, 1],  # iOS 16.0.1, 16.0.2, 16.0.3 (сентябрь-октябрь 2022)
        },
        15: {
            8: [4, 3, 2, 1],  # iOS 15.8.1 - 15.8.4 (включая март 2025)
            7: [9, 8, 7, 6, 5, 4, 3, 2, 1],  # iOS 15.7.1 - 15.7.9
            6: [1],  # iOS 15.6.1
            5: [],  # iOS 15.5
            4: [1],  # iOS 15.4.1
            3: [1],  # iOS 15.3.1
            2: [],  # iOS 15.2
            1: [1],  # iOS 15.1.1
            0: [2, 1],  # iOS 15.0.1, 15.0.2
        },
    }

    deviceList: List[DeviceInfo] = []

    @classmethod
    def __gen__(cls: Type[iOSDeivce]) -> None:

        if len(cls.deviceList) == 0:
            results: List[DeviceInfo] = []

            # ! SHITTY CODE BECAUSE I HAD TO CHECK FOR THE RIGHT VERSION
            # Проверяем версию iPhone и выдаем версию iOS
            for id_model in cls.device_models:
                if id_model in [11, 12, 13, 14, 15, 16]:
                    available_versions = [15, 16, 17, 18]
                else:
                    available_versions = [16, 17, 18]

                for model_name in cls.device_models[id_model]:

                    device_model = f"iPhone {id_model}{model_name}"

                    for major in available_versions:
                        for minor, patches in cls.system_versions[major].items():

                            if len(patches) == 0:
                                results.append(
                                    DeviceInfo(device_model, f"{major}.{minor}")
                                )
                            else:
                                for patch in patches:
                                    results.append(
                                        DeviceInfo(
                                            device_model, f"{major}.{minor}.{patch}"
                                        )
                                    )

            cls.deviceList = results
