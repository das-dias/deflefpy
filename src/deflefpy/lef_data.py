"""_summary_: lef_data.py
Data structures for LEF / TLEF files.
Author : das-dias
Email  : das.dias6@gmail.com
Github : /das-dias
Date   : 2022-04-08
"""
import numpy as np
from enum import Enum  # import enum to create enumerations
from importlib.metadata import PathDistribution
from pickletools import uint8
from deflefpy.util import *


class LefCoverClass(Enum):
    """_summary_
    Types of LEF COVER statement values.
    Args:
        None
        BUMP    : Bump cover.
    """

    None
    BUMP = 1


class LefBlockClass(Enum):
    """_summary_
    Types of LEF BLOCK statement values.
    Args:
        BLACKBOX    : Blackbox block.
        SOFT        : Soft block.
    """

    None
    BLACKBOX = 1
    SOFT = 2


class LefPadClass(Enum):
    """_summary_
    Types of LEF PAD statement values.
    Args:
        INPUT       : Input pad.
        OUTPUT      : Output pad.
        INOUT       : Inout pad.
        POWER       : Power pad.
        SPACER      : Spacer pad.
        AREAIO      : Area I/O pad.
    """

    None
    INPUT = 1
    OUTPUT = 2
    INOUT = 3
    POWER = 4
    SPACER = 5
    AREAIO = 6


class LefCoreClass(Enum):
    """_summary_
    Types of LEF CORE statement values.
    Args:
        FEEDTHRU    : Feedthru core.
        TIEHIGH     : Tiehigh core.
        TIELOW      : Tielow core.
        SPACER      : Spacer core.
        ANTENNACELL : Antenna cell core.
        WELLTAP     : Welltap core.
    """

    None
    FEEDTHRU = 1
    TIEHIGH = 2
    TIELOW = 3
    SPACER = 4
    ANTENNACELL = 5
    WELLTAP = 6


class LefEndcapClass(Enum):
    """_summary_
    Types of LEF ENDCAP statement values.
    Args:
        PRE         : Pre Endcap.
        POST        : Post Endcap.
        TOPLEFT     : Top left Endcap.
        TOPRIGHT    : Top right Endcap.
        BOTTOMLEFT  : Bottom left Endcap.
        BOTTOMRIGHT : Bottom right Endcap.
    """

    PRE = 1
    POST = 2
    TOPLEFT = 3
    TOPRIGHT = 4
    BOTTOMLEFT = 5
    BOTTOMRIGHT = 6


class LefClassType(Enum):
    """_summary_
    Possible statement values for CLASS LEF statement.
    Args:
        COVER       : Cover class.
        RING        : Ring class.
        BLOCK       : Block class.
        PAD         : Pad class.
        CORE        : Core class.
        ENDCAP      : Endcap class.
    """

    COVER = LefCoverClass
    RING = 1
    BLOCK = LefBlockClass
    PAD = LefPadClass
    CORE = LefCoreClass
    ENDCAP = LefEndcapClass


class LefSymmetry(Enum):
    """_summary_
    Possible values for the SYMMETRY LEF statement.
    Args:
        X   :  Symmetry along the x axis
        Y   :  Symmetry along the y axis
        R90 : Symmetry along the 90 degree rotation
    """

    X = 1
    Y = 2
    R90 = 3


class LefOrient(Enum):
    """_summary_
    Possible values for the ORIENTATION LEF statement.
    Args:
        N   :  Orientation along the North of the cell
        W   :  Orientation along the West of the cell (+90 deg rotation)
        S   :  Orientation along the South of the cell (180deg rotation)
        E   :  Orientation along the East of the cell (-90 deg rotation)
        FN  :  Foreign Orientation along the North of the cell (90 deg rotation)
        FS  :  Foreign Orientation along the South of the cell (270 deg rotation)
        FE  :  Foreign Orientation along the East of the cell (180 deg rotation)
        FW  :  Foreign Orientation along the West of the cell (270 deg rotation)
    """

    N = 1
    W = 2
    S = 3
    E = 4
    FN = 5
    FS = 6
    FE = 7
    FW = 8


