## Python modules
import re

## Regular expressions

## Cisco-like AABB.CCDD.EEFF
rx_mac_address_cisco = re.compile(
    r"^[0-9A-F]{4}(?P<sep>[.\-])[0-9A-F]{4}(?P=sep)[0-9A-F]{4}$")
## Alternative Cisco form 01AA.BBCC.DDEE.FF
rx_mac_address_cisco_media = re.compile(
    "^01[0-9A-F]{2}\.[0-9A-F]{4}\.[0-9A-F]{4}\.[0-9A-F]{2}$")
## Size blocks, leading zeroes can be ommited
## AA:BB:C:DD:EE:F
rx_mac_address_sixblock = re.compile(
    "^([0-9A-F]{1,2}):([0-9A-F]{1,2}):([0-9A-F]{1,2}):([0-9A-F]{1,2}):([0-9A-F]{1,2}):([0-9A-F]{1,2})$")
## HP-like AABBCC-DDEEFF
rx_mac_address_hp = re.compile("^[0-9A-F]{6}-[0-9A-F]{6}$")
## Unseparated block
rx_mac_address_solid = re.compile(r"^[0-9A-F]{12}$")


class MAC(str):
    """
    MAC address validation and conversion class

    >>> MAC("1234.5678.9ABC")
    '12:34:56:78:9A:BC'
    >>> MAC("1234.5678.9abc")
    '12:34:56:78:9A:BC'
    >>> MAC("0112.3456.789a.bc")
    '12:34:56:78:9A:BC'
    >>> MAC("1234.5678.9abc.def0")
    Traceback (most recent call last):
        ...
    ValueError: Invalid MAC: '1234.5678.9abc.def0'
    >>> MAC("12:34:56:78:9A:BC")
    '12:34:56:78:9A:BC'
    >>> MAC("12-34-56-78-9A-BC")
    '12:34:56:78:9A:BC'
    >>> MAC("0:13:46:50:87:5")
    '00:13:46:50:87:05'
    >>> MAC("123456-789abc")
    '12:34:56:78:9A:BC'
    >>> MAC("12-34-56-78-9A-BC-DE")   #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    ValueError: Invalid MAC: '12:34:56:78:9A:BC:DE'
    >>> MAC("AB-CD-EF-GH-HJ-KL")   #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    ValueError: Invalid MAC: 'AB:CD:EF:GH:HJ:KL'
    >>> MAC("aabb-ccdd-eeff")
    'AA:BB:CC:DD:EE:FF'
    >>> MAC("aabbccddeeff")
    'AA:BB:CC:DD:EE:FF'
    >>> MAC("AABBCCDDEEFF")
    'AA:BB:CC:DD:EE:FF'
    >>> MAC("AABBCCDDEEFF") + " -- " + MAC("0011.2233.4455")
    'AA:BB:CC:DD:EE:FF -- 00:11:22:33:44:55'
    """

    def __new__(cls, mac):
        return super(MAC, cls).__new__(cls, cls._clean(mac))

    @classmethod
    def _clean(self, mac):
        value = mac
        value = value.upper()
        match = rx_mac_address_solid.match(value)
        if match:
            return "%s:%s:%s:%s:%s:%s" % (
                value[:2], value[2:4], value[4:6],
                value[6:8], value[8:10], value[10:])
        match = rx_mac_address_cisco_media.match(value)
        if match:
            value = value.replace(".", "")[2:]
            return "%s:%s:%s:%s:%s:%s" % (
                value[:2], value[2:4], value[4:6],
                value[6:8], value[8:10], value[10:])
        match = rx_mac_address_cisco.match(value)
        if match:
            value = value.replace(".", "").replace("-", "")
        else:
            match = rx_mac_address_hp.match(value)
            if match:
                value = value.replace("-", "")
            else:
                value = value.replace("-", ":")
                match = rx_mac_address_sixblock.match(value)
                if not match:
                    raise ValueError("Invalid MAC: '%s'" % mac)
                value = ""
                for i in range(1, 7):
                    v = match.group(i)
                    if len(v) == 1:
                        v = "0" + v
                    value += v
        return "%s:%s:%s:%s:%s:%s" % (
            value[:2], value[2:4], value[4:6],
            value[6:8], value[8:10], value[10:])

    def to_cisco(self):
        """
        Convert to Cisco-like format

        >>> MAC("AA:BB:CC:DD:EE:FF").to_cisco()
        'aabb.ccdd.eeff'
        """
        r = self.lower().replace(":", "")
        return "%s.%s.%s" % (r[:4], r[4:8], r[8:])

    def shift(self, count):
        """
        Return shifted MAC address

        >>> MAC("AA:BB:CC:DD:EE:FF").shift(0)
        'AA:BB:CC:DD:EE:FF'
        >>> MAC("AA:BB:CC:DD:EE:FF").shift(1)
        'AA:BB:CC:DD:EF:00'
        >>> MAC("AA:BB:CC:DD:EE:FF").shift(256)
        'AA:BB:CC:DD:EF:FF'
        >>> MAC("AA:BB:CC:DD:EE:FF").shift(257)
        'AA:BB:CC:DD:F0:00'
        >>>MAC("AA:BB:CC:DD:EE:FF").shift(4096)
        'AA:BB:CC:DD:FE:FF'

        :param count:
        :return:
        """
        # Convert to 64-bit integer
        v = 0L
        for o in [int(x, 16) for x in self.split(":")]:
            v <<= 8
            v += o
        # Shift count addresses
        v += count
        # Convert back to MAC
        r = []
        for i in range(6):
            r += ["%02X" % (v & 0xFF)]
            v >>= 8
        r.reverse()
        return ":".join(r)


