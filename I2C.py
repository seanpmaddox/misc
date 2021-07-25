# /*
# /* I2C.py
# /*
# /* I2C primatives
# /*
# /* v3.3
# /*
# /* 20190922 SPM
# /* 20191007 SPM - corrections, updates and additions to bump to v1.9
# /*  - implemented I2C Bus arbitration via the I2CBusState list structure and the captureI2CBus() and releaseI2CBus() functions
# /*  - implemented a .01 sleep between the write and read functions of the write8read16() function in an attempt to minimize read failure occurences if the ADC has not completed the requested conversion
# /* 20191203 SPM - bumped to v2.0 with the following changes;
# /*                1) for all external callable functions added the lockI2CBus optional parameter with a default value of True
# /*                2) implemented if/then structured code based on this boolean which controls whether or not the external call results in the I2C Bus being locked prior to read/write on it
# /*                3) this allows external callers to lock the I2C Bus outside of this scope and notify the I2C subsystem of this
# /*                4) this permits sequential repetitive calls to be performed with the caller holding the I2C Bus during the duration of these calls which improves performance
# /* 20191231 SPM - bumped to v2.9 with the following changes;
# /*                1. implemented a threading.RLock() as the resource lock for each I2C bus, this replaced the usage of a variable
# /* 20200117 SPM - bumped to v3.0 with the following changes;
# /*                1) made handle_error() private as _handle_error()
# /*                2) added lockI2CBus as an arg for _handle_error()
# /*                3) added a conditional release of I2CBus to _handle_error(), bus is released if lockI2CBus is True
# /* 20210227 SPM - bumped to v3.1 with the following changes;
# /*                1) changed lock from [0, 0, 0] to just [0, 0] - this provides 2 I2C busses, not 3
# /*                2) changed lock[1] = threading.RLock() and lock[2] = threading.RLock() to lock[0] and lock[1]
# /* 20210312 SPM - bumped to v3.2 with the following changes;
# /*                1) changed the lock semiphore from a public to a private
# /* 20210315 SPM - bumped to v3.3 with the following changes;
# /*                1) added the readByte function to read a byte from an I2C address
# /*
# /*

import smbus
import threading

_lock = [0, 0]
_lock[0] = threading.RLock()
_lock[1] = threading.RLock()

def captureI2CBus(Bus):
    """capture the I2C bus subsystem RLock
    """
    while not (_lock[Bus].acquire(True, .01)):
	pass

def releaseI2CBus(Bus):
    """release the I2C bus subsystem RLock
    """
    try:
        _lock[Bus].release()
    except:
	pass

def _handle_error(access_name, Bus, Address, Register, Error, lockI2CBus):
    """Handle exception condition for I2CDevice.
    """
    if (lockI2CBus):
        releaseI2CBus(Bus)
    return -1

def write8(Bus, Address, Register, Byte, lockI2CBus = True):
    """"Write an 8-bit value to the specified register/address."""
    if lockI2CBus:
        captureI2CBus(Bus)
    try:
        smbus.SMBus(Bus).write_byte_data(Address, Register, Byte)
        result = 0
    except IOError as Error:
        result = _handle_error('write8', Bus, Address, Register, Error, lockI2CBus)
    if lockI2CBus:
        releaseI2CBus(Bus)
    return result

def write16(Bus, Address, Register, Word, lockI2CBus = True):
    """Write a 16-bit value to the specified register/address pair."""
    if lockI2CBus:
        captureI2CBus(Bus)
    try:
        smbus.SMBus(Bus).write_word_data(Address, Register, Word)
        result = 0
    except IOError as Error:
        result = _handle_error('write16', Bus, Address, Register, Error, lockI2CBus)
    if lockI2CBus:
        releaseI2CBus(Bus)
    return result

def writeList(Bus, Address, Register, List, lockI2CBus = True):
    """Write an array of bytes using I2C format."""
    if lockI2CBus:
        captureI2CBus(Bus)
    try:
        smbus.SMBus(Bus).write_i2c_block_data(Address, Register, List)
        result = 0
    except IOError as Error:
        result = _handle_error('writeList', Bus, Address, Register, Error, lockI2CBus)
    if lockI2CBus:
        releaseI2CBus(Bus)
    return result

def readU8(Bus, Address, Register, lockI2CBus = True):
    """Read an unsigned byte from the I2C device."""
    if lockI2CBus:
        captureI2CBus(Bus)
    try:
        result = smbus.SMBus(Bus).read_byte_data(Address, Register)
    except IOError as Error:
        result = _handle_error('readU8', Bus, Address, Register, Error, lockI2CBus)
    if lockI2CBus:
        releaseI2CBus(Bus)
    return result

def readS8(Bus, Address, Register, lockI2CBus = True):
    """Read a signed byte from the I2C device."""
    if lockI2CBus:
        captureI2CBus(Bus)
    try:
        result = smbus.SMBus(Bus).read_byte_data(Address, Register)
        result = (result - 256) if result > 127 else result
    except IOError as Error:
        result = _handle_error('readS8', Bus, Address, Register, Error, lockI2CBus)
    if lockI2CBus:
        releaseI2CBus(Bus)
    return result

def readU16(Bus, Address, Register, lockI2CBus = True):
    """Read an unsigned 16-bit value from the I2C device."""
    if lockI2CBus:
        captureI2CBus(Bus)
    try:
        result = smbus.SMBus(Bus).read_word_data(Address, Register)
    except IOError as Error:
        result = _handle_error('readU16', Bus, Address, Register, Error, lockI2CBus)
    if lockI2CBus:
        releaseI2CBus(Bus)
    return result

def readS16(Bus, Address, Register, lockI2CBus = True):
    """"Read a signed 16-bit value from the I2C device."""
    if lockI2CBus:
        captureI2CBus(Bus)
    try:
        result = smbus.SMBus(Bus).read_word_data(Address, Register)
    except IOError as Error:
        result = _handle_error('readS16', Bus, Address, Register, Error, lockI2CBus)
    if lockI2CBus:
        releaseI2CBus(Bus)
    return result

def readList(Bus, Address, Register, Length, lockI2CBus = True):
    """Read a list of bytes from the I2C device."""
    if lockI2CBus:
        captureI2CBus(Bus)
    try:
        result = smbus.SMBus(Bus).read_i2c_block_data(Address, Register, Length)
    except IOError as Error:
        result = _handle_error('readList', Bus, Address, Register, Error, lockI2CBus)
    if lockI2CBus:
        releaseI2CBus(Bus)
    return result

def readByte(Bus, Address, lockI2CBus = True):
    """Read a byte from an address."""
    if lockI2CBus:
        captureI2CBus(Bus)
    try:
        result = smbus.SMBus(Bus).read_byte(Address)
    except IOError as Error:
        result = _handle_error('readByte', Bus, Address, 0, Error, lockI2CBus)
    if lockI2CBus:
        releaseI2CBus(Bus)
    return result

