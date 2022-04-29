"""_summary_
An utilities file containing data structures and other data
that is used both in LEF parsing and DEF parsing.
"""

from collections import defaultdict
from enum import Enum
from pickletools import uint8
import pstats
import numpy as np


class Unsupported(object):
    """_summary_
    A class that represents an unsupported feature.
    """

    def __init__(self, feature):
        self.feature = feature

    def __str__(self):
        return f"Unsupported feature: {self.feature}"


"""
List of possible LFEF keywords
"""
LEF_STATEMENTS = [
    "VERSION",
    "DIVIDERCHAR",
    "BUSBITCHARS",
    "DESIGN",
    "UNITS",
    "FREQUENCY",
    "TIME",
    "OHMS",
    "NANOSECONDS",
    "PICOFARADS",
    "DATABASE",
    "MICRONS",
    "MANUFACTURINGGRID",
    "SYMMETRY",
    "CLASS",
    "CORE",
    "SIZE",
    "END",
    "PROPERTY",
    "LAYER",
    "ROW",
    "SITE",
    "VIA",
    "VIARULE",
    "SPACING",
    "ORIGIN",
    "PITCH",
    "OFFSET",
    "MASK",
    "PATTERN",
    "MACRO",
    "PIN",
    "GATE",
    "GENERATE",
    "SPACINGTABLE",
    "ARRAYSPACING",
    "WIDTH",
    "LENGTH",
    "ENCLOSURE",
    "PREFERENCLOSURE",
    "RESISTANCE",
    "RPERSQ",
    "CAPACITANCE",
    "CPERSQDIST",
    "EDGECAPACITANCE",
    "NET",
    "DCCURRENTDENSITY",
    "VOLTAGE",
    "ACCURRENTDENSITY",
    "ANTENNAMODEL",
    "ANTENNAAREARATIO",
    "ANTENNADIFFAREARATIO",
    "ANTENNACUMAREARATIO",
    "ANTENNACUMDIFFAREARATIO",
    "ANTENNAAREAFACTOR",
    "ANTENNACUMROUTINGPLUSCUT",
    "ANTENNAGATEPLUSDIFF",
    "ANTENNAAREAMINUSDIFF",
    "ANTENNAAREADIFFREDUCEPWL",
    "CUT",
    "ROUTING",
    "PWL",
    "RECT",
    "POLYGON",
    "OVERLAP",
    "MASTERSLICE",
    "BUMP",
    "DIELECTRIC",
    "DIRECTION",
    "MINWIDTH",
    "MINENCLOSEDAREA",
    "PARALLELRUNLENGTH",
    "THICKNESS",
    "AVERAGE",
    "PEAK",
    "RMS",
]