class LefInOut(Enum):
    """_summary_
    Possible values for the INOUT LEF statement.
    Args:
        None    : regular Input/Output
        TRISTATE: Tristate Input/Output
    """

    None
    TRISTATE = 1


class LefDirection(Enum):
    """_summary_
    Possible values for the DIRECTION LEF statement.
    Args:
        INPUT   : Input direction
        OUTPUT  : Output direction
        INOUT   : Inout direction
        FEEDTHRU: Feedthru direction

    """

    INPUT = LefInOut
    OUTPUT = LefInOut
    INOUT = 1
    FEEDTHRU = 2


class LefUse(Enum):
    """_summary_
    Possible values for the USE LEF statement.
    Args:
        SIGNAL  : Signal use
        ANALOG  : Analog use
        POWER   : Power use
        GROUND  : Ground
        CLOCK   : Clock use of the pin
    """

    SIGNAL = 1
    ANALOG = 2
    POWER = 3
    GROUND = 4
    CLOCK = 5


class LefShape(Enum):
    """_summary_
    Possible values for the SHAPE LEF statement.
    Args:
        ABUTMENT : Abutment shape
        RING     : Ring shape
        FEEDTHRU : Feedthru shape
    """

    ABUTMENT = 1
    RING = 2
    FEEDTHRU = 3


class LefForeign(LefStatement):
    """_summary_
    A LEF FOREIGN statement.
    Args:
        object (_type_): LefForeign class object
    """

    def __init__(
        self,
        foreignCellName: str,
        offset: LefPoint = LefPoint(0, 0),
        orient: LefOrient = LefOrient.N,
    ):
        """_summary_
        The class object constructor.
        Args:
            foreignCellName (str): str representation of the name of the foreign cell.
            offset (LefPoint)       : offset of the foreign cell.
            orient (LefOrient)      : orientation of the foreign cell.
        """
        self.foreignCellName = foreignCellName
        self.offset = offset
        self.orient = orient

    def __str__(self):
        """_summary_
        The class object str description.
        Args:
            object (LefForeign): statement object
        """
        return f"LefForeign: {self.type.name} {self.name} {self.foreignCellName} {self.offset} {self.orient}"


class LefSize(LefStatement):
    """_summary_
    A LEF SIZE statement object.
    Args:
        LefStatement (_type_): _description_

    Raises:
        TypeError: _description_

    Returns:
        _type_: _description_
    """

    def __init__(self, width: LefDecimal, height: LefDecimal):
        self.height = height
        self.width = width

    def __str__(self):
        """_summary_
        A str representation of the object.
        Args:
            object (LefSize): LefSize object
        """
        return f"SIZE {self.width} BY {self.height}"


class LefSitePattern(LefStatement):
    """_summary_

    Args:
        Enum (_type_): _description_

    Raises:
        TypeError: _description_

    Returns:
        _type_: _description_
    """

    def __init__(
        self,
        xOrigin: LefDecimal,
        yOrigin: LefDecimal,
        siteOrient: LefOrient,
        stepPattern: LefStepPattern = None,
    ):
        self.origin = LefPoint(xOrigin, yOrigin)
        self.siteOrient = siteOrient
        self.stepPattern = stepPattern

    def __str__(self):
        """_summary_
        A str representation of the object.
        Args:
            object (LefSitePattern): LefSitePattern object
        """
        return f"{self.origin} {self.siteOrient.name} {self.stepPattern}"


class LefRowpattern(LefStatement):
    """_summary_

    Args:
        LefStatement (_type_): _description_

    Raises:
        TypeError: _description_

    Returns:
        _type_: _description_
    """

    def __init__(
        self,
        prevSiteName: str,
        prevSiteOrient: LefOrient,
    ):
        self.prevSiteName = prevSiteName
        self.prevSiteOrient = prevSiteOrient

    def __str__(self):
        return f"ROWPATTERN {self.prevSiteName} {self.prevSiteOrient.name}"


