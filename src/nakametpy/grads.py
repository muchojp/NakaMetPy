# Copyright 2022 nakamura_yuki. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import numpy as np
from numpy import ma
from ._error import ExceedZidxError, ExceedTidxError, InvalidTidxError, InvalidZidxError
import re
import os
import glob
import warnings
import datetime

class GrADS:
  """
  A nakametpy.grads `GrADS` is a collection of dimensions and variables. 

  The following class variables are read-only.

  **`dimensions`**: The `dimensions` dictionary maps the names of
  dimensions defined for the `Dataset` to instances of the
  `Dimension` class.

  **`variables`**: The `variables` dictionary maps the names of variables
  defined for this `Dataset` or `Group` to instances of the
  `Variable` class.
  """
  def __init__(self, filename, endian=None, do_squeeze=True):
    """
      **`__init__(self, filename, s2n=True, endian=None, do_squeese=True`**
      
      `GrADS` constructor which is simular to netCDF4-Python `Dataset` constructor.
      
      **`filename`**: Name of GrADS control file to handle GrADS binary data.
      
      **`s2n`**: Data saved direction in ydef.
      
      **`endian`**: Endian of the binary data. `big_endian`, `little_endian` and `native_endian` are available.
      
      **`do_squeeze`**: Whether drop dimension which have only one element. Default is True.
    """
    self.filename = filename
    self.do_squeese = do_squeeze
    self.dimensions = dict()
    
    s2n = True
    b2t = True
    
    with open(self.filename) as f:
      lines = f.readlines()
      
    _sidx = 1E30 # provisional value
    _eidx = None
    _var_idx = []
    _nzdims = []
    
    for idx, line in enumerate(lines):
      if "*" in line[:3]: # check for comment out
        continue
      else:
        if "dset" in line.lower():
          _binname = _get_line_list(line)[1]
          _binname = _replace_template(_binname)
          if "/" == _binname[0]: # is this enough ?
            self.binname = glob.glob(_binname)[0]
          else:
            self.binname = glob.glob(os.path.join(os.path.dirname(self.filename), _binname))[0]
          continue
            
        if "undef" in line.lower():
          self.undef = float(_get_line_list(line)[1])
          continue
          
        if "options" in line.lower(): # So far, endian, yrev, zrev is available. byteswapped is not supported.
          if "big_endian" in line.lower():
            self.endian = "big_endian"
          elif "little_endian" in line.lower():
            self.endian = "little_endian"
          else:
            self.endian = "native_endian"
          if "yrev" in line.lower():
            s2n = False
          if "zrev" in line.lower():
            b2t = False
          continue
          
        if "xdef" in line.lower():
          _xdef = _get_line_list(line)
          self.nx = int(_xdef[1])
          if "linear" in line.lower():
            self.dimensions["xdef"] = Dimension(np.arange(float(_xdef[3]), float(_xdef[3])+float(_xdef[1])*float(_xdef[4]), float(_xdef[4])), "xdef")
          else:
            warnings.warn("Debug Warning: Currently, Only 'LINEAR' is supported in XDEF.")
          continue
          
        if "ydef" in line.lower():
          _ydef = _get_line_list(line)
          self.ny = int(_ydef[1])
          if "linear" in line.lower():
            self.dimensions["ydef"] = Dimension(np.arange(float(_ydef[3]), float(_ydef[3])+float(_ydef[1])*float(_ydef[4]), float(_ydef[4]))[::(-1)**(int(s2n)+1)], "ydef") # if s2n is True -> +1, if False -> -1
          else:
            warnings.warn("Debug Warning: Currently, Only 'LINEAR' is supported in YDEF.")
          continue
          
        if "zdef" in line.lower():
          _zdef = _get_line_list(line)
          if "levels" in line.lower():
            _zdef = [float(_izdef) for _izdef in _zdef[3:int(_zdef[1])+3]]
            self.dimensions["zdef"] = Dimension(np.array(_zdef[::(-1)**(int(b2t)+1)]), "zdef")
          elif "linear" in line.lower():
            self.dimensions["zdef"] = Dimension(np.arange(float(_zdef[3]), float(_zdef[3])+float(_zdef[1])*float(_zdef[4]), float(_zdef[4]))[::(-1)**(int(b2t)+1)], "zdef") # if b2c is True -> +1, if False -> -1
          else:
            warnings.warn("Debug Warning: Currently, Only 'LEVELS' and 'LINEAR' are supported in ZDEF.")
          continue
          
        if "tdef" in line.lower():
          _tdef = _get_line_list(line)
          self.nt = int(_tdef[1])
          if "linear" in line.lower():
            _init_dt = datetime.datetime.strptime(_tdef[3].title(), "%HZ%d%b%Y")
            if _tdef[4][-2:].lower() == "hr":
              self.dimensions["tdef"] = Dimension(np.array([_init_dt + i*datetime.timedelta(hours=int(_tdef[4][:-2])) for i in range(int(_tdef[1]))]), "tdef")
            elif _tdef[4][-2:].lower() == "dy":
              self.dimensions["tdef"] = Dimension(np.array([_init_dt + i*datetime.timedelta(days=int(_tdef[4][:-2])) for i in range(int(_tdef[1]))]), "tdef")
            elif _tdef[4][-2:].lower() == "mo":
              self.dimensions["tdef"] = Dimension(np.array([_init_dt + i*datetime.timedelta(months=int(_tdef[4][:-2])) for i in range(int(_tdef[1]))]), "tdef")
          else:
            warnings.warn("Debug Warning: Currently, Only 'LINEAR' is supported in TDEF.")
          continue

        if bool(re.match("^vars", line.lower())):
          _sidx = idx
          _nvar2 = int(_get_line_list(line)[1])
          continue
        if bool(re.match("^endvars", line.lower())):
          _eidx = idx
          continue
        if (_sidx<idx) and (_eidx==None):
          _var_idx.append(idx)
          _inzdim = int(_get_line_list(line)[1])
          if _inzdim==0:
            _nzdims.append(1)
          else:
            _nzdims.append(_inzdim)
          
    if endian!=None:
      self.endian = endian
    if len(_var_idx)!=_nvar2:
      warnings.warn("The Number of variables is NOT match.")
      
    self.variables = _get_vars(self, lines, _var_idx, _nzdims, do_squeeze)