class Parameter(object):
    """
    Abstract parameter
    """
    def __init__(self, required=True, default=None):
        self.required = required
        self.default = default
        if default is not None:
            self.default = self.clean(default)

    def clean(self, value):
        """
        Input parameter normalization

        :param value: Input parameter
        :type value: Arbitrary python type
        :return: Normalized value
        """
        return value


class StringParameter(Parameter):
    """
    >>> StringParameter().clean("Test")
    'Test'
    >>> StringParameter().clean(10)
    '10'
    >>> StringParameter().clean(None)
    'None'
    >>> StringParameter(default="test").clean("no test")
    'no test'
    >>> StringParameter(default="test").clean(None)
    'test'
    >>> StringParameter(choices=["1","2"]).clean("1")
    '1'
    >>> StringParameter(choices=["1","2"]).clean("3") #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    InterfaceTypeError: StringParameter: '3'.
    """
    def __init__(self, required=True, default=None, choices=None):
        self.choices = choices
        super(StringParameter, self).__init__(required=required,
                                              default=default)

    def clean(self, value):
        if value is None and self.default is not None:
            return self.default
        try:
            value = str(value)
        except:
            self.raise_error(value)
        if self.choices and value not in self.choices:
            self.raise_error(value)
        return value


class MACAddressParameter(StringParameter):
    """
    >>> MACAddressParameter().clean("1234.5678.9ABC")
    '12:34:56:78:9A:BC'
    >>> MACAddressParameter().clean("1234.5678.9abc")
    '12:34:56:78:9A:BC'
    >>> MACAddressParameter().clean("0112.3456.789a.bc")
    '12:34:56:78:9A:BC'
    >>> MACAddressParameter().clean("1234.5678.9abc.def0") #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    InterfaceTypeError: MACAddressParameter: '1234.5678.9ABC.DEF0'
    >>> MACAddressParameter().clean("12:34:56:78:9A:BC")
    '12:34:56:78:9A:BC'
    >>> MACAddressParameter().clean("12-34-56-78-9A-BC")
    '12:34:56:78:9A:BC'
    >>> MACAddressParameter().clean("0:13:46:50:87:5")
    '00:13:46:50:87:05'
    >>> MACAddressParameter().clean("123456-789abc")
    '12:34:56:78:9A:BC'
    >>> MACAddressParameter().clean("12-34-56-78-9A-BC-DE") #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    InterfaceTypeError: MACAddressParameter: '12:34:56:78:9A:BC:DE'
    >>> MACAddressParameter().clean("AB-CD-EF-GH-HJ-KL") #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    InterfaceTypeError: MACAddressParameter: 'AB:CD:EF:GH:HJ:KL'
    >>> MACAddressParameter().clean("aabb-ccdd-eeff")
    'AA:BB:CC:DD:EE:FF'
    >>> MACAddressParameter().clean("aabbccddeeff")
    'AA:BB:CC:DD:EE:FF'
    >>> MACAddressParameter().clean("AABBCCDDEEFF")
    'AA:BB:CC:DD:EE:FF'
    >>> MACAddressParameter().clean("\\xa8\\xf9K\\x80\\xb4\\xc0")
    'A8:F9:4B:80:B4:C0'
    >>> MACAddressParameter(accept_bin=False).clean("\\xa8\\xf9K\\x80\\xb4\\xc0") #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    InterfaceTypeError: MACAddressParameter: '\xa8\xf9K\x80\xb4\xc0'.
    """
    def __init__(self, required=True, default=None, accept_bin=True):
        self.accept_bin = accept_bin
        super(MACAddressParameter, self).__init__(required=required,
                                                  default=default)

    def clean(self, value):
        if value is None and self.default is not None:
            return self.default
        value = super(MACAddressParameter, self).clean(value)
        if len(value) == 6 and self.accept_bin:
            # MAC address in binary form
            return str(MAC(":".join(["%02X" % ord(c) for c in value])))
        return str(MAC(value))