class LefSite(LefStatement):
    """_summary_
    A LEF SITE statement.
    Args:
        LefStatement (_type_): _description_
    Raises:
        TypeError: _description_
    Returns:
        _type_: _description_
    """

    def __init__(
        self,
        name: str,
        type: LefStatementType,
    ):
        """_summary_
        The class object constructor.
        Args:
            name (str): str representation of the name of the site.
            type (LefStatementType): type of the site.
        """
        self.name = name
        if type != LefStatementType.SITE:
            raise TypeError("LefSite: type must be SITE")
        self.type = type
        self.siteClass = None
        self.symmetry = []  # simmetry list
        self.rowpattern = []  # row pattern list
        self.size = None
        self.sitePattern = None

    def parse_data(self, data):
        """_summary_

        Args:
            data (_type_): _description_

        Raises:
            TypeError: _description_

        Returns:
            _type_: _description_
        """
        statement = data[0]
        value = data[1]
        if statement == "CLASS":
            if type(value) != LefClassType:
                raise TypeError("LefSite: CLASS needs to be LefClassType object")
            self.siteClass = value  # value will be a LefClassType object
        elif statement == "SYMMETRY":
            if type(value) != LefSymmetry:
                raise TypeError("LefSite: SYMMETRY needs to be LefSymmetry object")
            self.symmetry.append(value)
        elif statement == "ROWPATTERN":
            if type(value) != LefRowpattern:
                raise TypeError("LefSite: ROWPATTERN needs to be LefRowpattern object")
            self.rowpattern.append(value)
        elif statement == "SIZE":
            if type(value) != LefSize:
                raise TypeError("LefSite: SIZE needs to be LefSize object")
            self.size = value
        else:
            raise TypeError(f"LefSite: {statement} is not a valid statement")


class LefProperty(LefStatement):
    """_summary_
    A LEF PROPERTY statement data structure
    """

    def __init__(self, name: str, value):
        """_summary_
        The class object constructor.
        Args:
            name (str)               : property name
            value (str/LefDecimal)   : property value
        Raises:
            TypeError
        """
        self.name = name
        if type(value) != str or type(value) != LefDecimal:
            raise TypeError("LefProperty: value must be str or LefDecimal")
        self.value = value

    def __str__(self):
        return f"PROPERTY {self.name} {self.value}"