def _get_vars(self, lines, idx_list, nz_list, do_squeese): # self : grads.GrADS object
  """
  Get the variables info
  """
  variables = dict()
  for inidx, iline_idx in enumerate(idx_list):
    iline = lines[iline_idx]
    _ivar_list = _get_line_list(iline)
    varname = _ivar_list[0]
    idesc = None
    
    if "**" in iline:
      idesc = iline[(iline.index("**") + 1):].replace("\n", "").strip()
      if idesc == " ":
        idesc = None
    elif "*" in iline:
      idesc = iline[iline.index("*"):].replace("\n", "").strip()
      if idesc == " ":
        idesc = None
    else:
      idesc = None
    
    varids = np.cumsum(np.array(nz_list))
    _loop_block = varids[-1]
    varids = list(varids[:-1])
    varids.insert(0,0)
    varids = np.array(varids)
    
    variables[_ivar_list[0]] = Variable(self.binname, varname, varids[inidx],\
                        _loop_block, self.nx, self.ny, nz_list[inidx],\
                        self.nt, self.endian, self.undef, idesc, do_squeese)
  
  return variables      

def _get_line_list(line):
  """
  Get a list of single line.
  """
  return [i for i in re.split("[\s\t\n^,]+", \
          line.replace("\n", "", 1).strip()) if i != ""]
  
def _replace_template(dset):
  """
  Convert specific simbol into ?, which means some ONE letter.
  """
  for i in range(1, 5, 1):
    dset = re.sub(f"%[a-z]{i}", "?"*i, dset)
  return dset
            