class LefDecimal:
    """_summary_
    A special LEF decimal representation.
    Args:
        object (LefDecimal): LefDecimal class object
    """

    def __init__(self, value: float):
        """_summary_
        The class object constructor.
        Args:
            value (float) : decimal value.
        """
        self.value = value

    def __str__(self):
        """_summary_
        The class object string description.
        Args:
            object (LefDecimal): LefDecimal class object
        """
        return f"{self.value}"

    def __add__(self, other):
        """_summary_
        The class object addition operator.
        Args:
            object (LefDecimal): LefDecimal class object
        """
        return LefDecimal(self.value + other.value)

    def __sub__(self, other):
        """_summary_
        The class object subtraction operator.
        Args:
            object (LefDecimal): LefDecimal class object
        """
        return LefDecimal(self.value - other.value)

    def __mult__(self, other):
        """_summary_
        The class object multiplication operator.
        Args:
            object (LefDecimal): LefDecimal class object
        """
        return LefDecimal(self.value * other.value)

    def __truediv__(self, other):
        """_summary_
        The class object division operator.
        Args:
            object (LefDecimal): LefDecimal class object
        """
        return LefDecimal(self.value / other.value)

    def __floordiv__(self, other):
        """_summary_
        The class object division operator.
        Args:
            object (LefDecimal): LefDecimal class object
        """
        return LefDecimal(self.value // other.value)

    def __mod__(self, other):
        """_summary_
        The class object modulus division operator.
        Args:
            object (LefDecimal): LefDecimal class object
        """
        return LefDecimal(self.value % other.value)

    def __eq__(self, other):
        """_summary_
        The class object equality operator.
        Args:
            object (LefDecimal): LefDecimal class object
        """
        return self.value == other.value

    def __ne__(self, other):
        """_summary_
        The class object inequality operator.
        Args:
            object (LefDecimal): LefDecimal class object
        """
        return self.value != other.value

    def __lt__(self, other):
        """_summary_
        The class object less than operator.
        Args:
            object (LefDecimal): LefDecimal class object
        """
        return self.value < other.value

    def __le__(self, other):
        """_summary_
        The class object less than or equal operator.
        Args:
            object (LefDecimal): LefDecimal class object
        """
        return self.value <= other.value

    def __gt__(self, other):
        """_summary_
        The class object greater than operator.
        Args:
            object (LefDecimal): LefDecimal class object
        """
        return self.value > other.value

    def __ge__(self, other):
        """_summary_
        The class object greater than or equal operator.
        Args:
            object (LefDecimal): LefDecimal class object
        """
        return self.value >= other.value

    def __neg__(self):
        """_summary_
        The class object negation operator.
        Args:
            object (LefDecimal): LefDecimal class object
        """
        return LefDecimal(-self.value)

    def __abs__(self):
        """_summary_
        The class object absolute value operator.
        Args:
            object (LefDecimal): LefDecimal class object
        """
        return LefDecimal(abs(self.value))

    def __round__(self, ndigits=None):
        """_summary_
        The class object rounding operator.
        Args:
            object (LefDecimal): LefDecimal class object
        """
        return LefDecimal(round(self.value, ndigits))


class LefPoint:
    """_summary_
    A point for LEF geometries.

    Raises:
        TypeError: _description_

    Returns:
        _type_: _description_
    """

    def __init__(self, x: float, y: float):
        self.x = LefDecimal(x)
        self.y = LefDecimal(y)

    def __add__(self, other):
        return LefPoint(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return LefPoint(self.x - other.x, self.y - other.y)

    def __str__(self):
        return f"({self.x}, {self.y})"


class LefStepPattern(object):
    """_summary_

    Args:
        xCount (int): _description_

    Raises:
        TypeError: _description_

    Returns:
        _type_: _description_
    """

    def __init__(
        self, xCount: uint8, yCount: uint8, xStep: LefDecimal, yStep: LefDecimal
    ):
        self.xCount = xCount
        self.yCount = yCount
        self.xStep = xStep
        self.yStep = yStep

    def __str__(self):
        """_summary_
        A string representation of the object.
        Args:
            object (LefStepPattern): LefStepPattern object
        """
        return f"DO {self.xCount} BY {self.yCount} STEP {self.xStep} {self.yStep}"


class LefGeometryClass(Enum):
    """_summary_
    LEF geometry statement types.
    Args:
        RECT    : Rectangle
        PATH    : Path
        POLYGON : Polygon
        VIA     : Via
    """

    LAYER = 0
    RECT = 1
    PATH = 2
    POLYGON = 3
    VIA = 4


class LefGeometry(object):
    """_summary_
    A geometry parent class for LEF geometries.
    """

    def __init__(self, type):
        """_summary_
        The class object constructor.
        Args:
            type (LefGeometryClass): The geometry type.
            points (list):
        """
        self.type = type
        self.mask = None
        self.iterate = False
        self.points = None
        self.stepPattern = None

    def __str__(self):
        rets = ""
        points = f'{" ".join([str(p) for p in self.points])}'
        rets = f"{self.type.name} "
        if self.type != LefGeometryClass.VIA:
            if self.mask != None:
                rets += f"MASK {str(self.mask)} "
            if self.iterate:
                rets += "ITERATE "
        else:
            if self.iterate:
                rets += "ITERATE "
            if self.mask != None:
                rets += f"MASK {str(self.mask)} "
        rets += points
        if self.stepPattern != None:
            rets += f" {str(self.stepPattern)}"
        return rets

    def parse_data(self, data):
        """_summary_
        Parse the geometry data into the geometry object fields.
        Args:
            data (list): data[0] = statement name, data[1] = geometry data
        """
        statement = data[0]
        value = data[1]
        if statement == "MASK":
            if type(value) != uint8:
                raise TypeError("MASK value must be an unsigned 8-bit integer")
            self.mask = value
        elif statement == "ITERATE":
            if type(value) != bool:
                raise TypeError("ITERATE value must be a boolean")
            self.iterate = True
        else:
            raise TypeError(f"Unknown geometry statement: {statement}")

    def add_points(self, points: list):
        """_summary_
        Adds the points to the LEF geometry object.
        Args:
            points (list): _description_
            pathWidth (float, optional): _description_. Defaults to None.
        Raises:
            TypeError
        """
        if self.points is None:
            raise TypeError("Points must be added")
        if self.type == LefGeometryClass.PATH and len(points) < 2:
            raise TypeError("Path must have at least 2 points")
        if self.type == LefGeometryClass.POLYGON and len(points) < 3:
            raise TypeError("Polygon must have at least 3 points")
        if self.type == LefGeometryClass.VIA and len(points) != 1:
            raise TypeError("Via must have exactly 1 point")
        if self.type == LefGeometryClass.RECT and len(points) != 2:
            raise TypeError("Rectangle must have exactly 2 points")
        self.points = np.ndarray([LefPoint(p[0], p[1]) for p in points])

    def add_stepPattern(self, stepPattern: LefStepPattern):
        """_summary_
        Adds the step pattern to the LEF geometry object.
        Args:
            stepPattern (list): _description_
        Raises:
            TypeError
        """
        if self.stepPattern is None:
            raise TypeError("Step pattern is None")
        self.stepPattern = stepPattern


class LefRect(LefGeometry):
    """_summary_
    A child class for LEF RECT geometries.
    """

    def __init__(self, type):
        super().__init__(LefGeometryClass.RECT)
        self.density = None

    def __str__(self):
        ret = super().__str__()
        if self.density != None:
            ret += f" {self.density}"
        return ret

    def add_points(self, points: list):
        return super().add_points(points)

    def add_stepPattern(self, stepPattern: LefStepPattern):
        return super().add_stepPattern(stepPattern)

    def add_density(self, density):
        """_summary_
        Adds the density to the LEF geometry object.
        Args:
            density (float): density of the rect in DENSITY statements
        Raises:
            TypeError
        """
        if self.density != None:
            raise TypeError("Density already set")
        if type(density) == LefDecimal:
            self.density = density
        elif type(density) == float:
            self.density = LefDecimal(density)
        else:
            raise TypeError("Density must be a float or LefDecimal")


class LefPath(LefGeometry):
    """_summary_
    A child class for LEF PATH geometries.
    """

    def __init__(self, type):
        super().__init__(LefGeometryClass.PATH)
        self.pathWidth = None

    def __str__(self):
        return super().__str__()

    def add_points(self, points: list):
        return super().add_points(points)

    def add_pathWidth(self, pathWidth):
        """_summary_
        Adds the path width to the geometry object.
        Args:
            pathWidth (float): _description_
        Raises:
            TypeError
        """
        if self.points is None:
            raise TypeError("Points must be added")
        if type(pathWidth) == float:
            self.pathWidth = LefDecimal(pathWidth)
        elif type(pathWidth) == LefDecimal:
            self.pathWidth = pathWidth
        else:
            raise TypeError("Path width must be a float or LefDecimal")

    def add_stepPattern(self, stepPattern: LefStepPattern):
        return super().add_stepPattern(stepPattern)


class LefDesignRuleWidth(object):
    def __init__(self, value):
        if type(value) == float:
            self.value = LefDecimal(value)
        elif type(value) == LefDecimal:
            self.value = value
        else:
            raise TypeError("Design rule width must be a float or LefDecimal")

    def __str__(self):
        return f"DESIGNRULEWIDTH {str(self.value)}"


class LefViaGeom(LefGeometry):
    """_summary_
    A child class for LEF VIA geometries.
    """

    def __init__(self):
        super().__init__(LefGeometryClass.VIA)
        self.viaWidth = None

    def __str__(self):
        return super().__str__()

    def add_points(self, points: list):
        return super().add_points(points)

    def add_viaWidth(self, viaWidth: float):
        """_summary_
        Adds the via width to the geometry object.
        Args:
            viaWidth (float): _description_
        Raises:
            TypeError
        """
        if self.points is None:
            raise TypeError("Points must be added")
        if type(viaWidth) != float:
            raise TypeError("Via width must be a float")
        self.viaWidth = LefDecimal(viaWidth)

    def add_stepPattern(self, stepPattern: LefStepPattern):
        return super().add_stepPattern(stepPattern)


class LefLayerGeom(LefGeometry):
    def __init__(self, name: str):
        super().__init__(LefGeometryClass.LAYER)
        self.name = name
        self.exceptPgNet = False
        self.designRule = None
        self.width = None
        self.geometries = []

    def __str__(self):
        ret = "LAYER {}\n".format(self.name)
        if self.exceptPgNet:
            ret += "\tEXCEPTPGNET\n"
        if self.spacing is not None:
            ret += "\t{} ;\n".format(str(self.spacing))
        if self.width is not None:
            ret += "{} ;\n".format(str(self.width))
        for g in self.geometries:
            ret += "\t{} ;\n".format(str(g))
        return ret

    def parse_data(self, data):
        """_summary_
        Parse the geometry data into the geometry object fields.
        Args:
            data (list): data[0] = statement name, data[1] = geometry data
        """
        statement = data[0]
        value = data[1]
        if statement == "EXCEPTPGNET":
            self.exceptPgNet = True
        elif statement == "SPACING":
            if type(value) != LefSpacing:
                raise TypeError("SPACING value must be a LefSpacing object")
            self.designRule = value
        elif statement == "DESIGNRULEWIDTH":
            if type(value) == LefDesignRuleWidth:
                self.designRule = value
            elif type(value) in [LefDecimal, float]:
                self.designRule = LefDesignRuleWidth(value)
            else:
                raise TypeError(
                    "DESIGNRULEWIDTH value must be a LefDesignRuleWidth object"
                )
        elif statement == "WIDTH":
            if type(value) == float:
                self.width = LefDecimal(value)
            elif type(value) == LefDecimal:
                self.width = value
            else:
                raise TypeError("WIDTH value must be a float or LefDecimal object")
        elif statement == "RECT":
            if type(value) != LefRect:
                raise TypeError("RECT value must be a LefRect object")
            self.geometries.append(value)
        elif statement == "PATH":
            if type(value) != LefPath:
                raise TypeError("PATH value must be a LefPath object")
            self.geometries.append(value)
        elif statement == "POLYGON":
            if type(value) != LefPolygon:
                raise TypeError("POLYGON value must be a LefPolygon object")
            self.geometries.append(value)
        else:
            raise TypeError(f"Unknown geometry statement: {statement}")


class LefPolygon(LefGeometry):
    """_summary_
    A child class for LEF RECT geometries.
    """

    def __init__(self):
        super().__init__(LefGeometryClass.POLYGON)

    def __str__(self):
        return super().__str__()

    def add_points(self, points: list):
        return super().add_points(points)

    def add_stepPattern(self, stepPattern: LefStepPattern):
        return super().add_stepPattern(stepPattern)


class LefSpacingValType(Enum):
    """_summary_
    Possible LEF SPACING statement values.
    Args:
        LAYER           : Secondary layer statement
        ADJACENTCUTS    : Adjacent cuts statement
        PARALLELOVERLAP : Parallel overlap statement
        AREA            : Area statement
    """

    LAYER = 1
    ADJACENTCUTS = 2
    PARALLELOVERLAP = 3
    AREA = 4


class LefSecondaryLayer(object):
    """_summary_
    A LEF secondary layer object to use as a SPACING statement value.
    Args:
        object (_type_): _description_
    """

    def __init__(self, layerName: str, stack: bool):
        self.layerName = layerName
        self.stack = stack

    def __str__(self):
        ret = f"LAYER {self.layerName}"
        if self.stack:
            ret += " STACK"
        return ret


class LefAdjacentCuts(object):
    """_summary_
    A LEF ADJACENTCUTS object to use as a SPACING statement value.
    Args:
        object (_type_): _description_
    """

    def __init__(self, numVia: uint8, cutWithin: float, exceptSamePgNet: bool):
        if numVia not in [2, 3, 4]:
            raise ValueError("Number of vias must be 2, 3, or 4")
        self.numVia = numVia
        self.cutWithin = LefDecimal(cutWithin)
        self.exceptSamePgNet = exceptSamePgNet

    def __str__(self):
        ret = f"ADJACENTCUTS {self.numVia} WITHIN {self.cutWithin}"
        if self.exceptSamePgNet:
            ret += " EXCEPTSAMEPGNET"
        return ret


class LefSpacing(object):
    """_summary_
    An LEF Spacing table.
    Args:
        object (_type_): _description_
    """

    def __init__(self, cutSpacing: float):
        self.cutSpacing = LefDecimal(cutSpacing)
        self.centerToCenter = False
        self.sameNet = False
        self.valueType = None
        self.value = None

    def __str__(self) -> str:
        ret = f"SPACING {self.cutSpacing}"
        if self.centerToCenter:
            ret += "\n\tCENTERTOCENTER"
        if self.sameNet:
            ret += "\n\tSAMENET"
        if self.valueType is not None:
            if self.valueType in [
                LefSpacingValType.LAYER,
                LefSpacingValType.ADJACENTCUTS,
            ]:
                ret += "\n\t{}".format(str(self.value))
            elif self.valueType == LefSpacingValType.PARALLELOVERLAP:
                ret += "\n\t{}".format(self.valueType.name)
            elif self.valueType == LefSpacingValType.AREA:
                ret += "\n\t{} {}".format(self.valueType.name, str(self.value))
            else:
                raise ValueError("Unknown value type")
        ret += "\n;"
        return ret

    def parse_data(self, data):
        statement = data[0]
        value = data[1]
        if statement == "CENTERTOCENTER":
            self.centerToCenter = True
        elif statement == "SAMENET":
            self.sameNet = True
        elif statement == "LAYER":
            if type(value) is not LefSecondaryLayer:
                raise TypeError("Value must be a LefLayerGeom object")
            self.valueType = LefSpacingValType.LAYER
            self.value = value  # value is a LefSecondaryLayer object
        elif statement == "ADJACENTCUTS":
            if type(value) is not LefAdjacentCuts:
                raise TypeError("Value must be a LefAdjacentCuts object")
            self.valueType = LefSpacingValType.ADJACENTCUTS
            self.value = value  # value is a LefAdjacentCuts object
        elif statement == "PARALLELOVERLAP":
            self.valueType = LefSpacingValType.PARALLELOVERLAP
        elif statement == "AREA":
            self.valueType = LefSpacingValType.AREA
            if type(value) is float:
                self.value = LefDecimal(value)
            elif type(value) is LefDecimal:
                self.value = value
            else:
                raise TypeError("Value must be a float or LefDecimal object")
        else:
            raise ValueError("Unknown statement")


# TODO: develop LayerGeometry Class as part of layer geometries
class LefLayerGeometry(object):
    """_summary_
    A LEF LAYER GEOMETRY statement for MACROs.
    Args:
        object (_type_): _description_
    """

    def __init__(self, name: str):
        """_summary_
        Class constructor.
        Args:
            name (str)              : name of the layer geometry
        """
        self.geometries = []

    def __str__(self):
        """_summary_
        Returns a string representation of the object.
        Args:
            object (_type_): LefLayerGeometry object
        Returns:
            str : string representation of the object
        """
        return "".join("\t{} ;\n".format(str(geom)) for geom in self.geometries)

    def add_geometry(self, geom):
        """_summary_
        Adds a geometry to the layer geometry.
        Args:
            geom (LefGeometry) : geometry to add
        """
        if type(geom) is LefLayerGeom or type(geom) is LefViaGeom:
            self.geometries.append(geom)
        else:
            raise TypeError(
                "Layer Geometry must be a LefLayerGeom or LefViaGeom object"
            )


class LefDensity(object):
    def __init__(self):
        """_summary_
        Class constructor.
        Args:
            object (_type_): LefDensity object
        """
        self._currentLayer = ""  # state variable to know
        # to which layer the rect
        # will be declared in
        self.layerRectDict = defaultdict(list)

    def __str__(self):
        """_summary_
        String representation of the object.
        Args:
            object (_type_): LefDensity object
        Returns:
            str : string representation of the object
        """
        ret = "DENSITY\n"
        for layer in self.layerRectDict.keys():
            ret += "\tLAYER {} ;\n".format(layer)
            for rect in self.layerRectDict[layer]:
                ret += "\t\t{} ;\n".format(str(rect))
        ret += "END"
        return ret

    def parse_data(self, data):
        """_summary_
        Parses the data and adds the rectangles to the
        respective layer in the DENSITY statement.
        Args:
            data (Tuple): (statement, value)
        Raises:
            TypeError: Value must be a nust be a string
            TypeError: Value must be a LefRect object
            ValueError: Unknown statement
        """
        statement = data[0]
        value = data[1]
        if statement == "LAYER":
            if type(value) is not str:
                raise TypeError("Value following LAYER statement must be a string")
            self._currentLayer = value
        elif statement == "RECT":
            if type(value) is not LefRect:
                raise TypeError(
                    "Value following RECT statement must be a LefRect object"
                )
            self.layerRectDict[self._currentLayer].append(value)
        else:
            raise ValueError("Unknown statement")


class LefPieceWiseLinearInterpol(object):
    """_summary_
    LEF Piecewise Linear interpolation data struct (PWL).
    """

    def __init__(self, points):
        """_summary_
        The class object constructor.
        Args:
            points (list): list of points
        """
        self.points = np.ndarray([LefPoint(p[0], p[1]) for p in points])

    def __str__(self):
        """_summary_
        A str representation of the LEF PWL statement value.
        Args:
            object (LefPieceWiseLinearInterpol): LEF PWL value
        """
        points = "".join([f" ( {str(p)} ) " for p in self.points])
        return f"PWL ({points})"


class LefAntennaFieldType(Enum):
    """_summary_
    An enum class for antenna field types.
    Args:
        ANTENNAMODEL : ANTENNAMODEL statement
        ANTENNAPARTIALMETALAREA : ANTENNAPARTIALMETALAREA statement
        ...
    """

    ANTENNAMODEL = 1
    ANTENNAPARTIALMETALAREA = 2
    ANTENNAPARTIALMETALSIDEAREA = 3
    ANTENNAPARTIALCUTAREA = 4
    ANTENNADIFFAREA = 5
    ANTENNAGATEAREA = 6
    ANTENNAMXAAREACAR = 7
    ANTENNAMAXSIDEAREACAR = 8
    ANTENNAMAXCUTCAR = 9
    ANTENNAAREARATIO = 10
    ANTENNADIFFAREARATIO = 11
    ANTENNACUMAREARATIO = 12
    ANTENNACUMDIFFAREARATIO = 13
    ANTENNAAREAFACTOR = 14
    ANTENNACUMROUTINGPLUSCUT = 15
    ANTENNAGATEPLUSDIFF = 16
    ANTENNAAREAMINUSDIFF = 17
    ANTENNAAREADIFFREDUCEPWL = 18


class LefAntennaModel(Enum):
    """_summary_
    Enumeration of possible antenna model types.
    Args:
        OXIDE1 : oxide1 antenna type
        OXIDE2 : oxide2 antenna type
        OXIDE3 : oxide3 antenna type
        OXIDE4 : oxide4 antenna type
    """

    OXIDE1 = 1
    OXIDE2 = 2
    OXIDE3 = 3
    OXIDE4 = 4


class LefAntennaField(object):
    """_summary_
    A LEF ANTENNA FIELD statement data structure
    """

    def __init__(
        self,
        fieldType: LefAntennaFieldType,
    ):
        """_summary_
        The class object constructor.
        Args:
            name (str)               : property name
            value (str/LefDecimal)   : property value
        Raises:
            TypeError
        """
        if type(fieldType) != LefAntennaFieldType:
            raise TypeError("LefAntennaField: fieldType must be LefAntennaFieldType")
        self.fieldType = fieldType
        self.layerName = ""
        self.value = (
            None  # can either be LefDecimal or PWL class object, or a antenna model
        )
        self.diffuseOnly = False

    def __str__(self):
        """_summary_
        str representation of the LEF ANTENNA FIELD statement value.
        Returns:
            ret (str): str representation of the LEF ANTENNA FIELD statement
        """
        ret = f"{self.fieldType.name}"
        if self.value != None:
            ret += f" {str(self.value)}"
        if self.layerName != "":
            ret += f" LAYER {self.layerName}"
        if self.diffuseOnly:
            ret += " DIFFUSEONLY"
        return ret

    def parse_data(self, data):
        """_summary_
        Parses the data for the LEF ANTENNA FIELD statement.
        Args:
            data (Tuple): (statment : str, value: Generic Type)
        Raises:
            TypeError: Unknown statement
        """
        statement = data[0]
        value = data[1]
        if statement == "LAYER":
            self.layerName = value
        elif statement == "PWL":
            if type(value) != LefPieceWiseLinearInterpol:
                raise TypeError(
                    "LefAntennaField: PWL needs to be LefPieceWiseLinearInterpol object"
                )
            self.value = value
        elif statement == "DIFFUSEONLY":
            self.diffuseOnly = True
        elif statement == "OXIDE1":
            self.value = LefAntennaModel.OXIDE1
        elif statement == "OXIDE2":
            self.value = LefAntennaModel.OXIDE2
        elif statement == "OXIDE3":
            self.value = LefAntennaModel.OXIDE3
        elif statement == "OXIDE4":
            self.value = LefAntennaModel.OXIDE4
        else:
            raise TypeError(f"LefAntennaField: {statement} is not a valid statement")


class LefPort(object):
    """_summary_
    A LEF PORT statement data structure
    """

    def __init__(self):
        self.name = None
        self.type = LefStatementType.PORT
        self.portClass = None
        self.layerGeometries = []

    def __str__(self):
        ret = "PORT\n".format(self.name)
        if self.portClass != None:
            ret += "CLASS {} ;\n".format(self.portClass.name)
        for layerGeometry in self.layerGeometries:
            ret += "{}\n".format(layerGeometry)
        return ret


class LefWithin(object):
    """_summary_
    A LEF WITHIN statement data structure
    """

    def __init__(self, cutWithin, spacing):
        if type(cutWithin) == float:
            self.cutwithin = LefDecimal(cutWithin)
        elif type(cutWithin) == LefDecimal:
            self.cutwithin = cutWithin
        else:
            raise TypeError("LefWithin: cutWithin must be LefDecimal or float")
        if type(spacing) == float:
            self.orthoSpacing = LefDecimal(spacing)
        elif type(spacing) == LefDecimal:
            self.orthoSpacing = spacing
        else:
            raise TypeError("LefWithin: spacing must be LefDecimal or float")

    def __str__(self):
        return f"WITHIN {str(self.cutwithin)} SPACING {str(self.orthoSpacing)}"


class LefSpacingTableType(Enum):
    """_summary_
    A LEF SPACINGTABLE type enumerator
    Args:
        None
        ORTHOGONAL : Orthogonal spacing table
    """

    None
    ORTHOGONAL = 1


class LefSpacingTable(object):
    def __init__(self, type):
        if type(type) != LefSpacingTableType:
            raise TypeError("LefSpacingTable: type must be LefSpacingTableType")
        self.type = type
        self.rows = []

    def __str__(self):
        ret = "SPACINGTABLE"
        if self.type == LefSpacingTableType.ORTHOGONAL:
            return "SPACINGTABLE ORTHOGONAL\n"
        for row in self.rows:
            ret += "\t{}\n".format(str(row))
        ret += ";"
        return ret

    def parse_row(self, row):
        """_summary_
        Parse a new row into the spacing table
        Args:
            row (LefWithin) : A LefWithin object
        """
        if type(row) != LefWithin:
            raise TypeError("LefSpacingTable: row must be LefWithin")
        self.rows.append(row)


class LefTableEntries(object):  # TODO: implement
    def __init__(self) -> Unsupported:
        raise Unsupported("LefTableEntries: Not implemented")

    def __init__(self, rows=[]):
        self.rows = []
        if type(rows[0]) != list:
            raise TypeError(
                "LefTableEntries: rows must be a list of LefDecimal or float"
            )
        if type(rows[0][0]) not in [float, LefDecimal]:
            raise TypeError("LefTableEntries: row entries must be LefDecimal or float")
        for row in rows:
            if type(row[0]) is LefDecimal:
                self.rows.append(row)
            else:
                self.rows.append([LefDecimal(val) for val in row])

    def __str__(self):
        ret = "TABLEENTRIES\n"
        for row in self.rows:
            rowStr = "".join([f"{str(val)} " for val in row])
            ret += "\t{}\n".format(rowStr)
        return ret

    def addRow(self, row=[]):
        if type(row[0]) == LefDecimal:
            self.rows.append(row)
        elif type(row[0]) == float:
            self.rows.append([LefDecimal(val) for val in row])
        else:
            raise TypeError("LefTableEntries: row entries must be LefDecimal or float")


class LefArrayCuts(object):
    """_summary_
    A LEF ARRAYCUTS statement data structure
    """

    def __init__(self, arrayCuts, arraySpacing):
        if type(arrayCuts) == float:
            self.arrayCuts = LefDecimal(arrayCuts)
        elif type(arrayCuts) == LefDecimal:
            self.arrayCuts = arrayCuts
        else:
            raise TypeError("LefArrayCuts: arrayCuts must be LefDecimal or float")
        if type(arraySpacing) == float:
            self.arraySpacing = LefDecimal(arraySpacing)
        elif type(arraySpacing) == LefDecimal:
            self.orthoSpacing = arraySpacing
        else:
            raise TypeError("LefArrayCuts: arraySpacing must be LefDecimal or float")

    def __str__(self):
        return f"ARRAYCUTS {str(self.arrayCuts)} SPACING {str(self.arraySpacing)}"


class LefArrayTable(object):
    def __init__(self):
        self.longArray = False
        self.viaWidth = None
        self.cutSpacing = None
        self.rows = []

    def __str__(self):
        ret = "ARRAYTABLE"
        if self.longArray:
            ret += " LONGARRAY\n"
        if self.viaWidth != None:
            ret += "\tWIDTH {}".format(str(self.viaWidth))
        if self.cutSpacing != None:
            ret += " CUTSPACING {}\n".format(str(self.cutSpacing))
        for row in self.rows:
            ret += "\t{}\n".format(str(row))
        ret += ";"
        return ret

    def parse_row(self, row):
        if type(row) != LefArrayCuts:
            raise TypeError("LefArrayTable: row must be LefArrayCuts")
        self.rows.append(row)

    def parse_data(self, data):
        statement = data[0]
        value = data[1]
        if statement == "LONGARRAY":
            self.longArray = True
        elif statement == "WIDTH":
            if type(value) == float:
                self.viaWidth = LefDecimal(value)
            elif type(value) == LefDecimal:
                self.viaWidth = value
            else:
                raise TypeError("LefArrayTable: WIDTH must be LefDecimal or float")
        elif statement == "CUTSPACING":
            if type(value) == float:
                self.cutSpacing = LefDecimal(value)
            elif type(value) == LefDecimal:
                self.cutSpacing = value
            else:
                raise TypeError("LefArrayTable: CUTSPACING must be LefDecimal or float")
        else:
            raise TypeError(f"LefArrayTable: {statement} is not a valid statement")


class LefParamType(Enum):
    """_summary_
    A LEF PARAM type enumerator
    Args:
        Enum (_type_): _description_
    """

    LENGTH = 1
    WIDTH = 2


class LefParam(object):
    def __init__(self, typo: LefParamType, minParam, maxParam=None):
        """_summary_
        Class constructor
        Args:
            minWidth (_type_): _description_
            maxWidth (_type_, optional): _description_. Defaults to None.
        Raises:
            TypeError: width must be LefDecimal or float
        """
        self.type = typo
        # it is mandatory that at least minParam is parsed
        if type(minParam) == float:
            self.minParam = LefDecimal(minParam)
        elif type(minParam) == LefDecimal:
            self.minParam = minParam
        else:
            raise TypeError("LefParam: minParam must be LefDecimal or float")
        if maxParam != None:
            if type(maxParam) == float:
                self.maxParam = LefDecimal(maxParam)
            elif type(maxParam) == LefDecimal:
                self.maxParam = maxParam
            else:
                raise TypeError("LefParam: maxParam must be LefDecimal or float")
        self.exceptExtraCut = None

    def __str__(self):
        """_summary_
        String representation of the object statement
        Returns:
            _type_: _description_
        """
        ret = f"{self.type.name} {str(self.minParam)}"
        if self.maxParam != None:
            ret += f" {str(self.maxParam)}"
        if self.exceptExtraCut != None:
            ret += f" EXCEPTEXTRACUT {str(self.exceptExtraCut)}"
        return ret

    def addExceptExtraCut(self, cutWithin):
        """_summary_
        Add an EXCEPTEXTRACUT statement
        Args:
            exceptExtraCut (_type_): _description_
        """
        if type(cutWithin) == LefDecimal:
            self.exceptExtraCut = cutWithin
        elif type(cutWithin) == float:
            self.exceptExtraCut = LefDecimal(cutWithin)
        else:
            raise TypeError("LefParam: exceptExtraCut must be LefDecimal or float")


class LefWidth(LefParam):
    def __init__(self, minWidth, maxWidth=None):
        """_summary_
        Class constructor
        Args:
            minWidth (_type_): _description_
            maxWidth (_type_, optional): _description_. Defaults to None.
        Raises:
            TypeError: width must be LefDecimal or float
        """
        super().__init__(LefParamType.WIDTH, minWidth, maxWidth)

    def __str__(self):
        """_summary_
        String representation of the object statement
        Returns:
            _type_: _description_
        """
        super.__str__()

    def addExceptExtraCut(self, cutWithin):
        """_summary_
        Add an EXCEPTEXTRACUT statement
        Args:
            exceptExtraCut (_type_): _description_
        """
        super.addExceptExtraCut(cutWithin)


class LefLength(LefParam):
    def __init__(self, minLength, maxLength=None):
        """_summary_
        Class constructor
        Args:
            minLength (_type_): _description_
            maxLength (_type_, optional): _description_. Defaults to None.
        Raises:
            TypeError: length must be LefDecimal or float
        """
        super().__init__(LefParamType.LENGTH, minLength, maxLength)

    def __str__(self):
        """_summary_
        String representation of the object statement
        Returns:
            _type_: _description_
        """
        super.__str__()

    # doens't feature EXCEPTEXTRACUT statement


class LefEnclosureClass(Enum):
    ABOVE = 1
    BELOW = 2


class LefEnclosure(object):
    """_summary_
    A LEF ENCLOSURE statement data structure
    Args:
        object (_type_): _description_
    """

    def __init__(
        self, overhang1, overhang2, side: LefEnclosureClass = None, enclosureParam=None
    ):
        self.side = side
        self.overhang1 = overhang1
        self.overhang2 = overhang2
        self.enclosureParam = None
        if enclosureParam != None:
            if type(enclosureParam) in [LefWidth, LefLength]:
                self.enclosureParam = enclosureParam
            else:
                raise TypeError(
                    "LefEnclosure: enclosureParam must be LefWidth or LefLength"
                )

    def __str__(self):
        ret = "ENCLOSURE"
        if self.side != None:
            ret += f" {self.side.name}"
        ret += " {} {}\n".format(str(self.overhang1), str(self.overhang2))
        if self.enclosureParam != None:
            ret += "\t{}\n".format(str(self.enclosureParam))
        ret += ";"
        return ret


class LefPreferEnclosure(LefEnclosure):
    def __init__(
        self,
        overhang1,
        overhang2,
        side: LefEnclosureClass = None,
        enclosureParam: LefWidth = None,
    ):
        """_summary_

        Raises:

        Returns:
            _type_: _description_
        """
        super.__init__(overhang1, overhang2, side, enclosureParam)

    def __str__(self):
        """_summary_
        String representation of the object statement
        Returns:
            _type_: _description_
        """
        ret = "PREFERENCLOSURE"
        if self.side != None:
            ret += f" {self.side.name}"
        ret += f" {str(self.overhang1)} {str(self.overhang2)}"
        if self.enclosureParam != None:
            ret += f" {str(self.enclosureParam)}"
        ret += " ;"
        return ret


class LefFloatType(Enum):
    """_summary_
    LEF floating point types for each available statement
    Args:
        AVERAGE     : average floating point
        PEAK        : peak floating point
        RMS         : root mean square floating point
        RPERSQ      : resistance per square floating point
        CPERSQDIST  : capacitance per square distance floating point
    """

    None
    AVERAGE = 1
    PEAK = 2
    RMS = 3
    RPERSQ = 4
    CPERSQDIST = 5


class LefUnitType(Enum):
    """_summary_
    LEF unit types for each available statement
    Args:
       PICOFARADS : picoFarad
       OHMS       : ohm
       NANOSECONDS: nanosecond
       HERTZ      : hertz
    """

    None
    PICOFARAD = 1
    OHMS = 2
    NANOSECONDS = 3
    HERTZ = 5


class LefUnit(object):
    def __init__(self, unitType, unitValue):
        self.unitType = None
        if unitType is not None:
            if type(unitType) in [LefFloatType, LefUnitType]:
                self.unitType = unitType
            else:
                raise TypeError("LefUnit: unitType must be LefFloatType or LefUnitType")
        if type(unitValue) in [LefDecimal, int]:
            self.unitValue = unitValue
        elif type(unitValue) == float:
            self.unitValue = LefDecimal(unitValue)
        else:
            raise TypeError("LefUnit: unitValue must be LefDecimal, float or integer")

    def __str__(self):
        """_summary_
        String representation of the object statement
        Returns:
            _type_: _description_
        """
        ret = ""
        if self.unitType is not None:
            return f"{self.unitType.name} {str(self.unitValue)}"
        else:
            return str(self.unitValue)


class LefResistance(LefUnit):
    def __init__(self, resistance, unitType=None):
        """_summary_
        Class constructor
        Args:
            resistance (_type_): _description_
            unitType (_type_, optional): _description_. Defaults to LefFloatType.OHMS.
        Raises:
            TypeError: resistance must be LefDecimal or float
        """
        if unitType is None:
            super().__init__(None, resistance)

        elif unitType is LefUnitType.OHMS or unitType is LefFloatType.RPERSQ:
            super().__init__(unitType, resistance)
        else:
            raise TypeError(
                "LefResistance: type must be LefUnitType.OHMS or LefFloatType.RPERSQ"
            )

    def __str__(self):
        return f"RESISTANCE {super().__str__()}"


class LefCurrentDensityTableValue(object):
    def __init__(self):
        self.frequencies = []
        self.cutAreas = []
        self.tableEntries = None

    def __str__(self):
        if len(self.frequencies) <= 0:
            raise ValueError(
                "LefCurrentDensityTableValue: frequencies must not be an empty list"
            )
        ret = "" + "FREQUENCY"
        for freq in self.frequencies:
            ret += f" {str(freq)}"
        ret += " ;\n"
        if len(self.cutAreas) > 0:
            ret += "CUTAREA"
            for cutArea in self.cutAreas:
                ret += f" {str(cutArea)}"
            ret += " ;\n"
        if self.tableEntries is not None:
            ret += str(self.tableEntries)
        return ret

    def parseFrequency(self, frequency):
        """_summary_
        Adds a frequency to the list of frequencies
        Args:
            frequency (_type_): _description_
        Raises:
            TypeError: frequency must be LefDecimal or float
        """
        if type(frequency) in [LefDecimal, float]:
            self.frequencies.append(frequency)
        else:
            raise TypeError(
                "LefCurrentDensityTableValue: frequency must be LefDecimal or float"
            )

    def parseCutArea(self, cutArea):
        """_summary_
        Adds a cut area to the list of cut areas
        Args:
            cutArea (_type_): _description_
        Raises:
            TypeError: cutArea must be LefDecimal or float
        """
        if type(cutArea) in [LefDecimal, float]:
            self.cutAreas.append(cutArea)
        else:
            raise TypeError(
                "LefCurrentDensityTableValue: cutArea must be LefDecimal or float"
            )

    def parseTableEntry(self, tableEntries: LefTableEntries):
        self.tableEntries = tableEntries


class LefCurrentDensityType(Enum):
    """_summary_
    LEF Current Density statement types
    Args:
        AC : AC current density statement (ACCURRENTDENSITY)
        DC : DC current density statement (DCCURRENTDENSITY)
    """

    AC = 1
    DC = 2


class LefCurrentDensity(object):  # TODO: Implement
    def __init__(
        self, currentDensity, unitType: LefFloatType, typo: LefCurrentDensityType
    ):
        self.type = typo
        self.floatType = unitType
        if (
            type(currentDensity) == LefDecimal
            or type(currentDensity) != float
            and type(currentDensity) == LefCurrentDensityTableValue
        ):
            self.currentDensity = currentDensity
        elif type(currentDensity) == float:
            self.currentDensity = LefDecimal(currentDensity)
        else:
            raise TypeError(
                "LefCurrentDensity: currentDensity must be LefDecimal, float or a LefCurrentDensityTableValue"
            )

    def __str__(self):
        """_summary_

        Raises:
            Unsupported: _description_

        Returns:
            _type_: _description_
        """
        if type(self.currentDensity) in [LefDecimal, float]:
            return f"{self.floatType.name} {str(self.currentDensity)}"
        elif type(self.currentDensity) == LefCurrentDensityTableValue:
            return "{}\n{}".format(self.floatType.name, str(self.currentDensity))


class LefAcCurrentDensity(LefCurrentDensity):  # TODO: Implement
    def __init__(self, currentDensity, unitType: LefFloatType):
        if (
            type(currentDensity) is LefCurrentDensityTableValue
            and len(currentDensity.frequencies) is 0
        ):
            raise ValueError(
                "LefAcCurrentDensity: frequencies must not be an empty list"
            )
        super().__init__(currentDensity, unitType, LefCurrentDensityType.AC)

    def __str__(self):
        ret = "ACCURRENTDENSITY\n" + "\t{}\n".format(super().__str__())
        ret += ";\n"
        return ret


class LefDcCurrentDensity(LefCurrentDensity):  # TODO: Implement
    def __init__(self, currentDensity, unitType: LefFloatType):
        if unitType is not LefFloatType.AVERAGE:
            raise TypeError(
                "LefDcCurrentDensity: unitType must be LefFloatType.AVERAGE"
            )

        if (
            type(currentDensity) is LefCurrentDensityTableValue
            and len(currentDensity.frequencies) > 0
        ):
            raise ValueError("LefDcCurrentDensity: frequencies must not be parsed")
        super().__init__(currentDensity, unitType, LefCurrentDensityType.DC)

    def __str__(self):
        ret = "DCCURRENTDENSITY\n" + "\t{}\n".format(super().__str__())
        ret += ";\n"
        return ret


class LefProperty(object):
    def __init__(self, propName, propValue):
        self.propName = propName
        if type(propValue) == LefDecimal:
            self.propValue = propValue
        elif type(propValue) == float:
            self.propValue = LefDecimal(propValue)
        else:
            raise TypeError("LefProperty: propValue must be LefDecimal or float")

    def __str__(self):
        return f"PROPERTY {self.propName} {str(self.propValue)}"


class LefStatementType(Enum):
    """_summary_: LefStatementType
    Types of possible LEF super statements.
    Args:
        MACRO   : Macro statement.
        LAYER   : Layer statement.
        SITE    : Site statement.
        VIA     : Via statement.
        VIARULE : Via rule statement.
        OBS     : Obstruction statement.
        PIN     : Pin statement.
        PORT    : Port statement.
    """

    MACRO = 1
    LAYER = 2
    SITE = 3
    VIA = 4
    VIARULE = 5
    OBS = 6
    PIN = 7
    PORT = 8


class LefStatement(object):
    """_summary_
    A parent class for all LEF statements.
    Args:
        object (_type_): LefStatement class object
    """

    def __init__(self, name: str, type: LefStatementType):
        """_summary_
        The class object constructor.
        Args:
            name (str)           : str representation of the name of the  statement.
            type (LefStatementType) : type of the LEF statement.
        """
        self.type = type
        self.name = name

    def __str__(self):
        """_summary_
        The class object str description.
        Args:
            object (LefStatement): statement object
        """
        return f"LefStatement: {self.type.name} {self.name}"