class LefPin(LefStatement):
    """_summary_
    A LEF PIN statement data structure.
    Args:
        LefStatement (_type_): _description_

    Returns:
        _type_: _description_
    """

    def __init__(self, name: str):
        """_summary_
        The class object constructor.
        Args:
            name (str): str representation of the name of the pin.
            type (LefStatementType): type of the pin.
        """
        self.name = name
        self.type = LefStatementType.PIN
        self.taperRule = ""
        self.direction = None
        self.use = None
        self.netExpr = ""
        self.supplySensitivity = ""
        self.groundSensitivity = ""
        self.shape = None
        self.mustJoin = ""
        self.port = []
        self.property = {}
        self.propertyLef58ViaInPinOnly = ""

        # antenna fields
        self.antennaPartialMetalArea = []
        self.antennaPartialMetalSideArea = []
        self.antennaPartialCutArea = []
        self.antennaDiffArea = []
        self.antennaModel = []
        self.antennaGateArea = []
        self.antennaMaxAreaCar = []
        self.antennaMaxSideAreaCar = []
        self.antennaMaxCutCar = []

    def __str__(self):
        """_summary_
        str representation of LEF PIN macro statement.
        Returns:
            ret (str): str representation
        """
        ret = f"PIN {self.name}"
        if self.taperRule != "":
            ret += "\tTAPERRULE {} ;\n".format(self.taperRule)
        if self.direction != None:
            ret += "\tDIRECTION {} ;\n".format(self.direction.name)
        if self.use != None:
            ret += "\tUSE {} ;\n".format(self.use.name)
        if self.netExpr != "":
            ret += "\tNETEXPR {} ;\n".format(self.netExpr)
        if self.supplySensitivity != "":
            ret += "\tSUPPLYSENSITIVITY {} ;\n".format(self.supplySensitivity)
        if self.groundSensitivity != "":
            ret += "\tGROUNDSENSITIVITY {} ;\n".format(self.groundSensitivity)
        if self.shape != None:
            ret += "\tSHAPE {} ;\n".format(self.shape.name)
        if self.mustJoin != "":
            ret += "\tMUSTJOIN {} ;\n".format(self.mustJoin)
        for p in self.port:
            ret += "\t{} ;\n".format(str(p))
        for prop in self.property.values():
            ret += "\t{} ;\n".format(str(prop))
        if self.propertyLef58ViaInPinOnly != "":
            ret += "\tPROPERTY Lef58ViaInPinOnly {} ;\n".format(
                self.propertyLef58ViaInPinOnly
            )
        for a in self.antennaPartialMetalArea:
            ret += "\t{} ;\n".format(str(a))
        for a in self.antennaPartialMetalSideArea:
            ret += "\t{} ;\n".format(str(a))
        for a in self.antennaPartialCutArea:
            ret += "\t{} ;\n".format(str(a))
        for a in self.antennaDiffArea:
            ret += "\t{} ;\n".format(str(a))
        for a in self.antennaModel:
            ret += "\t{} ;\n".format(str(a))
        for a in self.antennaGateArea:
            ret += "\t{} ;\n".format(str(a))
        for a in self.antennaMaxAreaCar:
            ret += "\t{} ;\n".format(str(a))
        for a in self.antennaMaxSideAreaCar:
            ret += "\t{} ;\n".format(str(a))
        for a in self.antennaMaxCutCar:
            ret += "\t{} ;\n".format(str(a))
        ret += "END {}\n".format(self.name)
        return ret

    def parse_data(self, data):
        """_summary_
        Parses data into the PIN LEF data structure in order to build its constituent fields.
        Args:
            data (Tuple): (statement: str, value: Generic Type)
        Raises:
            TypeError: Unknown statement
        Returns:
            None
        """
        statement = data[0]
        value = data[1]
        if statement == "TAPERRULE":
            if type(value) != str:
                raise TypeError("LefPin: TAPERRULE must be a str")
            self.taperRule = value
        elif statement == "DIRECTION":
            if type(value) != LefDirection:
                raise TypeError("LefPin: DIRECTION must be LefDirection")
            self.direction = value
        elif statement == "USE":
            if type(value) != LefUse:
                raise TypeError("LefPin: USE must be a LefUse statement")
            self.use = value
        elif statement == "NETEXPR":
            if type(value) != str:
                raise TypeError("LefPin: NETEXPR value must be a str")
            self.netExpr = value
        elif statement == "SUPPLYSENSITIVITY":
            if type(value) != str:
                raise TypeError(
                    "LefPin: SUPPLYSENSITIVITY value must be a str with the Supply Pin Name"
                )
            self.supplySensitivity = value
        elif statement == "GROUNDSENSITIVITY":
            if type(value) != str:
                raise TypeError(
                    "LefPin: GROUNDSENSITIVITY value must be a str with the Ground Pin Name"
                )
            self.groundSensitivity = value
        elif statement == "SHAPE":
            if type(value) != LefShape:
                raise TypeError("LefPin: SHAPE value must be a LefShape statement")
            self.shape = value
        elif statement == "MUSTJOIN":
            if type(value) != str:
                raise TypeError(
                    "LefPin: MUSTJOIN value must be a str with the Pin Name"
                )
            self.mustJoin = value
        elif statement == "PORT":
            if type(value) != LefPort:
                raise TypeError("LefPin: PORT value must be a LefPort statement")
            self.port.append(value)
        elif statement == "PROPERTY":
            if type(value) != LefProperty:
                raise TypeError(
                    "LefPin: PROPERTY value must be a LefProperty statement"
                )
            self.property[value.name] = value
        elif statement == "PROPERTY_LEF58_VIAINPINONLY":
            if type(value) != str:
                raise TypeError(
                    "LefPin: PROPERTY_LEF58_VIAINPINONLY value must be a str with the Pin Name"
                )
            self.propertyLef58ViaInPinOnly = value

        elif statement == "ANTENNAPARTIALMETALAREA":
            if type(value) != LefAntennaField:
                raise TypeError(
                    "LefPin: ANTENNAPARTIALMETALAREA value must be a LefAntennaField statement"
                )
            if value.model != LefAntennaFieldType.ANTENNAPARTIALMETALAREA:
                raise TypeError(
                    "LefPin: ANTENNAPARTIALMETALAREA statement value must be of type ANTENNAPARTIALMETALAREA"
                )
            self.antennaPartialMetalArea.append(value)
        elif statement == "ANTENNAPARTIALMETALSIDEAREA":
            if type(value) != LefAntennaField:
                raise TypeError(
                    "LefPin: ANTENNAPARTIALMETALSIDEAREA value must be a LefAntennaField statement"
                )
            if value.model != LefAntennaFieldType.ANTENNAPARTIALMETALSIDEAREA:
                raise TypeError(
                    "LefPin: ANTENNAPARTIALMETALSIDEAREA statement value must be of type ANTENNAPARTIALMETALSIDEAREA"
                )
            self.antennaPartialMetalSideArea.append(value)
        elif statement == "ANTENNAPARTIALCUTAREA":
            if type(value) != LefAntennaField:
                raise TypeError(
                    "LefPin: ANTENNAPARTIALCUTAREA value must be a LefAntennaField statement"
                )
            if value.model != LefAntennaFieldType.ANTENNAPARTIALCUTAREA:
                raise TypeError(
                    "LefPin: ANTENNAPARTIALCUTAREA statement value must be of type ANTENNAPARTIALCUTAREA"
                )
            self.antennaPartialCutArea.append(value)
        elif statement == "ANTENNADIFFAREA":
            if type(value) != LefAntennaField:
                raise TypeError(
                    "LefPin: ANTENNADIFFAREA value must be a LefAntennaField statement"
                )
            if value.model != LefAntennaFieldType.ANTENNADIFFAREA:
                raise TypeError(
                    "LefPin: ANTENNADIFFAREA statement value must be of type ANTENNADIFFAREA"
                )
            self.antennaDiffArea.append(value)
        elif statement == "ANTENNAMODEL":
            if type(value) != LefAntennaField:
                raise TypeError(
                    "LefPin: ANTENNAMODEL value must be a LefAntennaField statement"
                )
            if value.model != LefAntennaFieldType.ANTENNAMODEL:
                raise TypeError(
                    "LefPin: ANTENNAMODEL statement value must be of type ANTENNAMODEL"
                )
            self.antennaModel.append(value)
        elif statement == "ANTENNAGATEAREA":
            if type(value) != LefAntennaField:
                raise TypeError(
                    "LefPin: ANTENNAGATEAREA value must be a LefAntennaField statement"
                )
            if value.model != LefAntennaFieldType.ANTENNAGATEAREA:
                raise TypeError(
                    "LefPin: ANTENNAGATEAREA statement value must be of type ANTENNAGATEAREA"
                )
            self.antennaGateArea.append(value)
        elif statement == "ANTENNAMAXAREACAR":
            if type(value) != LefAntennaField:
                raise TypeError(
                    "LefPin: ANTENNAMAXAREACAR value must be a LefAntennaField statement"
                )
            if value.model != LefAntennaFieldType.ANTENNAMAXAREACAR:
                raise TypeError(
                    "LefPin: ANTENNAMAXAREACAR statement value must be of type ANTENNAMAXAREACAR"
                )
            self.antennaMaxAreaCar.append(value)
        elif statement == "ANTENNAMAXSIDEAREACAR":
            if type(value) != LefAntennaField:
                raise TypeError(
                    "LefPin: ANTENNAMAXSIDEAREACAR value must be a LefAntennaField statement"
                )
            if value.model != LefAntennaFieldType.ANTENNAMAXSIDEAREACAR:
                raise TypeError(
                    "LefPin: ANTENNAMAXSIDEAREACAR statement value must be of type ANTENNAMAXSIDEAREACAR"
                )
            self.antennaMaxSideAreaCar.append(value)
        elif statement == "ANTENNAMAXCUTCAR":
            if type(value) != LefAntennaField:
                raise TypeError(
                    "LefPin: ANTENNAMAXCUTCAR value must be a LefAntennaField statement"
                )
            if value.model != LefAntennaFieldType.ANTENNAMAXCUTCAR:
                raise TypeError(
                    "LefPin: ANTENNAMAXCUTCAR statement value must be of type ANTENNAMAXCUTCAR"
                )
            self.antennaMaxCutCar.append(value)
        else:
            raise TypeError(f"LefPin: Unknown statement: {statement}")