class Variable:
  """
  A GrADS `Variable` is used to read 4 bytes direct access binary data.  
  They are analogous to numpy array objects. 
  See `Variable.__init__` for more details.
  """
  def __init__(self, binname, varname, varid, loop_block, nx, ny, nz, nt, endian, undef, desc, do_squeese):
    """
    **`__init__(self, binname, varname, varid, loop_block, nx, ny, nz, nt, endian, undef, desc, do_squeese)`**
    
    `Variable` constructor.
    """
    self._name = varname
    self._undef = undef
    self._binname = binname
    self._varid = varid
    self._loop_block = loop_block
    self._endian = endian
    self._nx = nx
    self._ny = ny
    self._nz = nz
    self._nt = nt
    self._dtype = np.float32
    self._desc = desc
    self._do_squeese = do_squeese

  def __array__(self):
    return self[...]

  def __repr__(self):
    return self.__str__()

  def __getitem__(self, elem):
    """
    Need for slicing.
    """
    return _sel(self._binname, self._name, self._varid, self._loop_block, self._endian,\
      self._nx, self._ny, self._nz, self._nt, self._undef, self._do_squeese)[elem]

  def __str__(self):
    ncdump = [repr(type(self))]
    ncdump.append(f'{self._dtype} {self._name}({self._nt}, {self._nz}, {self._ny}, {self._nx})')
    ncdump.append(f"    description: {self._desc}")
    ncdump.append(f"    _FillValue: {self._undef}")
    return "\n".join(ncdump)

  def sel(self,  zidx=None, tidx=None):
    return _sel(self._binname, self._name, self._varid, self._loop_block, self._endian, self._nx, self._ny, self._nz, self._nt, self._undef, self._do_squeese,  zidx, tidx)

def _sel(binname, name, varid, loop_block, endian, nx, ny, nz, nt, undef, do_squeese,  zidx=None, tidx=None):
  # check for index exceeding
  if tidx==None:
    tloop = range(nt)
  elif isinstance(tidx, int):
    if tidx >= nt:
      raise ExceedTidxError(name, (nt, nz, ny, nx), tidx)
    tloop = [tidx]
  elif isinstance(tidx, (list, tuple, np.ndarray)):
    for _itidx in tidx:
      if _itidx >= nt:
        raise ExceedTidxError(name, (nt, nz, ny, nx), _itidx)
    tloop = tidx
  else:
    raise InvalidTidxError(type(tidx))

  if zidx==None:
    zloop = range(nz)
  elif isinstance(zidx, int):
    if zidx >= nz:
      raise ExceedZidxError(name, (nt, nz, ny, nx), zidx)
    zloop = [zidx]
  elif isinstance(zidx, (list, tuple, np.ndarray)):
    for _izidx in zidx:
      if _izidx >= nz:
        raise ExceedZidxError(name, (nt, nz, ny, nx), _izidx)
    zloop = zidx
  else:
    raise InvalidZidxError(type(zidx))
  
  with open(binname, "rb") as f:
    _data = []
    for _it in tloop:
      if zloop==range(nz):
        f.seek((_it*loop_block+varid)*nx*ny*4, os.SEEK_SET)
        _data.append(ma.masked_equal(ma.masked_array(np.fromfile(f,\
          dtype=_endian2simbole(endian)+"f4", count=nx*ny*nz)), value=undef).reshape(nz, ny, nx))
      else:
        _idata = []
        for _iz in zloop:
          f.seek((varid+_it*loop_block+_iz)*nx*ny*4, os.SEEK_SET)
          _idata.append(ma.masked_equal(ma.masked_array(np.fromfile(f, dtype=_endian2simbole(endian)+"f4", count=nx*ny)), value=undef).reshape(ny, nx))
        _data.append(_idata)

  _data = ma.masked_array(_data)
  if do_squeese:
    return ma.squeeze(_data)
  else:
    return _data


class Dimension:
  """
  A GrADS `Dimension` is used to describe the coordinates of a `Variable`.
  See `Dimension.__init__` for more details.
  """
  def __init__(self, data, var):
    """
    **`__init__(self, data, var)`**
    """
    self.values = data
    self.dim = var

  def __array__(self):
    return self[...]

  def __repr__(self):
    return self.__str__()

  def __getitem__(self, elem):
    """
    Need for slicing.
    """
    return self.values[elem]

  def __str__(self):
    ncdump = [repr(type(self))]
    ncdump.append(f"    variables(dimensions): {self.dim}, ")
    ncdump.append(f"    dimensions(sizes): {len(self.values)}, ")
    ncdump.append(f"    dimensions(data): {self.values}, ")
    return "\n".join(ncdump)

def _endian2simbole(endian):
  """
  Get NumPy's endian simbol from the words.
  """
  if endian.lower() == "big_endian":
    return ">"
  elif endian.lower() == "little_endian":
    return "<"
  elif endian.lower() == "native_endian":
    return "="
  else:
    return ""