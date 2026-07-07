# WinMan

<p align="center">
  <img src="./images/win-man-pages-logo.png" alt="Windows Man Pages">

</p>

<p align="center">
  <img src="https://img.shields.io/github/stars/xchgll/winman" alt="Windows Man Pages">
  <img src="https://img.shields.io/github/forks/xchgll/winman" alt="Windows Man Pages">
  <img src="https://img.shields.io/twitter/follow/xchgll" alt="Windows Man Pages">
</p>


**WinMan** is an offline documentation for WIN/NT API with a man pages taste.

the tool downloads the documentation only one time, then you can browse it fully offline.

---

## Features

- its fully offline
- easy - fast searching & support wildcards `Virtual*`
- it supports windows/linux/macosX
- documentation is monthly updated


## Installation

only run

```bash
pip install winman==1.0.1
```

- Note: on windows do not forget to add Python Scripts Path to your environment variables

run `winman -u` to download or update documentations for first time

```bash
(venv) kali@kali:~$ winman -u
[?] Seems first time use winman
Download Documentation ? (y/n)                                                                                                                             
y
[+] New Update: First Version
Version: 1                                                                                                                                                 
Download Size: 14.8 MB                                                                                                                                     
Disk Size: 112 MB                                                                                                                                          
Wanna Update ? (y/n)
y
[#] Please Wait...
[#] Extracting Data
_misc.json
a.json
b.json
...
```

```
(venv) kali@kali:~$ winman -q VirtualProtect
VirtualProtect
  VirtualProtect function (memoryapi.h)

SYNOPSIS
  Header : memoryapi.h
  DLL    : Kernel32.dll
  LIB    : onecore.lib
  API    : VirtualProtect

DESCRIPTION
  Changes the protection on a region of committed pages in the virtual address space of the calling process.

To change the access protection of any process, use the [VirtualProtectEx](/windows/win32/api/memoryapi/nf-memoryapi-virtualprotectex) function.

PARAMETERS
  lpAddress
      Direction : in
      The address of the starting page of the region of pages whose access protection attributes are to be changed.

All pages in the specified region must be within the same reserved region allocated when calling the [VirtualAlloc](/windows/win32/api/memoryapi/nf-memoryapi-virtualalloc) or [VirtualAllocEx](/windows/win32/api/memoryapi/nf-memoryapi-virtualallocex) function using **MEM_RESERVE**. The pages cannot span adjacent reserved regions that were allocated by separate calls to **VirtualAlloc** or **VirtualAllocEx** using **MEM_RESERVE**.

  dwSize
      Direction : in
      The size of the region whose access protection attributes are to be changed, in bytes. The region of affected pages includes all pages containing one or more bytes in the range from the ***lpAddress*** parameter to `(lpAddress+dwSize)`. This means that a 2-byte range  straddling a page boundary causes the protection attributes of both pages to be changed.

  flNewProtect
      Direction : in
      The memory protection option. This parameter can be one of the [memory protection constants](/windows/win32/Memory/memory-protection-constants).

For mapped views, this value must be compatible with the access protection specified when the view was mapped (see [MapViewOfFile](/windows/win32/api/memoryapi/nf-memoryapi-mapviewoffile), [MapViewOfFileEx](/windows/win32/api/memoryapi/nf-memoryapi-mapviewoffileex), and [MapViewOfFileExNuma](/windows/win32/api/winbase/nf-winbase-mapviewoffileexnuma)).

  lpflOldProtect
      Direction : out
      A pointer to a variable that receives the previous access protection value of the first page in the specified region of pages. If this parameter is **NULL** or does not point to a valid variable, the function fails.

RETURN VALUE
  If the function succeeds, the return value is nonzero.

If the function fails, the return value is zero. To get extended error information, call [GetLastError](/windows/win32/api/errhandlingapi/nf-errhandlingapi-getlasterror).

REMARKS
You can set the access protection value on committed pages only. If the state of any page in the specified region is not committed, the function fails and returns without modifying the access protection of any pages in the specified region.

The **PAGE_GUARD** protection modifier establishes guard pages. Guard pages act as one-shot access alarms. For more information, see [Creating Guard Pages](/windows/win32/Memory/creating-guard-pages).

It is best to avoid using **VirtualProtect** to change page protections on memory blocks allocated by [GlobalAlloc](/windows/win32/api/winbase/nf-winbase-globalalloc), [HeapAlloc](/windows/win32/api/heapapi/nf-heapapi-heapalloc), or [LocalAlloc](/windows/win32/api/winbase/nf-winbase-localalloc), because multiple memory blocks can exist on a single page. The heap manager assumes that all pages in the heap grant at least read and write access.

When protecting a region that will be executable, the calling program bears responsibility for ensuring cache coherency via an appropriate call to [FlushInstructionCache](/windows/win32/api/processthreadsapi/nf-processthreadsapi-flushinstructioncache) once the code has been set in place.  Otherwise attempts to execute code out of the newly executable region may produce unpredictable results.

REQUIREMENTS
  Client : Windows XP [desktop apps \| UWP apps]
  Server : Windows Server 2003 [desktop apps \| UWP apps]

SOURCE
  memoryapi/nf-memoryapi-virtualprotect.md

====================                                                                                                                                       

```

You can also use wildcards

```
winman -q Virtual*
```