class LefObs(LefStatement):
    """_summary_
    A LEF Obstruction Statement data structure.
    Args:
        LefStatement (_type_): _description_
    """

    def __init__(self):
        """
        The class constructor.
        Args:
            self (LefObs): the object pointer.
        """
        self.name = None
        self.type = LefClassType.OBS
        self.layerGeometries = []  # layer geometries statements

    def __str__(self):
        """
        The str representation of the class.
        Args:
            self (LefObs): the object pointer.
        Returns:
            str: the str representation of the class.
        """
        ret = "OBS\n"
        # Build the obs statement
        for lg in self.layerGeometries.values():
            ret += "\t{} \n".format(str(lg))
        ret += "END"
        return ret

    def parse_geometry(self, geometry):
        """
        Parse the geometry statement.
        Args:
            self (LefObs): the object pointer.
            geometry (str): the geometry statement.
        Returns:
            LefLayerGeometry: the parsed geometry statement.
        """
        # Check if the geometry is a LefLayerGeometry
        if type(geometry) != LefLayerGeometry:
            raise TypeError("LefObs: geometry must be a LefLayerGeometry statement")
        self.layerGeometries.append(geometry)


class LefMacro(LefStatement):
    """_summary_
    Macro class of the Lef file.
    Args:
        object (LefMacro)       : LefMacro class object
        type (LefStatementType) : type of the statement (MACRO in this case)
        name (str)           : name of the macro
    """

    def __init__(self, type, name):
        if type != LefStatementType.MACRO:
            raise TypeError("LefMacro: type must be MACRO")
        self.type = type
        self.name = name
        self.macroClass = None  # class of the macro
        self.fixedMask = False  # fixed mask of the macro
        self.foreign = {}  # foreign statements
        self.origin = None  # origin of the macro
        self.eeqMacro = None  # equivalent eeschema macro name (None = "")
        self.size = None  # size of the macro
        self.symetry = []  # symetry statement values
        self.sites = {}  # sites of the macro
        self.pins = {}  # dictionary of pin statements
        self.obs = {}  # dictionary of obstruction statements
        self.density = {}  # dictionary of density statements
        self.properties = {}  # dictionary of property statements

    def __str__(self):
        """_summary_
        The class object str description.
        Args:
            object (LefMacro): statement object
        """
        return super().__str__()

    def parse_data(self, data):
        """_summary_
        Method to add information relative to a class obejct field.
        Args:
            data (tuple): (name of the variable, data of the variable statement)
        """
        statement = data[0]
        value = data[1]
        if statement == "CLASS":
            if type(value) != LefClassType:
                raise TypeError("LefMacro: CLASS needs to be LefClassType object")
            self.macroClass = value
        elif statement == "FIXEDMASK":
            self.fixedMask = True
        elif statement == "FOREIGN":
            if type(value) != LefForeign:
                raise TypeError("LefMacro: FOREIGN needs to be LefForeign object")
            self.foreign[value.foreignCellName] = value  # value is a LefForeign object
        elif statement == "ORIGIN":
            if type(value) != LefPoint:
                raise TypeError("LefMacro: ORIGIN needs to be LefPoint object")
            self.origin = value  # value is an LEF point
        elif statement == "EEQ":
            if type(value) != str:
                raise TypeError("LefMacro: EEQ needs to be str")
            self.eeq = value  # value is a str
        elif statement == "SIZE":
            if type(value) != LefSize:
                raise TypeError("LefMacro: SIZE needs to be LefSize object")
            self.size = value  # value is a LefSize object
        elif statement == "SYMMETRY":
            if type(value) != LefSymmetry:
                raise TypeError("LefSite: SYMMETRY needs to be LefSymmetry object")
            self.symmetry.append(value)
        elif statement == "SITE":
            if type(value) != LefSite:
                raise TypeError("LefMacro: SITE needs to be LefSite object")
            self.sites[value.name] = value  # value is a LefSite object
        elif statement == "PIN":
            if type(value) != LefPin:
                raise TypeError("LefMacro: PIN needs to be LefPin object")
            self.pins[value.name] = value
        elif statement == "OBS":
            if type(value) != LefObs:
                raise TypeError("LefMacro: OBS needs to be LefObs object")
            self.obs[value.name] = value
        elif statement == "DENSITY":
            if type(value) != LefDensity:
                raise TypeError("LefMacro: DENSITY needs to be LefDensity object")
            self.density[value.name] = value
        elif statement == "PROPERTY":
            if type(value) != LefProperty:
                raise TypeError("LefMacro: PROPERTY needs to be LefProperty object")
            self.properties[value.name] = value
        else:
            raise TypeError(f"LefMacro: {statement} is not a valid statement")


class LefLayerType(Enum):
    """
    Enum class for the LEF layer statement types.
    Args:
        CUT         : cut layer type
        ROUTING     : routing layer type
        MASTERSLICE : masterslice layer type
        OVERLAP     : overlap layer type
    """

    CUT = 1
    ROUTING = 2
    MASTERSLICE = 3
    OVERLAP = 4


class LefLayer(LefStatement):
    def __init__(self, name, layerType: LefLayerType):
        self.type = layerType
        self.name = name

    def __str__(self):
        return f"{self.type.name} {self.name}"


class LefLayerCut(LefLayer):
    def __init__(self, name):
        """_summary_
        Class constructor.
        Args:
            name (str): name of the layer
        """
        super().__init__(name, LefLayerType.CUT)
        self.mask = None
        self.spacing = []
        self.spacingTable = None
        self.arraySpacing = None
        self.width = None
        self.enclosure = []
        self.preferEnclosure = []
        self.resistance = None
        self.property = {}
        self.acCurrentDensity = None
        self.dcCurrentDensity = None
        self.antennaModel = []
        self.antennaAreaRatio = []
        self.antennaDiffAreaRatio = []
        self.antennaCumAreaRatio = []
        self.antennaCumDiffAreaRatio = []
        self.antennaAreaFactor = []
        self.antennaCumRoutingPlusCut = False
        self.antennaGatePlusDiff = None
        self.antennaAreaMinusDiff = None
        self.antennaAreaDiffReducePWL = None

    def __str__(self):
        """_summary_
        The class object string description.
        Args:
            self (LefLayerCut): class object
        Returns:
            str: class object string description
        """
        ret = super().__str__() + "\n"
        # build the string body
        if self.mask is not None:
            ret += "MASK {} ;\n".format(self.mask)
        for spacing in self.spacing:
            ret += "\t{}\n".format(str(spacing))
        if self.spacingTable is not None:
            ret += "\t{} ;\n".format(str(self.spacingTable))
        if self.arraySpacing is not None:
            ret += "\t{} ;\n".format(str(self.arraySpacing))
        if self.width is not None:
            ret += "\tWIDTH {} ;\n".format(str(self.width))
        for enclosure in self.enclosure:
            ret += "\t{}\n".format(str(enclosure))
        for preferEnclosure in self.preferEnclosure:
            ret += "\t{}\n".format(str(preferEnclosure))
        if self.resistance is not None:
            ret += "\tRESISTANCE {} ;\n".format(str(self.resistance))
        for prop in self.property.values():
            ret += "\t{} ;\n".format(str(prop))
        if self.acCurrentDensity is not None:
            ret += "\t{}\n".format(str(self.acCurrentDensity))
        if self.dcCurrentDensity is not None:
            ret += "\t{}\n".format(str(self.dcCurrentDensity))
        for antennaModel in self.antennaModel:
            ret += "\t{}\n".format(str(antennaModel))
        for antennaAreaRatio in self.antennaAreaRatio:
            ret += "\t{}\n".format(str(antennaAreaRatio))
        for antennaDiffAreaRatio in self.antennaDiffAreaRatio:
            ret += "\t{}\n".format(str(antennaDiffAreaRatio))
        for antennaCumAreaRatio in self.antennaCumAreaRatio:
            ret += "\t{}\n".format(str(antennaCumAreaRatio))
        for antennaCumDiffAreaRatio in self.antennaCumDiffAreaRatio:
            ret += "\t{}\n".format(str(antennaCumDiffAreaRatio))
        for antennaAreaFactor in self.antennaAreaFactor:
            ret += "\t{}\n".format(str(antennaAreaFactor))
        if self.antennaCumRoutingPlusCut:
            ret += "\tANTENNACUMROUTINGPLUSCUT ;\n"
        if self.antennaGatePlusDiff is not None:
            ret += "\t{}\n".format(str(self.antennaGatePlusDiff))
        if self.antennaAreaMinusDiff is not None:
            ret += "\t{}\n".format(str(self.antennaAreaMinusDiff))
        if self.antennaAreaDiffReducePWL is not None:
            ret += "\t{}\n".format(str(self.antennaAreaDiffReducePWL))
        ret += "END {}\n".format(self.name)
        return ret

    def parseData(self, data):  # TODO : add the parsing of the data
        raise NotImplementedError("LefLayerCut: parseData not implemented")


class LefLayerRouting(LefLayer):  # TODO : implement
    """_summary_
    A LEF LAYER of TYPE ROUTING statement.
    Args:
        LefLayer (_type_): _description_
    """

    def __init__(self):
        raise NotImplementedError("LefLayerRouting: not implemented")


class LefVia(LefStatement):  # TODO : implement
    """_summary_
    A LEF VIA (DEFAULT) statement.
    Args:
        LefLayer (_type_): _description_
    """

    def __init__(self):
        raise NotImplementedError("LefVia: not implemented")


class LefViaRule(LefStatement):  # TODO : implement
    """_summary_
    A LEF VIARULE statement, of type GENERATE or not.
    Args:
        LefLayer (_type_): _description_
    """

    def __init__(self):
        raise NotImplementedError("LefViaRule: not implemented")


class LefUnits(LefStatement):  # TODO : implement
    """_summary_
    An LEF LIBRARY UNITS statement.
    Args:
        LefStatement (_type_): _description_
    """

    def __init__(self):
        raise NotImplementedError("LefUnits: not implemented")


class LefLibrary(LefStatement):  # TODO : implement
    """_summary_
    an LEF LIBRARY data structure holding all the info regarding
    a technology node declared inside the ".lef" or ".tlef" file.
    Args:
        LefStatement (_type_): _description_
    """

    def __init__(self):
        raise NotImplementedError("LefLibrary: not implemented")


#   TODO: IMPLEMENT LEF/TLEF LIBRARY MODULE
#   TODO: IMPLEMENT LEF_WRITE FILE
#   TODO: IMPLEMENT LEF_READ FILE
